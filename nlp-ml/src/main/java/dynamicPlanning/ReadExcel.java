package dynamicPlanning;

import dynamicPlanning.dataCorrection.DistributionAreaCorrection;

import org.apache.poi.openxml4j.opc.OPCPackage;
import org.apache.poi.xssf.eventusermodel.XSSFReader;
import org.apache.poi.xssf.model.SharedStringsTable;

import org.apache.poi.xssf.usermodel.XSSFRichTextString;
import org.xml.sax.*;
import org.xml.sax.helpers.DefaultHandler;
import org.xml.sax.helpers.XMLReaderFactory;

import java.io.File;
import java.io.InputStream;
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
public class ReadExcel {

    public JZTData readXls(String fileName) {

        JZTData jztDate = new JZTData();

        //目的地与名称对应的名字
        HashMap<String,String> desAndNameMap = new HashMap();

        //目的地对应的索引的ID
        HashMap<String, Integer> desIndexMap = new HashMap<String, Integer>();

        //装车单号对应的目的地list
        HashMap<String, List<DesRankData>> truckIDAndDestList = new HashMap<String, List<DesRankData>>();

        //目的地Id对应的中文名称
        HashMap<Integer,String> desIdAndNameMap = new HashMap<>();

        //对每个“单位编号”的“提货方式”进行纠正
        DistributionAreaCorrection distributionAreaCorrection = new DistributionAreaCorrection();

        try {
            OPCPackage pkg = OPCPackage.open(fileName);
            XSSFReader r = new XSSFReader( pkg );
            SharedStringsTable sst = r.getSharedStringsTable();

            XMLReader parser = fetchSheetParser(sst);

            Iterator<InputStream> sheets = r.getSheetsData();
            while(sheets.hasNext()) {
                System.out.println("Processing new sheet:\n");
                InputStream sheet = sheets.next();
                InputSource sheetSource = new InputSource(sheet);
                parser.parse(sheetSource);
                sheet.close();
                System.out.println("");
            }



//            FileInputStream input = new FileInputStream(fileName);

//            HSSFWorkbook work = new HSSFWorkbook(input);// 得到这个excel表格对象2003版
            //2007版excle
//            XSSFWorkbook work = new XSSFWorkbook(input);
//            int sheets =  work.getNumberOfSheets();
//            for (int sheetNum=0;sheetNum<sheets;sheetNum++){
//                //得到每一个个sheet
////                HSSFSheet sheet = work.getSheetAt(sheetNum);// 得到这个excel表格对象2003版
//                XSSFSheet sheet = work.getSheetAt(sheetNum);
//                int rowNo = sheet.getLastRowNum();
////                HSSFRow trow = sheet.getRow(0);// 得到这个excel表格对象2003版
//                XSSFRow trow = sheet.getRow(0);
//                int colNum = trow.getLastCellNum();
//                List<String> colName = new ArrayList<String>();
//                for (int i = 0; i < colNum; i++) {
//                    XSSFCell cell = trow.getCell((short) i);
//                    if (!cell.toString().equals("")) {
//                        colName.add(cell.toString());
//                    }
//                }
//                //得到行数
//                for (int i = 1; i <= rowNo; i++) {
//                    XSSFRow row = sheet.getRow(i);
//
//                    Date date =null;
//
//                    //装车单号
//                    String truckId = null;
//                    //装车顺序
//                    int rank = 0;
//                    //单位编号
//                    String desString = null;
//                    //单位名称
//                    String desName = null;
//                    //提货方式
//                    String delivery = null;
//                    //提货方式id
//                    int deliveryNum = 0;
//
//                    //配送地址名称
//                    String location = null;
//
//                    for (int n = 0; n < colNum; n++) {
//                        XSSFCell c = row.getCell((short) n);
//                        if (n==1){
//                            date = c.getDateCellValue();
//                        }
//                        if (n == 2) {
//                            truckId = c.getStringCellValue();
//                        }
//
//                        if ((n == 4)) {
//                            desString = c.getStringCellValue();
//                        }
//
//                        if (n == 5) {
//                            if (!c.getStringCellValue().isEmpty() && c.getStringCellValue().length() > 1) {
//                                desName = c.getStringCellValue();
//                            }
//                        }
//
//                        if (n == 9) {
//                            rank = Double.valueOf(c.getNumericCellValue()).intValue();
//                        }
//
//
//                        if(n==10){
//                            delivery = c.getStringCellValue();
//                            deliveryNum  = DeliveryArea.getDeliveryAreaNum(delivery);
//                            distributionAreaCorrection.update(desString,desName,delivery,location,date);
//                        }
//
//                        if (n==13){
//                            if (!c.getStringCellValue().isEmpty() && c.getStringCellValue().length() > 1){
//                                location = c.getStringCellValue();
//                            }
//                        }
//
//                    }
//
//                    //增加地点Id与其对应的名称
//                    if ((desAndNameMap.isEmpty() || !desAndNameMap.containsKey(desString)) && desName != null) {
//                        desAndNameMap.put(desString, desName);
//                    }
//
//                    //构建站点列表和对应的map表
//                    if (desIndexMap.isEmpty()){
//                        desIndexMap.put(desString,0);
//                        desIdAndNameMap.put(0,desName);
//                    }else if (!desIndexMap.containsKey(desString)){
//                        int index = desIndexMap.size();
//                        desIndexMap.put(desString,index);
//                        desIdAndNameMap.put(index,desName);
//                    }
//
//
//                    //组装每趟车装车记录
//                    List<DesRankData> desRankDataSet = new ArrayList<>();
//                    if (truckIDAndDestList != null && truckIDAndDestList.size() > 0 && truckIDAndDestList.containsKey(truckId)) {
//                        desRankDataSet = truckIDAndDestList.get(truckId);
//                        boolean same = false;
//                        for (DesRankData desRankD : desRankDataSet) {
//                            int des = desRankD.getDes();
//                            int ran = desRankD.getRank();
//                            int delivery_num = desRankD.getDeliveryArea();
//                            if (des == desIndexMap.get(desString).intValue() && ran == rank && deliveryNum == delivery_num) {
//                                same = true;
//                                break;
//                            }
//                        }
//                        if (!same) {
//                            DesRankData desRankData = new DesRankData(desIndexMap.get(desString).intValue(), rank,deliveryNum);
//                            desRankDataSet.add(desRankData);
//                        }
//
//
//                    } else {
//                        DesRankData desRankData = new DesRankData(desIndexMap.get(desString).intValue(), rank,deliveryNum);
//                        desRankDataSet.add(desRankData);
//                    }
//                    truckIDAndDestList.put(truckId, desRankDataSet);
//                }
//
//            }
//
//
//            try {
//                input.close();
//            } catch (Exception e) {

//            }
        } catch (Exception e) {
            e.printStackTrace();
        }


        jztDate.setDesAndNameMap(desAndNameMap);
        jztDate.setDesIndexMap(desIndexMap);
        jztDate.setDesIdAndNameMap(desIdAndNameMap);
        HashMap<String,Integer> desAreaMap = distributionAreaCorrection.getDesAreaMap();
        jztDate.setDesCodeAreaMap(desAreaMap);

        HashMap<Integer,String> desIndexCodeMap = new HashMap<>();
        for (Map.Entry<String,Integer> desIndexM:desIndexMap.entrySet()){
            desIndexCodeMap.put(desIndexM.getValue(),desIndexM.getKey());
        }
        jztDate.setDesIndexCodeMap(desIndexCodeMap);

        //对数据的“提货方式”进行修正
        HashMap<String,List<DesRankData>> new_truckIDAndDestList = new HashMap<>();
        for (Map.Entry<String,List<DesRankData>> desRankData:truckIDAndDestList.entrySet()){
            List<DesRankData> desRankDataList = desRankData.getValue();
            List<DesRankData> newData  = new ArrayList<>();
            for (DesRankData desRankData1:desRankDataList){
                int old_area = desRankData1.getDeliveryArea();
                int desCode = desRankData1.getDes();
                int new_area = desAreaMap.get(desIndexCodeMap.get(desCode));
                if (old_area!=new_area){
                    System.out.println(desIndexCodeMap.get(desCode));
                }
                newData.add(new DesRankData(desCode,desRankData1.getRank(),new_area));
            }
            new_truckIDAndDestList.put(desRankData.getKey(),newData);
//            desRankDataList.stream().forEach(t -> t.setDeliveryArea(desAreaMap.get(desIndexCodeMap.get(t.getDes()))));
        }

        jztDate.setTruckIDAndDestList(new_truckIDAndDestList);



        return jztDate;
    }

