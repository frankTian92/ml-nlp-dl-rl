package dynamicPlanning;


import org.nd4j.linalg.api.ndarray.INDArray;

import java.util.ArrayList;
import java.util.List;

/**
 * Created by stormor on 2017/11/9.
 * 维特比动态规划算法
 */
public class Viterbi {

    //排序后的各个结果
    private List<ViterBiData> rankReslut;


    /**
     * 对序列orig_seq进行最有路径排序，运用维特比算法
     *
     * @param orig_seq    原始序列：待排序的序列
     * @param trans_p_arr 转移概率矩阵：边长为词典的正方形矩阵
     * @return
     */
    public ViterBiData computer(Integer[] orig_seq, INDArray trans_p_arr) {
        List<ViterBiData> rankReslut = new ArrayList<ViterBiData>();
        int origSeqSize = orig_seq.length;
//        int dictSize = start_p_arr1.length();

        // 路径序列表 V[原始序列][原始序列]
        int[][] path = new int[origSeqSize][origSeqSize];
        //初始化第一列,其余的序列均为-1
        for (int i = 0; i < origSeqSize; i++) {
            for (int j = 0;j<origSeqSize;j++){
                if (i==0){
                    path[j][i] = orig_seq[j];
                }else {
                    path[j][i]=-1;
                }
            }

        }


        // 一个中间变量，代表当前序列最大的概率值
        double[] maxProb = new double[origSeqSize];
        //初始化最大概率
        for (int i = 0; i < origSeqSize; i++) {
            maxProb[i] = 1.0;
        }


        //对每个跨度进行排序，选出每种概率最大的排序，并记录下该序列
        for (int t = 1; t < origSeqSize; t++) {
            //对每个节点对其他节点进行全排序，并计算概率,将概率最大的序列及概率值添加到对应的值中
            for (int y = 0; y < origSeqSize; y++) {
                int state = 0;
                double prob = -1;
                int[] seq_y = path[y];
                int orig_node = seq_y[t-1];
                for (int y0 = 0; y0 < origSeqSize; y0++) {
                    //排除“两个节点相同的情况”及“已经在序列中的节点”
                    int next_node = orig_seq[y0];
                    if (orig_node != next_node && !isIn(seq_y,next_node)) {
                        double y_y0_prob = maxProb[y] * trans_p_arr.getDouble(orig_node, next_node);
                        if (y_y0_prob > prob) {
                            prob = y_y0_prob;
                            state = next_node;
                        }
                    }
                }
                path[y][t] = state;
                maxProb[y] = prob;

            }
        }

        double max_prob = -1;
        int[] best_seq = new int[origSeqSize];
        for (int i = 0; i < origSeqSize; i++) {
            ViterBiData viterBiData = new ViterBiData();
            viterBiData.setProbility(maxProb[i]);
            viterBiData.setSeqRank(path[i]);
            rankReslut.add(viterBiData);
            if (maxProb[i] > max_prob) {
                max_prob = maxProb[i];
                best_seq = path[i];
            }
        }

        this.rankReslut = rankReslut;
        ViterBiData bestViterBiData = new ViterBiData();
        bestViterBiData.setProbility(max_prob);
        bestViterBiData.setSeqRank(best_seq);
        return bestViterBiData;
    }

    /**
     * 判断该数字是否在数组中
     *
     * @param nums
     * @param num
     * @return
     */
    private boolean isIn(int[] nums, int num) {
        boolean isIn = false;
        for (int nu : nums) {
            if (nu == num) {
                isIn = true;
                break;
            }
        }
        return isIn;
    }


    /**
     * 只有先进行computer计算才能获得该数据
     *
     * @return
     */
    public List<ViterBiData> getRankReslut() {
        if (rankReslut.size() > 0) {
            return rankReslut;
        } else {
            System.out.println("Please compute before!!!");
            return null;
        }

    }
}

