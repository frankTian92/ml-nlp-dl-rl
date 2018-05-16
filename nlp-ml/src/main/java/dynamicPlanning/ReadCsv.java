package dynamicPlanning;

import dynamicPlanning.dataCorrection.DistributionAreaCorrection;

import dynamicPlanning.domain.DeliveryArea;
import dynamicPlanning.domain.DesRankData;
import dynamicPlanning.domain.JZTData;

import java.io.BufferedReader;
import java.io.File;
import java.io.FileReader;
import java.util.*;

/**
 * /**
 * \* Created with IntelliJ IDEA.
 * \* User: Administrator
 * \* Date: 2018/5/9 0009
 * \* Time: 下午 15:21
 * \* Description: 读取excel
 * \
 */
public class ReadCsv {
    JZTData jztDate = new JZTData();

    //目的地与名称对应的名字
    private HashMap<String, String> desAndNameMap = new HashMap();

    //目的地对应的索引的ID
    private HashMap<String, Integer> desIndexMap = new HashMap<String, Integer>();

    //装车单号对应的目的地list
    private HashMap<String, List<DesRankData>> truckIDAndDestList = new HashMap<String, List<DesRankData>>();

    //目的地Id对应的中文名称
    private HashMap<Integer, String> desIdAndNameMap = new HashMap<>();

    //对每个“单位编号”的“提货方式”进行纠正
    private DistributionAreaCorrection distributionAreaCorrection = new DistributionAreaCorrection();

    public JZTData readCsv(String filePath) {

       List<String> files = getFiles(filePath);
       for (String fileName:files){
           int cols = 0;
           try {
               BufferedReader reader = new BufferedReader(new FileReader(fileName));
               reader.readLine();//第一行信息，为标题信息，不用,如果需要，注释掉
               String line = null;
               while((line=reader.readLine())!=null){
                   CsvValue csvValue = new CsvValue();
                   String item[] = line.split(",");//CSV格式文件为逗号分隔符文件，这里根据逗号切分
                   for (int i = 0;i<item.length;i++){
                       csvValue.updata(i,item[i]);
                   }
                   csvValue.statistics();
                   cols+=1;
               }
           } catch (Exception e) {
               e.printStackTrace();
           }
           System.out.println(fileName + " 中数据量 = " +cols);
       }



        jztDate.setDesAndNameMap(desAndNameMap);
        jztDate.setDesIndexMap(desIndexMap);
        jztDate.setDesIdAndNameMap(desIdAndNameMap);
        HashMap<String, Integer> desAreaMap = distributionAreaCorrection.getDesAreaMap();
        jztDate.setDesCodeAreaMap(desAreaMap);

        HashMap<Integer, String> desIndexCodeMap = new HashMap<>();
        for (Map.Entry<String, Integer> desIndexM : desIndexMap.entrySet()) {
            desIndexCodeMap.put(desIndexM.getValue(), desIndexM.getKey());
        }
        jztDate.setDesIndexCodeMap(desIndexCodeMap);

        //对数据的“提货方式”进行修正
        HashMap<String, List<DesRankData>> new_truckIDAndDestList = new HashMap<>();
        for (Map.Entry<String, List<DesRankData>> desRankData : truckIDAndDestList.entrySet()) {
            List<DesRankData> desRankDataList = desRankData.getValue();
            List<DesRankData> newData = new ArrayList<>();
            for (DesRankData desRankData1 : desRankDataList) {
//                int old_area = desRankData1.getDeliveryArea();
                int desCode = desRankData1.getDes();
                int new_area = desAreaMap.get(desIndexCodeMap.get(desCode));
//                if (old_area != new_area) {
//                    System.out.println(desIndexCodeMap.get(desCode));
//                }
                newData.add(new DesRankData(desCode, desRankData1.getRank(), new_area));
            }
            new_truckIDAndDestList.put(desRankData.getKey(), newData);
//            desRankDataList.stream().forEach(t -> t.setDeliveryArea(desAreaMap.get(desIndexCodeMap.get(t.getDes()))));
        }

        jztDate.setTruckIDAndDestList(new_truckIDAndDestList);


        return jztDate;
    }

    public class CsvValue {
        //装车单号
        private String truckId = null;
        //装车顺序
        private int rank = 0;
        //单位编号
        private String desString = null;
        //单位名称
        private String desName = null;
        //提货方式
        private String delivery = null;
        //提货方式id
        private int deliveryNum = 0;

        private Date date = null;

        //配送地址名称
        private String location = null;


        public CsvValue() {
        }

        public void updata(int n, String v) {

            if (n == 1) {
                this.date = new Date(v);
            }
            if (n == 2) {
                this.truckId = v;
            }

            if ((n == 4)) {
                this.desString = v;
            }

            if (n == 5) {
                if (!v.isEmpty() && v.length() > 1) {
                    this.desName = v;
                }
            }
            if (n == 6) {
                if (!v.isEmpty() && v.length() > 1) {
                    this.location = v;
                }
            }

            if (n == 7) {
                this.rank = Double.valueOf(v).intValue();
            }


            if (n == 8) {
                this.delivery = v;
                this.deliveryNum = DeliveryArea.getDeliveryAreaNum(delivery);
                distributionAreaCorrection.update(desString, delivery,desName, location, date);
            }



        }

        public void statistics() {
            //增加地点Id与其对应的名称
            if ((desAndNameMap.isEmpty() || !desAndNameMap.containsKey(desString)) && desName != null) {
                desAndNameMap.put(desString, desName);
            }

            //构建站点列表和对应的map表
            if (desIndexMap.isEmpty()) {
                desIndexMap.put(desString, 0);
                desIdAndNameMap.put(0, desName);
            } else if (!desIndexMap.containsKey(desString)) {
                int index = desIndexMap.size();
                desIndexMap.put(desString, index);
                desIdAndNameMap.put(index, desName);
            }


            //组装每趟车装车记录
            List<DesRankData> desRankDataSet = new ArrayList<>();
            if (truckIDAndDestList != null && truckIDAndDestList.size() > 0 && truckIDAndDestList.containsKey(truckId)) {
                desRankDataSet = truckIDAndDestList.get(truckId);
                boolean same = false;
                for (DesRankData desRankD : desRankDataSet) {
                    int des = desRankD.getDes();
                    int ran = desRankD.getRank();
                    int delivery_num = desRankD.getDeliveryArea();
                    if (des == desIndexMap.get(desString).intValue() && ran == rank && deliveryNum == delivery_num) {
                        same = true;
                        break;
                    }
                }
                if (!same) {
                    DesRankData desRankData = new DesRankData(desIndexMap.get(desString).intValue(), rank, deliveryNum);
                    desRankDataSet.add(desRankData);
                }


            } else {
                DesRankData desRankData = new DesRankData(desIndexMap.get(desString).intValue(), rank, deliveryNum);
                desRankDataSet.add(desRankData);
            }
            truckIDAndDestList.put(truckId, desRankDataSet);
        }

    }

    /**
     * 获取指定目录下的文件夹名称
     * @param path
     * @return
     */
    public static ArrayList<String> getFiles(String path) {
        ArrayList<String> files = new ArrayList<String>();
        File file = new File(path);
        File[] tempList = file.listFiles();

        for (int i = 0; i < tempList.length; i++) {
            if (tempList[i].isFile()) {
                System.out.println("文件：" + tempList[i]);
                files.add(tempList[i].toString());
            }
            if (tempList[i].isDirectory()) {
                System.out.println("文件夹：" + tempList[i]);
            }
        }
        return files;
    }


}
