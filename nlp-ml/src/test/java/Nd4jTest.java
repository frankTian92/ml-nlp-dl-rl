import org.nd4j.linalg.api.ndarray.INDArray;
import org.nd4j.linalg.factory.Nd4j;
import org.nd4j.linalg.indexing.NDArrayIndex;
import org.nd4j.linalg.indexing.NDArrayIndexAll;

/**
 * Created by stormor on 2017/11/8.
 */
public class Nd4jTest {
    public static void main(String[] args) {
//        INDArray tens = Nd4j.zeros(3,5).addi(10);
//        System.out.println(tens);
//        INDArray randArray = Nd4j.rand(3,2);
//        System.out.println(randArray);
//        INDArray randnArray = Nd4j.randn(3,4);
//        System.out.println(randnArray);

//        double[] v1 = new double[]{2.0,3.0,5.0};
//        INDArray vector = Nd4j.create(v1);
//        System.out.println(vector);

        INDArray array = Nd4j.linspace(1,25,25).reshape(5,5);
        System.out.println(array);
        System.out.println(array.get(NDArrayIndex.point(2), NDArrayIndex.all()));

    }
}
