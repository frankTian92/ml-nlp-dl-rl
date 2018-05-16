package dynamicPlanning.dataCorrection;

import dynamicPlanning.Constant;
import dynamicPlanning.domain.DeliveryArea;

import java.util.Calendar;
import java.util.Date;


/**
 * \* Created with IntelliJ IDEA.
 * \* User: Administrator
 * \* Date: 2018/5/14 0014
 * \* Time: 下午 15:32
 * \* Description:
 * \用于表示“市内”和“市外”每个地点的统计量，用于每个地点提货方式纠错
 */
public class AreaData {
    //配送地址唯一标识
    private int deliveryUniqueIdentif;

    //该单位属于市内提货的个数
    private int innerCount;

    //该单位属于市外提货的个数
    private int outerCount;

    //相对新的世界
    private Date thresholdTime = initDate(3);


    public AreaData(Integer deliveryUniqueIdentif) {
        this.deliveryUniqueIdentif = deliveryUniqueIdentif;
        this.innerCount = 0;
        this.outerCount = 0;
    }

    /**
     * 更新该提货方式的个数
     *
     * @param deliveryString
     */
    public void update(String deliveryString,Date date) {
        if (deliveryString.equals(Constant.INNER_CITY_DELIVERY)) {
            this.innerCount += 1;
            //根据“配送时间”，对距离近的“配送方式”做加权处理
            if (date.after(thresholdTime)){
                this.innerCount+=1;
            }
        } else if (deliveryString.equals(Constant.OUTER_CITY_DELIVERY)) {
            this.outerCount += 1;
            //根据“配送时间”，对距离近的“配送方式”做加权处理
            if (date.after(thresholdTime)){
                this.outerCount+=1;
            }
        }


    }

    /**
     * 获得最终的提货方式编号
     *
     * @return
     */
    public int getDeliveryArea() {
        if (this.innerCount > this.outerCount) {
            return DeliveryArea.INNER_CITY_DELIVERY.index();
        } else return DeliveryArea.OUTER_CITY_DELIVERY.index();
    }

    /**
     * 获取“配送地址唯一标识”的“提货类型”，主要分为三种，"市内配送、市外配送、即参与市内配送也参与市外配送"
     * @return
     */
    public int getDeliveryAreaType(){
        if (this.innerCount==0 && this.outerCount>0){
            return DeliveryArea.OUTER_CITY_DELIVERY.index();
        }else if(this.innerCount>0 && this.outerCount==0){
            return DeliveryArea.INNER_CITY_DELIVERY.index();
        }else {
            return DeliveryArea.MIXTURE_CITY_DELIVERY.index();
        }
    }

    /**
     * 获得前三个月的日期
     * @param beforeMonth
     * @return
     */
    private static Date initDate(int beforeMonth){
        Date d_now  = new Date();
        Date d_before = new Date();
        Calendar calendar = Calendar.getInstance();
        calendar.setTime(d_now);
        calendar.add(Calendar.MONTH,-beforeMonth);
        d_before = calendar.getTime();
        return d_before;

    }




}