import dynamicPlanning.ViterBiData;
import dynamicPlanning.ViterModel;
import dynamicPlanning.Viterbi;
import dynamicPlanning.domain.SameProbData;
import org.junit.Test;
import org.nd4j.linalg.api.ndarray.INDArray;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;

/**
 * \* Created with IntelliJ IDEA.
 * \* User: Administrator
 * \* Date: 2018/5/15 0015
 * \* Time: 下午 19:28
 * \* Description:
 * \
 */
public class VeterbiTest {
    @Test
    public void VetBTest1(){
        Integer[] pre_seq = new Integer[]{1,0,3,2,4};
        int dict_size = 5;
        HashMap<String,List<Integer>> trainData = new HashMap<>();
        String[] keys = new String[]{"a","b","c","d","e","f","g","h"};
        int[][] seq = new int[8][4];
        seq[0] = new int[]{2,1,0};
        seq[1] = new int[]{3,1,0};
        seq[2] = new int[]{3,2,0};
        seq[3] = new int[]{1,0};
        seq[4] = new int[]{2,0};
        seq[5] = new int[]{3,0};
        seq[6] = new int[]{4,2};
        seq[7] = new int[]{4,0};
        int data_size = seq.length;
        for (int i = 0;i<data_size;i++){
            int[] ints = seq[i];
            List<Integer> list = new ArrayList<>();
            for (int j = 0;j<ints.length;j++){
                list.add(ints[j]);
            }
            trainData.put(keys[i],list);
        }
        VetBT(dict_size,pre_seq,trainData);

    }


    private void VetBT(int dictSize,Integer[] rank_seq,  HashMap<String,List<Integer>> trainData ){
        ViterModel viterModel = new ViterModel();
        viterModel.trainModel(trainData,dictSize);
        INDArray trans_p_arr = viterModel.getTrans_p_arr();
        Viterbi viterbi = new Viterbi();
        ViterBiData viterBiData = viterbi.computer(rank_seq,trans_p_arr);
        List<ViterBiData> viterBiDataList = viterbi.getRankReslut();
        double max_prob = viterBiData.getProbility();
        List<Integer> final_seq = viterBiData.getFirstSeqRank();
        System.out.println("最终的最优路径有 "+ viterBiData.getSameProbNum() + "个");
        System.out.println(max_prob);
        for (int i :final_seq){
            System.out.print(i+",");
        }
        System.out.println();
    }


}