    /**
     * 获得指定文件夹下文件名
     * @param path
     * @return
     */
    public List<String> getFileName(String path) {
        File f = new File(path);
        List<String> list = new ArrayList<String>();
        if (!f.exists()) {
            System.out.println(path + " not exists");
            return list;
        }

        File fa[] = f.listFiles();
        for (int i = 0; i < fa.length; i++) {
            File fs = fa[i];
            if (fs.isDirectory()) {
                System.out.println(fs.getName() + " [目录]");
            } else {
                list.add(path + "\\" + fs.getName());
            }
        }
        return list;
    }


    public XMLReader fetchSheetParser(SharedStringsTable sst) throws SAXException {
        XMLReader parser =
                XMLReaderFactory.createXMLReader(
                        "com.sun.org.apache.xerces.internal.parsers.SAXParser"
                );
        ContentHandler handler = new SheetHandler(sst);
        parser.setContentHandler(handler);
        return parser;
    }

    private static class SheetHandler extends DefaultHandler {
        private SharedStringsTable sst;
        private String lastContents;
        private boolean nextIsString;

        private SheetHandler(SharedStringsTable sst) {
            this.sst = sst;
        }

        public void startElement(String uri, String localName, String name, Attributes attributes) throws SAXException {
            if (name.equals("c")) {
                System.out.print(attributes.getValue("r") + " - ");
                String cellType = attributes.getValue("t");
                if (cellType != null && cellType.equals("s")) {
                    nextIsString = true;
                } else {
                    nextIsString = false;
                }
            }
            lastContents = "";
        }

        public void endElement(String uri, String localName, String name) throws SAXException {
            if (nextIsString) {
                int idx = Integer.parseInt(lastContents);
                lastContents = new XSSFRichTextString(sst.getEntryAt(idx)).toString();
                nextIsString = false;
            }

            if (name.equals("v")) {
                System.out.println(lastContents);
            }
        }

        public void characters(char[] ch, int start, int length) throws SAXException {
            lastContents += new String(ch, start, length);
        }
    }


    }
