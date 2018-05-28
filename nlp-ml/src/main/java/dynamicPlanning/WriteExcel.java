package dynamicPlanning;

import dynamicPlanning.domain.DeliveryArea;
import dynamicPlanning.domain.DesRankData;
import org.apache.poi.hssf.usermodel.HSSFWorkbook;
import org.apache.poi.ss.usermodel.Cell;
import org.apache.poi.ss.usermodel.Row;
import org.apache.poi.ss.usermodel.Sheet;
import org.apache.poi.ss.usermodel.Workbook;

import java.io.File;
import java.io.FileOutputStream;
import java.io.IOException;
import java.io.OutputStream;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

/**
 * \* Created with IntelliJ IDEA.
 * \* User: Administrator
 * \* Date: 2018/5/14 0014
 * \* Time: 下午 14:35
 * \* Description:
 * \
 */
public class WriteExcel {

    /**
     * 将转换后的排单数据存为excel文件
     * @param dataList
     * @param savePath
     * @param desIndexCodeMap
     * @param desIndexNameMap
     */
    public static void writeExcelData(HashMap<String,List<DesRankData>> dataList, String savePath,
                                      HashMap<Integer,String> desIndexCodeMap, HashMap<Integer,String> desIndexNameMap){
        String[] title = {"装车单号","单位编号","单位名称","装车单装车顺序","提货方式"};
        OutputStream out = null;
        try {

            // 读取Excel文档
            File saveFile = new File(savePath);
            if (!saveFile.exists()){
                saveFile.createNewFile();
            }

            // 如果文件不存在，则创建一个新的Excel
            Workbook workBook= new HSSFWorkbook();
            workBook.createSheet("Sheet1");
            // sheet 对应一个工作页
            Sheet sheet = workBook.getSheetAt(0);
            /**
             * 删除原有数据，除了属性列
             */
            int rowNumber = sheet.getLastRowNum();  // 第一行从0开始算
            System.out.println("原始数据总行数，除属性列：" + rowNumber);
            for (int i = 1; i <= rowNumber; i++) {
                Row row = sheet.getRow(i);
                sheet.removeRow(row);
            }
            // 创建文件输出流，输出电子表格：这个必须有，否则你在sheet上做的任何操作都不会有效
            out =  new FileOutputStream(saveFile);
            workBook.write(out);
            /**
             * 往Excel中写新数据
             */
            int j = 0;
            //增加标题
            Row row = sheet.createRow(j);
            for (int i =0 ; i<title.length;i++){
                Cell cell = row.createCell(i);
                cell.setCellValue(title[i]);
            }
            j+=1;

            for (Map.Entry<String,List<DesRankData>> data :dataList.entrySet()){
                // 创建一行：从第二行开始，跳过属性列

                // 得到要插入的每一条记录
                String zcdh = data.getKey();
                List<DesRankData> desRankDatas = data.getValue();
                for (DesRankData desRankData:desRankDatas){
                    row = sheet.createRow(j);
                    int rank = desRankData.getRank();
                    int desIndex= desRankData.getDes();
                    String desName = desIndexNameMap.get(desIndex);
                    String desCode = desIndexCodeMap.get(desIndex);

                    Cell first = row.createCell(0);
                    first.setCellValue(zcdh);
                    Cell second = row.createCell(1);
                    second.setCellValue(desCode);
                    Cell third = row.createCell(2);
                    third.setCellValue(desName);
                    Cell four = row.createCell(3);
                    four.setCellValue(rank);

                    j+=1;
                }

            }
            // 创建文件输出流，准备输出电子表格：这个必须有，否则你在sheet上做的任何操作都不会有效
            out =  new FileOutputStream(saveFile);
            workBook.write(out);
        } catch (Exception e) {
            e.printStackTrace();
        } finally{
            try {
                if(out != null){
                    out.flush();
                    out.close();
                }
            } catch (IOException e) {
                e.printStackTrace();
            }
        }
        System.out.println("数据导出成功");
    }
}