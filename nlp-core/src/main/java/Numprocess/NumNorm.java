package Numprocess;

import java.text.DecimalFormat;

/**
 * Created by stormor on 2017/11/7.
 */
public class NumNorm {
    /**
     * 数值正规化，使值均落在（0,1）之间
     * @param value
     * @return
     */
    public static double noreValue (double value){
            return (1 - Math.exp(-2 * value)) / (1 + Math.exp(-2 * value));

    }

    /**
     * 小数点精度控制
     * @param value
     * @return
     */
   public static double decimalControl(double value){
        DecimalFormat df = new DecimalFormat("0.00000");
       return   Double.valueOf(df.format(value));
   }
}
