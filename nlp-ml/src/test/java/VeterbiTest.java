import dynamicPlanning.ViterBiData;
import dynamicPlanning.ViterModel;
import dynamicPlanning.Viterbi;
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
    public void VetBTest(){

        ViterModel viterModel = new ViterModel();
        HashMap<String,List<Integer>> trainData = getTrainData();

        int dictSize = 4;
        viterModel.trainModel(trainData,dictSize);
        INDArray trans_p_arr = viterModel.getTrans_p_arr();

        Viterbi viterbi = new Viterbi();
        Integer[] orig_seq = new Integer[]{3,0,1,2};
        ViterBiData viterBiData = viterbi.computer(orig_seq,trans_p_arr);
        List<ViterBiData> viterBiDataList = viterbi.getRankReslut();
        double max_prob = viterBiData.getProbility();
        int[] final_seq = viterBiData.getSeqRank();
        System.out.println(max_prob);
        for (int i :final_seq){
            System.out.print(i+",");
        }
        System.out.println();
    }

    /**
     * 获得训练转移矩阵的数据
     * @return
     */
    private HashMap<String,List<Integer>> getTrainData(){
        HashMap<String,List<Integer>> trainData = new HashMap<>();
        String[] keys = new String[]{"a","b","c","d","e","f","g"};
        int[][] seq = new int[6][4];
        seq[0] = new int[]{2,1,0};
        seq[1] = new int[]{3,1,0};
        seq[2] = new int[]{3,2,0};
        seq[3] = new int[]{1,0};
        seq[4] = new int[]{2,0};
        seq[5] = new int[]{3,0};
        int data_size = seq.length;
        for (int i = 0;i<data_size;i++){
            int[] ints = seq[i];
            List<Integer> list = new ArrayList<>();
            for (int j = 0;j<ints.length;j++){
                list.add(ints[j]);
            }
            trainData.put(keys[i],list);
        }
        return trainData;
    }
}