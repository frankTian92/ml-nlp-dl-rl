package eventTrack;

import Util.EsUtil;
import Util.ExcelUtil;
import org.elasticsearch.action.search.SearchResponse;
import org.elasticsearch.client.transport.TransportClient;
import org.elasticsearch.common.unit.TimeValue;
import org.elasticsearch.search.SearchHit;

import java.util.ArrayList;
import java.util.List;
import java.util.Map;

/**
 * 根据关键词从es中获取数据
 */

public class ObtainDataFormES {

    private static String esClusterName = "yuqing";
    private static String esServerIps = "192.168.1.194,192.168.1.195,192.168.1.196";
    private static Integer esServerPort = 9300;
    private static String esIndex = "yuqing";
    private static String esType = "dc_data";

    public static void main(String[] args) {
        //查询语句

         String qureyString = "(\"海底捞\" AND \"后厨\" AND \"卫生\")";
         String savaPath = "C:\\Users\\Administrator\\Desktop\\dc_data.xls";
        List<DcData> dcDatas = queryDcData(qureyString);
        saveExcle(dcDatas,3,savaPath);
    }


    private static List<DcData> queryDcData(String qureyString) {
        Long beginTime_AND_OR = System.currentTimeMillis();
        TransportClient client = EsUtil.connectEsClient(esClusterName, esServerIps, esServerPort);
        SearchResponse searchResponse = EsUtil.queryDcData(client,esIndex,esType,qureyString,false);
        int dcDataSum  = searchResponse.getHits().getHits().length;
        Long dcDataTotal = searchResponse.getHits().getTotalHits();
        System.out.println("一共有" + dcDataTotal + "条dc_data数据记录需要拿到");
        List<DcData> dcDatas = new ArrayList<>();

        for (SearchHit searchHit : searchResponse.getHits()){
            DcData  dcData = new DcData();
            String id  = searchHit.getId();
            Map<String,Object> stringObjectMap = searchHit.getSourceAsMap();
            dcData.setId(id);
            dcData.setContent((String) stringObjectMap.get("content"));
            dcData.setTitle((String) stringObjectMap.get("title"));
            dcDatas.add(dcData);

        }

        System.out.println("已经有" + dcDataSum + "条dc_data数据");

        while (dcDataSum<dcDataTotal){
            searchResponse = client.prepareSearchScroll(searchResponse.getScrollId())
                    .setScroll(TimeValue.timeValueMillis(8)).execute().actionGet();
            dcDataSum+= searchResponse.getHits().getHits().length;
            System.out.println("已经有" + dcDataSum + "条dc_data数据");
            for (SearchHit searchHit : searchResponse.getHits()){
                DcData  dcData = new DcData();
                String id  = searchHit.getId();
                Map<String,Object> stringObjectMap = searchHit.getSourceAsMap();
                dcData.setId(id);
                dcData.setContent((String) stringObjectMap.get("content"));
                dcData.setTitle((String) stringObjectMap.get("title"));
                dcDatas.add(dcData);

            }
        }
        Long endTime_AND_OR = System.currentTimeMillis();
        System.out.println("获取信息所需时间:" + (endTime_AND_OR - beginTime_AND_OR) + "毫秒");
        return dcDatas;
    }


    /**
     * 数据存储
     * @param dcDatas
     * @param cloumCount
     * @param savePath
     */
    private static void saveExcle(List<DcData> dcDatas,int cloumCount,String savePath){
        ExcelUtil excelUtil = new ExcelUtil();
        excelUtil.writeExcelData(dcDatas, cloumCount,savePath);
    }





} 