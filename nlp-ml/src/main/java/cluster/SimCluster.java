package cluster;

import java.util.ArrayList;
import java.util.HashSet;
import java.util.List;

/**
 * Created by stormor on 2017/11/8.
 * 基于文章相似度进行聚类
 */
public class SimCluster {

    public static void main(String[] args) {
        //readAaticl
        HashSet<Integer> integers = new HashSet<Integer>();
        integers.add(23);
        integers.add(34);
        AtData atData = new AtData("123",integers);
        List<AtData> atDataList = new ArrayList<AtData>();
        atDataList.add(atData);
        List<AtData> atDataListCopy = atDataList;
        atDataListCopy.get(0).setId("234");


    }


}
