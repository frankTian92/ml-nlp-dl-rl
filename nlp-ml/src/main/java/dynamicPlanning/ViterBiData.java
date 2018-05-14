package dynamicPlanning;

/**
 * 维特比算法计算结果存储
 */
public class ViterBiData {
    private double probility;
    private int[] seqRank;

    public double getProbility() {
        return probility;
    }

    public void setProbility(double probility) {
        this.probility = probility;
    }

    public int[] getSeqRank() {
        return seqRank;
    }

    public void setSeqRank(int[] seqRank) {
        this.seqRank = seqRank;
    }
}