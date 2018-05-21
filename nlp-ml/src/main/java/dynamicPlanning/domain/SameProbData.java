package dynamicPlanning.domain;

import java.util.ArrayList;
import java.util.List;

/**
 * \* Created with IntelliJ IDEA.
 * \* User: Administrator
 * \* Date: 2018/5/17 0017
 * \* Time: 下午 15:15
 * \* Description:
 * 对相同的概率的状态进行记录
 * \
 */
public class SameProbData {
    //相同概率情况下的序列
   private List<List<Integer>> same_seq = new ArrayList<>();
   //相同概率下的概率值
   private List<Double> same_pro = new ArrayList<>();

   //相同值的下班序列
   private int same_index = -1;
   //相同概率当前的当前最大的情况
   private double same_maxPro = -1.0;

   public SameProbData(){

   }

    /**
     * 更新存储相同概率的序列
     * @param last_seq
     * @param prob
     */
   public void upDate(List<Integer> last_seq,double prob){
       if (prob>=same_maxPro){
           same_maxPro = prob;
           same_index += 1;
           same_seq.add(same_index,last_seq);
           same_pro.add(same_index,prob);
       }

   }

    /**
     * 获得的概率最大的相似序列
     * @return
     */
   public List<List<Integer>> getSameSeq(){
       if (same_index>-1){
           return same_seq.subList(same_pro.indexOf(same_maxPro),same_seq.size());
       }else return null;
   }

    /**
     * 获得最大的概率值
     * @return
     */
   public double getSameMaxPro(){
       return same_maxPro;
   }

}