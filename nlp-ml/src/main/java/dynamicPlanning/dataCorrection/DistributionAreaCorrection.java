package dynamicPlanning.dataCorrection;

import java.util.Date;
import java.util.HashMap;
import java.util.Map;

/**
 * \* Created with IntelliJ IDEA.
 * \* User: Administrator
 * \* Date: 2018/5/14 0014
 * \* Time: 下午 15:26
 * \* Description:
 * \对“单位编号”的“提货方式”的修正，该“提货方式”主要有两种“市内配送”和“市外配送”
 */
public class DistributionAreaCorrection {

    /**
     * 配送地点集合
     */
    private HashMap<String,AreaData> desCodeMap = new HashMap<>();

    public DistributionAreaCorrection(){
    }

    /**
     * 更新单位编号及其对应的提货方式统计个数
     * @param desCode
     * @param deliveryString
     */
    public void update(String desCode, String deliveryString,String desName, String location, Date date){
        if (desCodeMap.isEmpty() || !desCodeMap.containsKey(desCode)){
//            AreaData areaData = new AreaData(desCode);
//            areaData.update(deliveryString,date);
//            desCodeMap.put(desCode,areaData);
        }else if(desCodeMap.containsKey(desCode)){
//            AreaData areaData = desCodeMap.get(desCode);
//            areaData.update(deliveryString,desName,location,date);
//            desCodeMap.put(desCode,areaData);
        }
    }


    /**
     * 获取每个“单位编号”的纠正后的“提货方式”
     * @return
     */
    public HashMap<String,Integer> getDesAreaMap(){
        HashMap<String,Integer> desCodeAndAreaIndexMap = new HashMap<>();
        for (Map.Entry<String,AreaData> codeArea:desCodeMap.entrySet()){
            desCodeAndAreaIndexMap.put(codeArea.getKey(),codeArea.getValue().getDeliveryArea());
        }
        return desCodeAndAreaIndexMap;
    }
}