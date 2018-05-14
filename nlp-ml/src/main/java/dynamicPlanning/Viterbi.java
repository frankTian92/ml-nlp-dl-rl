package dynamicPlanning;


import org.nd4j.linalg.api.ndarray.INDArray;

import java.util.ArrayList;
import java.util.List;

/**
 * Created by stormor on 2017/11/9.
 * 维特比动态规划算法
 */
public class Viterbi  {

  //排序后的各个结果
    private List<ViterBiData> rankReslut;


    /**
     * 对序列orig_seq进行最有路径排序，运用维特比算法
     *
     * @param orig_seq 原始序列：待排序的序列
     * @param trans_p_arr2 转移概率矩阵：边长为词典的正方形矩阵
     * @param start_p_arr1  初始概率：长度等于词典长度
     * @return
     */
    public ViterBiData computer(Integer[] orig_seq, INDArray trans_p_arr2, INDArray start_p_arr1) {
        List<ViterBiData> rankReslut = new ArrayList<ViterBiData>();
        int origSeqSize = orig_seq.length;
//        int dictSize = start_p_arr1.length();

        // 路径概率表 V[原始序列][词典宽度] = 概率
        double[][] V = new double[origSeqSize][origSeqSize];
        // 一个中间变量，代表当前序列是哪个词典对于的值
        int[][] path = new int[origSeqSize][origSeqSize];

        //第一次的初始概率
        for (int i = 0; i<origSeqSize;i++){
            V[0][i] = start_p_arr1.getDouble(0,orig_seq[i]);
            path[i][0] = orig_seq[i];
        }



        for (int t = 1; t < origSeqSize; t++) {
            int[][] newpath = new int[origSeqSize][origSeqSize];

            for (int y = 0; y<origSeqSize;y++) {
                double prob = -1;
                int state;
                for (int y0 = 0; y0<origSeqSize;y0++) {
                    double nprob = V[t - 1][y0] * trans_p_arr2.getDouble(orig_seq[y0],orig_seq[y]);
                    if (nprob > prob) {
                        prob = nprob;
                        state = y0;
                        // 记录最大概率
                        V[t][y] = prob;
                        // 记录路径
                        System.arraycopy(path[state], 0, newpath[y], 0, t);
                        newpath[y][t] = orig_seq[y];
                    }
                }
            }

            path = newpath;

        }

        double prob = -1;
        int state = 0;
        for (int y = 0; y<origSeqSize;y++) {
            ViterBiData viterBiData = new ViterBiData();
            viterBiData.setProbility(V[origSeqSize - 1][y]);
            viterBiData.setSeqRank(path[y]);
            rankReslut.add(viterBiData);

            if (V[origSeqSize - 1][y] > prob) {
                prob = V[origSeqSize - 1][y];
                state = y;
            }
        }

        this.rankReslut = rankReslut;
        ViterBiData bestViterBiData = new ViterBiData();
        bestViterBiData.setProbility(prob);
        bestViterBiData.setSeqRank(path[state]);
        return bestViterBiData;
    }


    /**
     * 只有先进行computer计算才能获得该数据
     * @return
     */
    public List<ViterBiData> getRankReslut() {
        if (rankReslut.size()>0){
            return rankReslut;
        }else {
            System.out.println("Please compute before!!!");
            return null;
        }

    }
}

