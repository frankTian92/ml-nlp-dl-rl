package Util;


import com.google.common.net.InetAddresses;
import org.elasticsearch.action.search.SearchRequestBuilder;
import org.elasticsearch.action.search.SearchResponse;
import org.elasticsearch.action.search.SearchType;
import org.elasticsearch.client.transport.TransportClient;
import org.elasticsearch.common.settings.Settings;
import org.elasticsearch.common.transport.InetSocketTransportAddress;
import org.elasticsearch.common.transport.TransportAddress;
import org.elasticsearch.common.unit.TimeValue;
import org.elasticsearch.index.query.BoolQueryBuilder;
import org.elasticsearch.index.query.QueryBuilders;
import org.elasticsearch.index.query.QueryStringQueryBuilder;
import org.elasticsearch.search.builder.SearchSourceBuilder;
import org.elasticsearch.transport.client.PreBuiltTransportClient;

import java.util.HashMap;
import java.util.Map;


/**
 * es工具类
 */
public class EsUtil {
//
//    private static Logger logger = Logger.getLogger(EsUtil.class);

    /**
     * 初始化连接es
     *
     * @param esClusterName 集群名
     * @param esServerIps   集群Ip列表，用逗号分隔的字符串
     * @param esServerPort  集群端口
     * @return
     */
    public static TransportClient connectEsClient(String esClusterName, String esServerIps, Integer esServerPort) {
        if (esServerIps == null || esServerIps.trim().isEmpty()) {
            System.out.println("Es的Ip地址为空！！！");
            return null;
        }
        System.out.println("Es配置：{" +
                "esClusterName : " + esClusterName + " ;" +
                "esServerIps : " + esServerIps + " ;" +
                "esServerPort : " + esServerPort + " ；}");

        Settings settings = Settings.builder()
                .put("cluster.name", esClusterName).build();

        String[] esIps = esServerIps.split(",");
        TransportClient client = new PreBuiltTransportClient(settings);
        for (String esIp : esIps) {
            TransportAddress transportAddress = new InetSocketTransportAddress(InetAddresses.forString(esIp), esServerPort);
            client.addTransportAddress(transportAddress);
        }

        System.out.println("Es链接成功！！！");
        return client;

    }

    /**
     * 根据用户的Id查询数据
     *
     * @param client  es集群
     * @param esIndex es中的索引，相当于sql数据库中的“库”
     * @param esType  es中的表类型，相当于sql数据库中的“表”
     * @param userId  es中的对应字段值
     * @return
     */
    public static SearchResponse queryUserData(TransportClient client, String esIndex, String esType, int userId) {
        SearchRequestBuilder requestBuilder = client.prepareSearch(esIndex);
        SearchSourceBuilder sourceBuilder = SearchSourceBuilder.searchSource();
        requestBuilder.setSource(sourceBuilder);
        requestBuilder.setTypes(esType).setSearchType(SearchType.DFS_QUERY_THEN_FETCH)
                .setScroll(TimeValue.timeValueMinutes(2)).setSize(5000);
        BoolQueryBuilder boolQueryBuilder = QueryBuilders.boolQuery();

        //时间范围查询
//        RangeQueryBuilder pubTimeRangQuery = QueryBuilders.rangeQuery("pubTime");
//        pubTimeRangQuery.gte(startTimeStr);
//        pubTimeRangQuery.timeZone("Asia/Shanghai");
//        boolQueryBuilder.must(pubTimeRangQuery);

        boolQueryBuilder.must(QueryBuilders.termQuery("userId", userId));
        requestBuilder.setQuery(boolQueryBuilder);
        SearchResponse searchResponse = requestBuilder.execute().actionGet();
        return searchResponse;
    }

    /**
     * 根据正则表达式查询es中的数据
     *
     * @param client      es集群
     * @param esIndex     es中的索引，相当于sql数据库中的“库”
     * @param esType      es中的表类型，相当于sql数据库中的“表”
     * @param queryString 正则表达式
     * @param isOR        正则表达式中，词组直接的关系（false——表示词组之间是“且”的关系）
     *                    例：“且”的关系——("质量" AND "裂缝" AND "漏水" AND "交房时间")
     *                    “或”的关系 —— "裂缝" OR "漏水" OR "交房时间" OR "质量"
     * @return
     */
    public static SearchResponse queryDcData(TransportClient client, String esIndex, String esType, String queryString, boolean isOR) {
        SearchRequestBuilder requestBuilder = client.prepareSearch(esIndex);
        SearchSourceBuilder sourceBuilder = SearchSourceBuilder.searchSource();
        requestBuilder.setSource(sourceBuilder);
        requestBuilder.setTypes(esType).setSearchType(SearchType.DFS_QUERY_THEN_FETCH)
                .setScroll(TimeValue.timeValueMinutes(8)).setSize(5000);
        BoolQueryBuilder boolQueryBuilder = QueryBuilders.boolQuery();

        System.out.println("查询语句 = " + queryString);
        //增加关键词的“And”和“OR”的关系，对标题、内容、评论、网站来源进行分别匹配来获取数据；
        QueryStringQueryBuilder queryStringQueryBuilder = new QueryStringQueryBuilder(queryString);
        Map<String, Float> fieldsMap = new HashMap<>();
        if (!isOR) {
            fieldsMap.put("from", 1f);
        }
        fieldsMap.put("title", 1f);
        fieldsMap.put("content", 1f);
        fieldsMap.put("comment", 1f);

        if (isOR) {
            queryStringQueryBuilder.minimumShouldMatch("40%");
        }
        queryStringQueryBuilder.fields(fieldsMap);
        boolQueryBuilder.filter(queryStringQueryBuilder);
        requestBuilder.setQuery(boolQueryBuilder);
        SearchResponse searchResponse = requestBuilder.execute().actionGet();
        return searchResponse;
    }


} 