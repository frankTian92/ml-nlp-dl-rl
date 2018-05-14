package dynamicPlanning;

import org.nd4j.linalg.api.iter.NdIndexIterator;
import org.nd4j.linalg.api.ndarray.INDArray;
import org.nd4j.linalg.factory.Nd4j;

import java.util.*;
import java.util.stream.Collectors;

public class test {
    public static void main(String[] args) {
//        INDArray nd = Nd4j.create(new float[]{1,2,3,4,5,6},new int[]{3,2});
//        NdIndexIterator iter = new NdIndexIterator(3, 2);
//        System.out.println(nd);
//        while (iter.hasNext()) {
//            int[] nextIndex = iter.next();
//
//            double nextVal = nd.getDouble(nextIndex);
//            System.out.println(nextVal);
//        List<String> strings = new ArrayList<String>();
//        strings.add(2,"a");
//        strings.add(9,"d");
//        strings.add(3,"m");
//        System.out.println();
//        HashSet<DesRankData> set = new HashSet();
//        DesRankData d1 = new DesRankData(1,3);
//        DesRankData d2 = new DesRankData(4,5);
//        DesRankData d3 = new DesRankData(6,2);
//        set.add(d1);
//        set.add(d2);
//        set.add(d3);
//        Collections.sort(set.stream().collect(Collectors.toList()), Comparator.comparing(DesRankData::getDes));
//       List<Integer> list =  set.stream().map(t -> t.getDes()).collect(Collectors.toList());
//
//       list.forEach(t -> System.out.println(t));

//        INDArray arr1 = Nd4j.create(new float[]{1,2,3,4,5,6},new int[]{2,3});
//        INDArray arr1 = Nd4j.ones(2,3);
//        System.out.println(arr1);
//        for(int i = 0; i<2;i++){
//            for (int j = 0; j<3;j++)
//            arr1.put(i,j,arr1.getInt(i,j)+i+j);
//        }
//        System.out.println(arr1);



        Integer[] orig_seq = new Integer[]{1,2,3,4};
        INDArray trans_p_arr2 = Nd4j.ones(6,6);
        INDArray start_p_arr1 = Nd4j.ones(6);
        for (int i =0;i<6;i++){
            for (int j = 0;j<6;j++){
                trans_p_arr2.put(i,j,trans_p_arr2.getInt(i,j)+i+j);
            }
        }

        for (int i =0;i<6;i++){
            start_p_arr1.put(0,i,start_p_arr1.getInt(0,i)+i);
        }

        Viterbi viterbi = new Viterbi();
        ViterBiData result = viterbi.computer(orig_seq, trans_p_arr2, start_p_arr1);
        System.out.println();



        }
    }
