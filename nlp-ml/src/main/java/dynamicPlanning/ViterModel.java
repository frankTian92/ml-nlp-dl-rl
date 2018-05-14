package dynamicPlanning;

import Util.ReadWriteTxtUtil;
import com.alibaba.fastjson.JSONObject;
import org.nd4j.linalg.api.ndarray.INDArray;
import org.nd4j.linalg.factory.Nd4j;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;

public class ViterModel {
    private INDArray trans_p_arr2;
    private INDArray strat_p_arr1;

    private static Viterbi viterbi = new Viterbi();

    public ViterModel(){
     super();
    }

    private ViterModel(INDArray trans_p_arr2,INDArray strat_p_arr1){
        this.trans_p_arr2= trans_p_arr2;
        this.strat_p_arr1 = strat_p_arr1;
    }



    /**
     * 维特比模型训练
     * @param trainData 训练数据
     * @param dictSize 转移矩阵宽度
     */
    public ViterModel trainModel(HashMap<String,List<Integer>> trainData,int dictSize){
       INDArray trans_p_Nd = Nd4j.ones(dictSize,dictSize);
       INDArray start_p_Nd = Nd4j.ones(dictSize);

       //获得词典表和起始列表
        trainData.values().stream().filter(list -> list.size() >= 2).forEach(list -> {
            int first = list.get(0);
            start_p_Nd.put(0, first, start_p_Nd.getInt(0, first) + 1);
            for (int i = 0; i < list.size() - 1; i++) {
                int before = list.get(i);
                int after = list.get(i + 1);
                trans_p_Nd.put(after, before, trans_p_Nd.getInt(after, before) + 1);
            }
        });

//        ReadWriteTxtUtil.writeTxtArr1("E:\\工作\\九州通\\九州通数据分析\\第一站点概率.txt",start_p_Nd,dictSize);
        ReadWriteTxtUtil.writeTxtArr2("E:\\工作\\九州通\\九州通数据分析\\站点之间的概率转移.txt",trans_p_Nd,dictSize);

        ViterModel viterModel = new ViterModel(trans_p_Nd,start_p_Nd);
        return viterModel;
    }


    /**
     * 测试准确率
     * @param testData
     * @return
     */
    public double testModel(HashMap<String,List<Integer>> testData){
        List<Integer> total = new ArrayList<>();
        List<Integer> acc = new ArrayList<>();
       testData.values().stream().filter( list -> list.size()>=2).forEach(list ->{
           boolean equal = true;
           total.add(1);
           int[] result = computer(list);
           System.out.println("原来的序列 = " +JSONObject.toJSON(list));
           System.out.println("预测的序列 = " +JSONObject.toJSON(result));

           for (int i = 0;i<result.length;i++){
               if (result[i] != list.get(i).intValue()){
                   equal = false;
                   break;
               }
           }
           if (equal){
               acc.add(1);
           }

       });

       return acc.size()/(total.size()+0.0);

    }


    /**
     * 为每条记录进行排序
     * @param ops_seq
     * @return
     */
    public int[] computer(List<Integer> ops_seq){
        Integer[] ops = (Integer[]) ops_seq.toArray(new Integer[ops_seq.size()]);
        return viterbi.computer(ops,trans_p_arr2,strat_p_arr1).getSeqRank();
    }




}