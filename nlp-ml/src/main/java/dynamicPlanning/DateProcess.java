package dynamicPlanning;


import dynamicPlanning.deal.ClusterDeal;
import dynamicPlanning.domain.DeliveryArea;
import dynamicPlanning.domain.DesRankData;
import dynamicPlanning.domain.JZTData;

import java.util.*;
import java.util.stream.Collectors;

public class DateProcess {
    public static void main(String[] args) {
        String dataPath = "E:\\work\\Join\\one_year_data\\csv";
        String resouresRoot = "D:\\myProject\\ml-nlp-dl-rl\\nlp-ml\\src\\main\\resources\\Jointown\\";
        ReadCsv readCsv = new ReadCsv();
        JZTData jztData = readCsv.readCsv(dataPath);
        HashMap<String, List<DesRankData>> data = jztData.getTruckIDAndDestList();
        System.out.println("总条数 = " + data.size());
        System.out.println("地点总数 = " + jztData.getDesDealData().getDesTotalNum());
        ClusterDeal clusterDeal = new ClusterDeal(data);
        System.out.println("分组得到的组的个数 = " +clusterDeal.getNumCluster());
//        List<HashMap<String, List<Integer>>> splitAndSortData_inner = splitAndSort(0.99, data, 1,jztData);
//        HashMap<String, List<Integer>> trainData_inner = splitAndSortData_inner.get(0);
//        HashMap<String, List<Integer>> testData_inner = splitAndSortData_inner.get(1);
//        ReadWriteTxtUtil.writeTxts2iMap(resouresRoot+"desIndexMap.txt",jztData.getDesIndexMap());
//        ReadWriteTxtUtil.writeTxts2sMap(resouresRoot+"desNameMap.txt",jztData.getDesAndNameMap());
//        ReadWriteTxtUtil.writeTxt(resouresRoot+"train_inner.txt",transData(trainData_inner,jztData.getDesIdAndNameMap()));
//        ReadWriteTxtUtil.writeTxt(resouresRoot+"test_inner.txt",transData(testData_inner,jztData.getDesIdAndNameMap()));
//        ReadWriteTxtUtil.writeTxt(resouresRoot+"one_inner.txt",transData(splitAndSortData_inner.get(3),jztData.getDesIdAndNameMap()));
//        ReadWriteTxtUtil.writeTxt(resouresRoot+"outer_inner.txt",transData(splitAndSortData_inner.get(4),jztData.getDesIdAndNameMap()));


//        HashMap<String,List<Integer>> totalData = splitAndSortData.get(2);
//        List<String> strings = jztData.getDestSList();
//        HashMap<String,String> map = jztData.getDesAndNameMap();
//        HashMap<String,List<String>> moreOneResult = new HashMap<>();
//        HashMap<String,List<String>> oneData = new HashMap<>();
//        totalData.forEach( (k,list) -> {
//            List<String> strings1 = list.stream().map(t -> map.get(strings.get(t))).collect(Collectors.toList());
//
//            if (strings1.size()==1){
//                oneData.put(k,strings1);
//            }else {
//                moreOneResult.put(k,strings1);
//            }
//        });
//
//        ReadWriteTxtUtil.writeTxt(oneTxt,oneData);
//        System.out.println("只含有一个单 = " + oneData.size());
//        ReadWriteTxtUtil.writeTxt(moreOneText,moreOneResult);
//        System.out.println("含有两个单以上 = " + moreOneResult.size());
//
//
//        int destionSize = jztData.getDestSList().size();
//        System.out.println("词典维度 = " +destionSize);
//        ViterModel viterModel = new ViterModel().trainModel(trainData,destionSize);
//        double acc = viterModel.testModel(testData);
//        System.out.println("准确率 = " + acc);


    }

//    /**
//     * 分割并排序
//     *
//     * @param split
//     * @param map
//     * @return
//     */
//    private static List<HashMap<String, List<Integer>>> splitAndSort(double split, HashMap<String, List<DesRankData>> map, int deliveryAreaType,JZTData jztData) {
//        int size = map.size();
//        List<HashMap<String, List<Integer>>> list = new ArrayList<>();
//        double first = size * split;
//        HashMap<String, List<Integer>> firstMap = new HashMap<String, List<Integer>>();
//        HashMap<String, List<Integer>> secondMap = new HashMap<String, List<Integer>>();
//        HashMap<String, List<Integer>> totalMap = new HashMap<String, List<Integer>>();
//        HashMap<String,List<Integer>> oneMap = new HashMap<>();
//        HashMap<String,List<Integer>> outer_more_one_Map = new HashMap<>();
//        HashMap<String,List<Integer>> outer_one_Map = new HashMap<>();
//        HashMap<String,List<DesRankData>> filterData = new HashMap<>();
//
//        int i = 0;
//        for (Map.Entry<String, List<DesRankData>> data : map.entrySet()) {
//            i++;
//            List<DesRankData> desRankDatas = data.getValue();
//            Collections.sort(desRankDatas, Comparator.comparing(DesRankData::getRank));
//            List<DesRankData> desRankDatasFilterWithAreaType = desRankDatas.stream().filter(t -> t.getDeliveryArea() == deliveryAreaType).collect(Collectors.toList());
//
//            //用于排除每车中配送范围是否一致
//            if (desRankDatasFilterWithAreaType.size()<desRankDatas.size() && desRankDatasFilterWithAreaType.size()>0 &&
//                    (desRankDatasFilterWithAreaType.size()>1 && desRankDatas.size()-desRankDatasFilterWithAreaType.size()>1) ){
//                System.out.println("同一单中配送地区不同的单号是 = " +data.getKey() + " ；未过滤前的配送地点配送数 = " +desRankDatas.size() +" ；过滤后'市内配送'的配送地点数 = " +desRankDatasFilterWithAreaType.size());
//                filterData.put(data.getKey(),desRankDatas);
//            }
//
//            List<Integer> sortList = desRankDatasFilterWithAreaType.stream().map(t -> t.getDes()).distinct().collect(Collectors.toList());
//            if (sortList.size() > 1) {
//                if (i < first) {
//                    firstMap.put(data.getKey(), sortList);
//                } else {
//                    secondMap.put(data.getKey(), sortList);
//                }
//            } else if(sortList.size()>0){
//                  oneMap.put(data.getKey(),sortList);
//            }else {
//                List<Integer> outer_sortList=desRankDatas.stream().filter(t -> t.getDeliveryArea() == 2).map(t -> t.getDes()).distinct().collect(Collectors.toList());
//                if (outer_sortList.size()>1){
//                    outer_more_one_Map.put(data.getKey(),outer_sortList);
//                }else {
//                    outer_one_Map.put(data.getKey(),outer_sortList);
//                }
//
//
//            }
//
//        }
//        totalMap.putAll(firstMap);
//        totalMap.putAll(secondMap);
//        totalMap.putAll(oneMap);
//        list.add(0, firstMap);
//        list.add(1, secondMap);
//        list.add(2, totalMap);
//        list.add(3,oneMap);
//        list.add(4,outer_one_Map);
//        list.add(5,outer_more_one_Map);
//        int outer_size = outer_more_one_Map.size()+outer_one_Map.size();
//        System.out.println("市外配送的单子共有 = " +(outer_size) + " ，所占的总体比例 = " +(outer_size/(map.size()+0.0)));
//        System.out.println("市外配送单子只有一个地方的单子 = " + outer_one_Map.size() +" 所占比例 = " +outer_one_Map.size()/(outer_size+0.0));
//        System.out.println("每车只有一个地方的单数 = " + oneMap.size());
//        System.out.println("每车只有一个地方的所占比例 = " + (oneMap.size()/(totalMap.size()+0.0)));
//        System.out.println("‘" + DeliveryArea.getDeliveryAreaName(deliveryAreaType) +"’的总数 = " +totalMap.size() + ",所占的总体比例 = " + totalMap.size()/(map.size()+0.0));
//        WriteExcel.writeExcelData(filterData,"D:\\myProject\\ml-nlp-dl-rl\\nlp-ml\\src\\main\\resources\\Jointown\\differentArea.xls",jztData.getDesIndexCodeMap(),jztData.getDesIdAndNameMap());
//        map.clear();
//        return list;
//    }


    /**
     * 获得每组的对应的地点数据
     * @param data
     * @param desNameAndId
     * @return
     */
    private static HashMap<String,List<String>> transData(HashMap<String,List<Integer>> data,HashMap<Integer,String> desNameAndId){
        HashMap<String,List<String>> newData =new HashMap<>();
        for (Map.Entry<String,List<Integer>> datamap : data.entrySet()){
            List<String> desNames = datamap.getValue().stream().map(t -> desNameAndId.get(t)).collect(Collectors.toList());
            newData.put(datamap.getKey(),desNames);

        }

        return newData;
    }




} 