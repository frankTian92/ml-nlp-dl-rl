package dynamicPlanning;

import Util.ReadWriteTxtUtil;
import com.alibaba.fastjson.JSONObject;
import org.nd4j.linalg.api.ndarray.INDArray;
import org.nd4j.linalg.factory.Nd4j;
import org.nd4j.linalg.ops.transforms.Transforms;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.IntSummaryStatistics;
import java.util.List;

public class ViterModel {
    private INDArray trans_p_arr;

    private static Viterbi viterbi = new Viterbi();

    public ViterModel(){
     super();
    }

    private ViterModel(INDArray trans_p_arr){
        this.trans_p_arr= trans_p_arr;
    }



    /**
     * 维特比模型训练
     * @param trainData 训练数据
     * @param dictSize 转移矩阵宽度
     */
    public void trainModel(HashMap<String,List<Integer>> trainData,int dictSize){
       INDArray trans_p_Nd = Nd4j.zeros(dictSize,dictSize);
//        INDArray trans_p_Nd = Nd4j.ones(dictSize,dictSize);
       //存储每个点在样本中出现的次数
//       INDArray trans_p_Num = Nd4j.ones(dictSize,dictSize);
//       INDArray start_p_Nd = Nd4j.ones(dictSize);

       //获得词典表和起始列表
        trainData.values().stream().filter(list -> list.size() >= 2).forEach(list -> {
            //只做相邻两个之间的先后顺序
//            for (int i = 0; i < list.size() - 1; i++) {
//                int before = list.get(i);
//                int after = list.get(i + 1);
//                trans_p_Nd.put(before, after, trans_p_Nd.getInt(before, after) + 1);
//            }
            //假设排序的顺序是有传递性的，即排在前面的可能性币排在后面的可能性要大
            for (int i = 0; i < list.size() - 1; i++) {
                int before = list.get(i);
                for (int j =i+1;j<list.size();j++){
                    int dis = j-i;
                    //两者距离衰减
                    double dis_decay = 1.0/dis;
                    if (dis_decay<1.0){
                        dis_decay = dis_decay/10.0;
                    }
                    int after = list.get(j);
                    trans_p_Nd.put(before, after, trans_p_Nd.getDouble(before, after) +1.0+ dis_decay);
//                    trans_p_Num.put(before,after,trans_p_Num.getInt(before,after)+1.0);
                }

            }
        });

//        INDArray trans_p_Nd_norm= trans_p_Nd.div(trans_p_Num);
//        this.trans_p_arr = trans_p_Nd_norm;
        trans_p_arr = trans_p_Nd;
//        trans_p_arr = Transforms.sigmoid(trans_p_Nd);
//        ReadWriteTxtUtil.writeTxtArr1("E:\\工作\\九州通\\九州通数据分析\\第一站点概率.txt",start_p_Nd,dictSize);
        ReadWriteTxtUtil.writeTxtArr2("D:\\myProject\\ml-nlp-dl-rl\\nlp-ml\\src\\main\\resources\\Jointown\\站点之间的概率转移.txt",trans_p_Nd,dictSize);
//        ReadWriteTxtUtil.writeTxtArr2("D:\\myProject\\ml-nlp-dl-rl\\nlp-ml\\src\\main\\resources\\Jointown\\站点之间出现的数据.txt",trans_p_Num,dictSize);
        ReadWriteTxtUtil.writeTxtArr2("D:\\myProject\\ml-nlp-dl-rl\\nlp-ml\\src\\main\\resources\\Jointown\\站点之间出现的数据_归一化.txt",trans_p_arr,dictSize);

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
           List<Integer> result = computer(list);
           System.out.println("原来的序列 = " +JSONObject.toJSON(list));
           System.out.println("预测的序列 = " +JSONObject.toJSON(result));

           for (int i = 0;i<result.size();i++){
               if (result.get(i) != list.get(i).intValue()){
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
    public List<Integer> computer(List<Integer> ops_seq){
        Integer[] ops = (Integer[]) ops_seq.toArray(new Integer[ops_seq.size()]);
        return viterbi.computer(ops,trans_p_arr).getFirstSeqRank();
    }

    public INDArray getTrans_p_arr() {
        return trans_p_arr;
    }
}