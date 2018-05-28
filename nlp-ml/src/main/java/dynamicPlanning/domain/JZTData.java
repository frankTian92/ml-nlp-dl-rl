package dynamicPlanning.domain;

import dynamicPlanning.deal.DesDealData;
import dynamicPlanning.domain.DesRankData;

import java.util.HashMap;
import java.util.List;

public class JZTData {

    //目的地(单位编号)对应的索引的ID
    private DesDealData desDealData;

    //装车单号对应的目的地list
    private HashMap<String,List<DesRankData>> truckIDAndDestList;

    public HashMap<String, List<DesRankData>> getTruckIDAndDestList() {
        return truckIDAndDestList;
    }

    public void setTruckIDAndDestList(HashMap<String, List<DesRankData>> truckIDAndDestList) {
        this.truckIDAndDestList = truckIDAndDestList;
    }

    public DesDealData getDesDealData() {
        return desDealData;
    }

    public void setDesDealData(DesDealData desDealData) {
        this.desDealData = desDealData;
    }
}