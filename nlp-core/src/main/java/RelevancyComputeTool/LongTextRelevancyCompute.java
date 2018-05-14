package RelevancyComputeTool;

import Numprocess.NumNorm;
import org.apache.commons.lang3.StringUtils;
import sentenceParse.SentenceClean;
import sentenceParse.SentenceSplit;
import sentenceParse.SetenceParseRegex;

import java.text.DecimalFormat;
import java.util.*;
import java.util.stream.Collectors;

/**
 * Created by stormor on 2017/11/7.
 * 长文本与关键词组之间的相似度计算，文本长度 > 300
 */
public class LongTextRelevancyCompute implements RelevancyCompute {

    private static DecimalFormat df = new DecimalFormat("0.00000");
    //标题中词的初始次数
    private  final double titleWordCount = 5.0;

    //标题中，若关键词出现两个以上，句子的初始次数
    private final double titleSentenceCount = 5.0;

    //只出现一个关键词的，句子初始次数
    private final double onlyOneWordSentenceCount = 0.1;

    //未出现在IDF表中的，词的IDF权重
    private final double wordNotInIDFWeight = 2.0;

    //分词中未出现关键词的句子权重
    private final double newWordInSentenceWeight = 1.4;

    //关键词在判断文章是否相关中所占的比重
    private final double wordsWeight = 0.2;

    //关键词在文章中权重放大的倍数
    private final double wordMul = 3.0;

    @Override
    public double releancyScore(String content, String title,
                                HashSet<String> removeWords, Set<String> keyWords, HashMap<String, Double> keyWordAndWeigt,
                                HashMap<String, Double> IDFMap, StringBuffer hitWords) {
        Map<String, Double> wordAndCount = new HashMap<>();
        double wordSize = 0.0;
        double sumScore = 0.0;
        double keyWordSumTFIDF = 0.0;
        double keyWordSentenceSize = 0.0;
        double sentenceSize = 0.0;

        SentenceClean sentenceClean = new SentenceClean(removeWords);

        if (!StringUtils.isEmpty(title) && StringUtils.isNotBlank(title)) {

           String newTitle = sentenceClean.parseSentence2Sting(title);

            List<String> titleList = sentenceClean.parseSentence2List(newTitle);

            if (titleList != null && titleList.size() >= 1) {
                for (String t : titleList) {
                    wordAndCount.merge(t, titleWordCount, (oldV, newV) -> oldV + newV);
                    wordSize += titleWordCount;
                }
            }

            boolean isFilter = false;
            int j = 0;
            String titleString = StringUtils.join(titleList, ",");
            for (String kw : keyWords) {

                //含有关键词的词数量统计
                if (!wordAndCount.containsKey(kw) && newTitle.contains(kw) && !titleString.contains(kw)) {
                    wordAndCount.put(kw, titleWordCount);
                    wordSize += titleWordCount;
                }

                //含有关键词的句子数量统计
                if (newTitle.contains(kw)) {
                    j++;
                    isFilter = true;
                }

            }
            if (isFilter) {
                double s = 0.0;
                if (j >= 2) {
                    s = titleSentenceCount;
                } else {
                    s = onlyOneWordSentenceCount;
                }
                keyWordSentenceSize += s;
                sentenceSize += s;

            }


        }

        if (!StringUtils.isEmpty(content) && StringUtils.isNotBlank(content)) {
          String  newContent = sentenceClean.parseSentence2Sting(content);
            List<String> sentenceList = SentenceSplit.toSentenceList(newContent).stream().filter(t -> t.length() >= 10).collect(Collectors.toList());
            double Ssize = sentenceList.size();
            sentenceSize = sentenceSize + Ssize;
            double i = 1.0;
            for (String sentence : sentenceList) {
                double LScore = getLocationWeight(i / Ssize);
                List<String> wordSeg = sentenceClean.parseSentence2List(sentence);
                if (wordSeg != null && wordSeg.size() >= 1) {
                    for (String word : wordSeg) {
                        wordAndCount.merge(word, LScore, (oldV, newV) -> oldV + newV);
                        wordSize += LScore;
                    }
                    i++;
                }

                //含有关键词的句子数量统计
                boolean isFilter = false;
                int j = 0;
                for (String kw : keyWords) {
                    if (sentence.contains(kw)) {
                        j++;
                        isFilter = true;
                    }

                }


                if (isFilter) {
                    double s = 0.0;
                    if (j >= 3) {
                        s = 3.0;
                    } else if (j == 2) {
                        s = 1.5;
                    } else if (j == 1) {
                        s = onlyOneWordSentenceCount;
                    }
                    keyWordSentenceSize += s;
                    sentenceSize += s;
                }


            }

            //含有关键词的词数量统计——没有被正确分词的“关键词”
            String wordCountKeys = StringUtils.join(wordAndCount.keySet(), ",");
            for (String kw : keyWords) {
                if (!wordAndCount.containsKey(kw) && newContent.contains(kw) && !wordCountKeys.contains(kw)) {
                    double count = SetenceParseRegex.getWordCount(kw, newContent) * newWordInSentenceWeight;
                    wordAndCount.merge(kw, count, (oldV, newV) -> oldV + newV);
                    wordSize += count;
                }
            }
        }


        if (wordAndCount != null && wordAndCount.size() > 0) {

            for (Map.Entry<String, Double> wc : wordAndCount.entrySet()) {
                String k = wc.getKey();
                double v = wc.getValue();
                double idf = wordNotInIDFWeight;
                if (IDFMap.containsKey(k)) {
                    idf = IDFMap.get(k);
                }
                double tfIdf = (v / wordSize) * idf;
                double tfIdfWS = tfIdf;

                for (String kw : keyWords) {
                    if (k.contains(kw)) {
                        tfIdfWS = tfIdf * keyWordAndWeigt.get(kw);
                        keyWordSumTFIDF += tfIdfWS;
                        hitWords.append(k + ",");
                    }
                }
                sumScore += tfIdfWS;

            }


            if (sentenceSize < 1.0) {
                return 0.0;
            } else {
                double tfIdfScore = keyWordSumTFIDF / sumScore;
                double sentenceScore = keyWordSentenceSize / (sentenceSize + 1.0);

                double score = tfIdfScore * wordMul * wordsWeight + sentenceScore * (1 - wordsWeight);
                return Double.valueOf(df.format((NumNorm.noreValue(score))));
            }


        } else {
            return 0.0;
        }
    }

    /**
     * 获取位置权重分别是1.4,1.2,1.0
     *
     * @param sc
     * @return
     */
    private double getLocationWeight(double sc) {
        return (Math.abs(Math.ceil((sc) / 0.2) - 3.5) + 0.5) / 5.0 + 0.8;
    }


}
