package dynamicPlanning.domain;

/**
 * 目的地和装车顺序
 */
public class DesRankData {
    private int des;
    private int rank;

    public DesRankData(int des,int rank){
        this.des = des;
        this.rank = rank;

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



    /**
     * 判断是两者是否相同
     * @param other
     * @return
     */
    public boolean isEqual(DesRankData other){
        if (des==other.des && rank == other.rank){
            return true;
        }else {
            return false;
        }
    }
}