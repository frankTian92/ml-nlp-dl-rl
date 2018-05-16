package dynamicPlanning.domain;

/**
 * 目的地和装车顺序
 */
public class DesRankData {
    private int des;
    private int rank;
    private int deliveryArea;


    public DesRankData(int des,int rank,int deliveryArea){
        this.des = des;
        this.rank = rank;
        this.deliveryArea = deliveryArea;
    }

    public int getDes() {
        return des;
    }

    public void setDes(int des) {
        this.des = des;
    }

    public int getRank() {
        return rank;
    }

    public void setRank(int rank) {
        this.rank = rank;
    }

    public int getDeliveryArea() {
        return deliveryArea;
    }

    public void setDeliveryArea(int deliveryArea) {
        this.deliveryArea = deliveryArea;
    }
}