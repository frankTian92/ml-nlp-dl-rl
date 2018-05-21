package dynamicPlanning;


import dynamicPlanning.domain.SameProbData;
import org.nd4j.linalg.api.ndarray.INDArray;

import java.util.ArrayList;
import java.util.Arrays;
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
//        int[][] path = new int[origSeqSize][origSeqSize];
        //考虑可能相同概率的数据出现,则path的路径可能会在中间有所增减
        List<List<Integer>> path = new ArrayList<>();
        //初始化第一列,每一个list表示为可能的路径，每个路径首个值为序列的值
        for (int i = 0; i < origSeqSize; i++) {
            List<Integer> every_path_first = new ArrayList<>();
            Integer first_data = orig_seq[i];
            every_path_first.add(0, first_data);
            path.add(i, every_path_first);
        }


        // 一个中间变量，代表当前序列最大的概率值
//        double[] maxProb = new double[origSeqSize];
        List<Double> maxProb = new ArrayList<>();
        //初始化最大概率
        for (int i = 0; i < origSeqSize; i++) {
            maxProb.add(i, 0.0);
        }


        //对每个跨度进行排序，选出每种概率最大的排序，并记录下该序列
        for (int t = 1; t < origSeqSize; t++) {
            List<List<Integer>> newPath = new ArrayList<>();
            List<Double> newMaxProb = new ArrayList<>();
            //对每个节点对其他节点进行全排序，并计算概率,将概率最大的序列及概率值添加到对应的值中
            for (int y = 0; y < origSeqSize; y++) {
                Integer next_node = orig_seq[y];
                List<Integer> max_prob_seq = new ArrayList<>();
                double max_prob = -1;
                SameProbData sameProbData = new SameProbData();
                int pastSize = path.size();
                for (int y0 = 0; y0 < pastSize; y0++) {
                    //排除“两个节点相同的情况”及“已经在序列中的节点”
                    List<Integer> last_best_path = new ArrayList<>();
                    last_best_path.addAll(path.get(y0));
                    int last_node = last_best_path.get(last_best_path.size() - 1);
                    if (last_node!=next_node && !last_best_path.contains(next_node)) {
                        double y_y0_prob = maxProb.get(y0) + trans_p_arr.getDouble(last_node, next_node.intValue());
                        if (y_y0_prob > max_prob) {
                            max_prob = y_y0_prob;
                            max_prob_seq = last_best_path;
                        }
                        //对路径概率相同的情况进行处理
                        else if (y_y0_prob == max_prob) {
                            sameProbData.upDate(last_best_path, max_prob);
                        }
                    }
                }

                //将最终与最大概率相同的序列添加到最新的子阶段序列中
                if (sameProbData.getSameMaxPro() == max_prob && max_prob>-1.0) {
                    List<List<Integer>> same_seq = sameProbData.getSameSeq();
                    for (List<Integer> same_last_seq : same_seq) {
                        same_last_seq.add(t, next_node);
                        newPath.add(same_last_seq);
                        newMaxProb.add(max_prob);
                    }
                }

                //将最大的概率序列添加到最新的子序列中
                if (max_prob>-1.0){
                    max_prob_seq.add(next_node);
                    newPath.add(max_prob_seq);
                    newMaxProb.add(max_prob);
                }
            }

            path = newPath;
            maxProb = newMaxProb;

        }

        double max_prob = -1;
        List<Integer> best_seq = null;
        int past_size = path.size();
        SameProbData sameProbData = new SameProbData();
        for (int i = 0; i < past_size; i++) {
            ViterBiData viterBiData = new ViterBiData();
            double max_prob_i = maxProb.get(i);
            List<Integer> max_prob_seq = path.get(i);
            viterBiData.setProbility(max_prob_i);
            viterBiData.addSeq(max_prob_seq);
            rankReslut.add(viterBiData);
            if (max_prob_i > max_prob) {
                max_prob = max_prob_i;
                best_seq = max_prob_seq;
            } else if (max_prob_i == max_prob) {
                sameProbData.upDate(max_prob_seq, max_prob);
            }
        }

        this.rankReslut = rankReslut;


        ViterBiData bestViterBiData = new ViterBiData();

        //最终的结果为多个的情况
        if (sameProbData.getSameMaxPro() == max_prob) {
            bestViterBiData.setSeqRankList(sameProbData.getSameSeq());
        }
        bestViterBiData.addSeq(best_seq);
        bestViterBiData.setProbility(max_prob);

        return bestViterBiData;
    }

//    /**
//     * 判断该数字是否在数组中
//     *
//     * @param nums
//     * @param num
//     * @return
//     */
//    private boolean isIn(int[] nums, int num) {
//        boolean isIn = false;
//        for (int nu : nums) {
//            if (nu == num) {
//                isIn = true;
//                break;
//            }
//        }
//        return isIn;
//    }


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

