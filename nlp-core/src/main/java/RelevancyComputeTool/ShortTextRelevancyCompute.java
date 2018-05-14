package RelevancyComputeTool;


import Numprocess.NumNorm;
import org.apache.commons.lang3.StringUtils;
import sentenceParse.SentenceClean;
import sentenceParse.SetenceParseRegex;

import java.util.*;

/**
 * Created by stormor on 2017/11/6.
 * 短文本与关键词组之间的相似度计算，文本长度区间(100,300)
 */
public class ShortTextRelevancyCompute implements RelevancyCompute {

    //标题权重
    private final double titleWeight = 3.0;

    //内容权重
    private final double contentWeight = 1.0;

    //未出现在IDFMap中的词，其IDF默认值
    private final double idfDefValue = 2.0;

    public ShortTextRelevancyCompute() {

    }

    @Override
    public double releancyScore(String content, String title,
                                HashSet<String> removeWords, Set<String> keyWords, HashMap<String, Double> keyWordAndWeigt,
                                HashMap<String, Double> IDFMap, StringBuffer hitWords) {

        SentenceClean sentenceClean = new SentenceClean(removeWords);
        String newTitle = null;
        String newContent = null;
        List<String> contentList = null;
        List<String> titleList = null;

        int titleSize = 0;
        int contentSize = 0;
        if (!StringUtils.isEmpty(title) && StringUtils.isNotBlank(title)) {
            newTitle = sentenceClean.parseSentence2Sting(title);
            titleSize = newTitle.length();
        }

        if (!StringUtils.isEmpty(content) && StringUtils.isNotBlank(content)) {
            newContent = sentenceClean.parseSentence2Sting(content);
            contentSize = newContent.length();
        }

        if (contentSize>10){
             contentList = sentenceClean.parseSentence2List(newContent);
        }

        if (titleSize > 3){
            titleList = sentenceClean.parseSentence2List(newTitle);
        }


        HashMap<String, Double> wordAndCount = new HashMap<>();
        double wordSize = 0.0;
        if (titleList != null) {
            for (String word : titleList) {
                wordAndCount.merge(word, titleWeight, (oldV, newV) -> oldV + newV);
                wordSize += titleWeight;
            }
        }

        if (contentList != null) {
            for (String word : contentList) {
                wordAndCount.merge(word, contentWeight, (oldV, newV) -> oldV + newV);
                wordSize += contentWeight;
            }
        }


        Set wordSet = wordAndCount.keySet();
        for (String kw : keyWords) {
            if (!wordSet.contains(kw)) {
                double titleCount = titleWeight * SetenceParseRegex.getWordCount(kw, newTitle);
                double countCount = contentWeight * SetenceParseRegex.getWordCount(kw, newContent);
                double sumCount = titleCount + countCount;
                if (sumCount > 0.1) {
                    wordAndCount.merge(kw, sumCount, (oldV, newV) -> oldV + newV);
                    wordSize += sumCount;
                }

            }
        }


        double finalWordSize = wordSize;
        List<Double> keyWordWeightSum = new ArrayList<>();
        List<Double> weightSum = new ArrayList<>();

        wordAndCount.forEach((k, v) -> {
            double  wordWeight = 1.0;
            double idf = IDFMap.get(k) == null ? idfDefValue : IDFMap.get(k);
            double weight = v / finalWordSize * idf * wordWeight;
            if (keyWords.contains(k)) {
                keyWordWeightSum.add(weight);
                hitWords.append(k + ",");
            }
            weightSum.add(weight);
        });


        double keyWeghtSum = keyWordWeightSum.size() > 0 ? keyWordWeightSum.stream().reduce(Double::sum).get() : 0.0;
        double weightS = weightSum.size() > 0 ? weightSum.stream().reduce(Double::sum).get() : 1.0;


        return NumNorm.noreValue(keyWeghtSum / weightS);

    }



}
