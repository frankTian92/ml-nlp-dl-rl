package cluster;

import java.util.HashSet;

/**
 * Created by stormor on 2017/11/9.
 * 存储文章id及其词集
 * 文章出现某个词就显示记为1
 */
public class AtData {

    private String id ;

    //词的索引号集
    private HashSet wordsIndex;

    //词集的模
    private double dataMode;

    public AtData( String id,HashSet<Integer> wordsIndex){
        this.wordsIndex = wordsIndex;
        this.id = id;
        this.dataMode = Math.sqrt(wordsIndex.size());
    }

    private String getId() {
        return id;
    }

    public void setId(String id) {
        this.id = id;
    }

    public HashSet getWordsIndex() {
        return wordsIndex;
    }

    public void setWordsIndex(HashSet wordsIndex) {
        this.wordsIndex = wordsIndex;
        this.dataMode = Math.sqrt(wordsIndex.size());
    }

    public double getDataMode() {
        return dataMode;
    }


}
