package dynamicPlanning;

import javax.swing.event.ListDataEvent;
import java.util.ArrayList;
import java.util.List;

/**
 * 维特比算法计算结果存储
 */
public class ViterBiData {
    private double probility;
    private List<List<Integer>> seqRankList = new ArrayList<>();

    public double getProbility() {
        return probility;
    }

    public void setProbility(double probility) {
        this.probility = probility;
    }

    public List<Integer> getFirstSeqRank() {
        return seqRankList.get(0);
    }

    public void setSeqRankList(List<List<Integer>> seqRankList) {
        this.seqRankList = seqRankList;
    }

    public void addSeq(List<Integer> seqRank){
        seqRankList.add(seqRank);
    }

    public List<List<Integer>> getSeqRankList() {
        return seqRankList;
    }


    public int getSameProbNum() {
        return seqRankList.size();
    }
}