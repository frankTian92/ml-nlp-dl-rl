package Util;

import org.apache.commons.lang3.StringUtils;
import org.nd4j.linalg.api.iter.NdIndexIterator;
import org.nd4j.linalg.api.ndarray.INDArray;

import java.io.*;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

/**
 * Created by stormor on 2017/7/25.
 */
public class ReadWriteTxtUtil {

    /**
     * 读取txt文本
     * @param path 读取路径
     * @return
     */
    public List<String> readTxt(String path){
        List<String> result = new ArrayList<>();
        try {
            String encoding = "UTF-8";
            File file = new File(path);
            if(file.isFile() && file.exists()){
                InputStreamReader reader = new InputStreamReader(
                        new FileInputStream(file),encoding);
                BufferedReader br = new BufferedReader(reader);
                String line = null;
                while ((line = br.readLine())!=null){
                    result.add(line);
                }
                reader.close();
            }else {
                System.out.println("文件路径不正确，文件路径为 ：" + path);
            }

        }catch (Exception e ){
            System.out.println("读取文件内容出错");
            e.printStackTrace();
        }
        return result;
    }


    /**
     * 读取txt文本
     * @param path 读取路径
     * @return
     */
    public HashMap<String,Double> readHashMap(String path,String delimiter){
       HashMap<String,Double> hashMap = new HashMap<>();
        try {
            String encoding = "UTF-8";
            File file = new File(path);
            if(file.isFile() && file.exists()){
                InputStreamReader reader = new InputStreamReader(
                        new FileInputStream(file),encoding);
                BufferedReader br = new BufferedReader(reader);
                String line = null;
                while ((line = br.readLine())!=null){
                    String[] lineSplit = line.split(delimiter);
                    String word = lineSplit[0];
                    double value = Double.valueOf(lineSplit[1]);
                    hashMap.put(word,value);
                }
                reader.close();
            }else {
                System.out.println("文件路径不正确，文件路径为 ：" + path);
            }

        }catch (Exception e ){
            System.out.println("读取文件内容出错");
            e.printStackTrace();
        }
        return hashMap;
    }




    /**
     * 存储数据
     */
    public static void writeTxt(String savePath,HashMap<String,List<String>> txt){
              /* 写入Txt文件 */
        File writeFile = new File(savePath);
        try {
            writeFile.createNewFile(); // 创建新文件
            BufferedWriter out = new BufferedWriter(new FileWriter(writeFile));
            for (Map.Entry<String,List<String>> map :txt.entrySet()){
                out.write(map.getKey() +" : " + StringUtils.join(map.getValue()," ,")+"\r\n"); // \r\n即为换行
            }
            out.flush(); // 把缓存区内容压入文件
            out.close(); // 最后记得关闭文件
        } catch (IOException e) {
            e.printStackTrace();
        }

    }

    /**
     * 存储数据
     */
    public static void writeTxts2iMap(String savePath,HashMap<String,Integer> txt){
              /* 写入Txt文件 */
        File writeFile = new File(savePath);
        try {
            writeFile.createNewFile(); // 创建新文件
            BufferedWriter out = new BufferedWriter(new FileWriter(writeFile));
            for (Map.Entry<String,Integer> map :txt.entrySet()){
                out.write(map.getKey() +" : " + map.getValue()+"\r\n"); // \r\n即为换行
            }
            out.flush(); // 把缓存区内容压入文件
            out.close(); // 最后记得关闭文件
        } catch (IOException e) {
            e.printStackTrace();
        }

    }

    /**
     * 存储数据
     */
    public static void writeTxts2sMap(String savePath,HashMap<String,String> txt){
              /* 写入Txt文件 */
        File writeFile = new File(savePath);
        try {
            writeFile.createNewFile(); // 创建新文件
            BufferedWriter out = new BufferedWriter(new FileWriter(writeFile));
            for (Map.Entry<String,String> map :txt.entrySet()){
                out.write(map.getKey() +" : " + map.getValue()+"\r\n"); // \r\n即为换行
            }
            out.flush(); // 把缓存区内容压入文件
            out.close(); // 最后记得关闭文件
        } catch (IOException e) {
            e.printStackTrace();
        }

    }


    /**
     * 存储数据
     */
    public static void writeTxtArr2(String savePath, INDArray arr2,int size){
              /* 写入Txt文件 */
        System.out.println("------------arr2-------------");
        File writeFile = new File(savePath);
        int one = 0;
        int oneMore = 0;
        int twoMore = 0;
        try {
            writeFile.createNewFile(); // 创建新文件
            BufferedWriter out = new BufferedWriter(new FileWriter(writeFile));

            NdIndexIterator iter = new NdIndexIterator(size,size);
            int i = 1;
            while (iter.hasNext()) {
                int[] nextIndex = iter.next();
                Double nextVal = arr2.getDouble(nextIndex);
                if (nextVal>2.0){
                    twoMore++;
                }else if(nextVal >1.0){
                    oneMore++;
                }else {
                    one++;
                }
                if (i%size ==0){
                    out.write(nextVal.toString() + "\r\n"); // \r\n即为换行
                }else {
                    out.write(nextVal.toString() +"  ");
                }

                //do something with the value
                i++;
            }

            System.out.println("one = " + one);
            System.out.println("oneMore = " + oneMore);
            System.out.println("twoMore = " + twoMore);

            out.flush(); // 把缓存区内容压入文件
            out.close(); // 最后记得关闭文件
        } catch (IOException e) {
            e.printStackTrace();
        }

        System.out.println("------------arr2-------------");

    }

    /**
     * 存储数据
     */
    public static void writeTxtArr1(String savePath, INDArray arr1,int size){
              /* 写入Txt文件 */
        System.out.println("------------arr1-------------");
        File writeFile = new File(savePath);
        int one = 0;
        int oneMore = 0;
        int twoMore = 0;
        try {
            writeFile.createNewFile(); // 创建新文件
            BufferedWriter out = new BufferedWriter(new FileWriter(writeFile));

            NdIndexIterator iter = new NdIndexIterator(size);

            while (iter.hasNext()) {
                int[] nextIndex = iter.next();
                Double nextVal = arr1.getDouble(nextIndex);
                if (nextVal>2.0){
                    twoMore++;
                }else if(nextVal >1.0){
                    oneMore++;
                }else {
                    one++;
                }

                out.write(nextVal.toString() +"  ");

            }

            System.out.println("one = " + one);
            System.out.println("oneMore = " + oneMore);
            System.out.println("twoMore = " + twoMore);

            out.flush(); // 把缓存区内容压入文件
            out.close(); // 最后记得关闭文件
        } catch (IOException e) {
            e.printStackTrace();
        }
        System.out.println("------------arr1-------------");

    }


    /**
     * 存储数据
     * @param txt
     * @param savePath
     */
    public void writeTxt(String[] txt,String savePath){
              /* 写入Txt文件 */
        File writeFile = new File(savePath);
        try {
            writeFile.createNewFile(); // 创建新文件
            BufferedWriter out = new BufferedWriter(new FileWriter(writeFile));
            for (String line :txt){
                out.write(line +"\r\n"); // \r\n即为换行
            }
            out.flush(); // 把缓存区内容压入文件
            out.close(); // 最后记得关闭文件
        } catch (IOException e) {
            e.printStackTrace();
        }

    }




}
