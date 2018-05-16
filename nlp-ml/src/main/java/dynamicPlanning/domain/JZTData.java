package dynamicPlanning.domain;

import dynamicPlanning.domain.DesRankData;

import java.util.HashMap;
import java.util.List;

public class JZTData {

    //目的地(单位编号)对应的索引的ID
    HashMap<String,Integer> desIndexMap ;

    //目的地(ID)对应的(单位编号)的Map
    HashMap<Integer,String> desIndexCodeMap;

    //目的地与名称对应的名字
    private HashMap<String,String> desAndNameMap;

    //装车单号对应的目的地list
    private HashMap<String,List<DesRankData>> truckIDAndDestList;

    //目的地Id对应的中文名称
    private HashMap<Integer,String> desIdAndNameMap;

    //每个“单位编号”的纠正后的“提货方式”
    private HashMap<String,Integer> desCodeAreaMap;


    public HashMap<String, String> getDesAndNameMap() {
        return desAndNameMap;
    }

    public void setDesAndNameMap(HashMap<String, String> desAndNameMap) {
        this.desAndNameMap = desAndNameMap;
    }


    public HashMap<String, List<DesRankData>> getTruckIDAndDestList() {
        return truckIDAndDestList;
    }

    public void setTruckIDAndDestList(HashMap<String, List<DesRankData>> truckIDAndDestList) {
        this.truckIDAndDestList = truckIDAndDestList;
    }

    public HashMap<String, Integer> getDesIndexMap() {
        return desIndexMap;
    }

    public void setDesIndexMap(HashMap<String, Integer> desIndexMap) {
        this.desIndexMap = desIndexMap;
    }

    public HashMap<Integer, String> getDesIdAndNameMap() {
        return desIdAndNameMap;
    }

    public void setDesIdAndNameMap(HashMap<Integer, String> desIdAndNameMap) {
        this.desIdAndNameMap = desIdAndNameMap;
    }

    public HashMap<Integer, String> getDesIndexCodeMap() {
        return desIndexCodeMap;
    }

    public void setDesIndexCodeMap(HashMap<Integer, String> desIndexCodeMap) {
        this.desIndexCodeMap = desIndexCodeMap;
    }

    public HashMap<String, Integer> getDesCodeAreaMap() {
        return desCodeAreaMap;
    }

    public void setDesCodeAreaMap(HashMap<String, Integer> desCodeAreaMap) {
        this.desCodeAreaMap = desCodeAreaMap;
    }
}