package RelevancyComputeTool;

import java.util.HashMap;
import java.util.HashSet;
import java.util.Set;

/**
 * Created by stormor on 2017/11/6.
 */
public interface RelevancyCompute {
    /**
     * 相关度计算
     * @return
     */
     double  releancyScore(String content, String title, HashSet<String> removeWords
             , Set<String> keyWords, HashMap<String, Double> keyWordAndWeigt, HashMap<String, Double> IDFMap, StringBuffer hitWords);

}
