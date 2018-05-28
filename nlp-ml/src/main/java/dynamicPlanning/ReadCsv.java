package dynamicPlanning;

import dynamicPlanning.dataCorrection.DistributionAreaCorrection;

import dynamicPlanning.deal.DesDealData;
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

    //装车单号对应的目的地list
    private HashMap<String, List<DesRankData>> truckIDAndDestList = new HashMap<String, List<DesRankData>>();


    //配送地点处理的数据
    private DesDealData desDealData = new DesDealData();


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



        jztDate.setTruckIDAndDestList(truckIDAndDestList);
        jztDate.setDesDealData(desDealData);

        return jztDate;
    }

    public class CsvValue {
        //装车单号
        private String truckId = null;
        //装车顺序
        private int rank = 0;
        //单位编号
        private String desNum = null;
        //单位名称
        private String desName = null;


        //配送地址内码
        private String desCode = null;



        public CsvValue() {
        }

        public void updata(int n, String v) {

            if (n == 2) {
                this.truckId = v;
            }

            if ((n == 4)) {
                this.desNum = v;
            }

            if (n == 5) {
                if (!v.isEmpty() && v.length() > 1) {
                    this.desName = v;
                }
            }


            if (n == 7) {
                this.rank = Double.valueOf(v).intValue();
            }


            if (n == 10){
                this.desCode = v;

            }



        }

        public void statistics() {
            desDealData.update(desNum,desName,desCode);
            //组装每趟车装车记录
            List<DesRankData> new_desRankDataSet = new ArrayList<>();
            DesRankData desRankData = new DesRankData(desDealData.getdesIndex(desNum,desCode), rank);
            if (truckIDAndDestList != null && truckIDAndDestList.size() > 0 && truckIDAndDestList.containsKey(truckId)) {
                List<DesRankData> old_desRankDataSet = truckIDAndDestList.get(truckId);
                new_desRankDataSet.addAll(old_desRankDataSet);

                for (DesRankData desRankD : old_desRankDataSet) {
                    if (!desRankD.isEqual(desRankData)){
                        new_desRankDataSet.add(desRankData);
                    }
                }
            } else {
                new_desRankDataSet.add(desRankData);
            }

            truckIDAndDestList.put(truckId, new_desRankDataSet);

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
