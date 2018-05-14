package RelevancyComputeTool;

import Numprocess.NumNorm;
import com.hankcs.hanlp.suggest.scorer.editdistance.CharArray;
import com.hankcs.hanlp.suggest.scorer.lexeme.IdVector;
import org.apache.commons.lang3.StringUtils;
import sentenceParse.SentenceClean;

import java.util.HashMap;
import java.util.HashSet;
import java.util.Set;

/**
 * Created by stormor on 2017/11/7.
 * 超短文本与关键词组之间的相似度计算，文本长度 < 100
 */
public class MostShortTextRelevancyCompute implements RelevancyCompute {

    private final double idvSimRatio = 0.05;

    public MostShortTextRelevancyCompute() {
    }

    @Override
    public double releancyScore(String content, String title,
                                HashSet<String> removeWords, Set<String> keyWords, HashMap<String, Double> keyWordAndWeigt,
                                HashMap<String, Double> IDFMap, StringBuffer hitWords) {

        double simScore = 0.0;
        SentenceClean sentenceClean = new SentenceClean(removeWords);
        String newTitle = null;
        String newContent = null;
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

        for (String kw : keyWords) {
            if (title.contains(kw) && titleSize > 1) {
                simScore += getIdVectorSimScore(newTitle, kw) * idvSimRatio;
                simScore += getEditDistanceScore(newTitle, kw) * (1 - idvSimRatio);
                hitWords.append(kw + ",");
            }

            if (content.contains(kw) && contentSize > 5) {
                simScore += getIdVectorSimScore(newContent, kw) * idvSimRatio;
                simScore += getEditDistanceScore(newContent, kw) * (1 - idvSimRatio);
                hitWords.append(kw + ",");
            }

        }

        hitWords.append("less_50");
        return NumNorm.noreValue(simScore);


    }

    /**
     * 基于词义进行相似度计算
     *
     * @param sentence
     * @param query
     * @return
     */
    private double getIdVectorSimScore(String sentence, String query) {
        IdVector sentenceIdVv = null;
        IdVector queryIdV = new IdVector(query);
        IdVector idVector = new IdVector(sentence);
        if (idVector.idArrayList.size() != 0) {
            sentenceIdVv = idVector;
            return queryIdV.similarity(sentenceIdVv);
        } else {
            return 0.0;
        }

    }

    /**
     * 编辑距离打分器
     *
     * @param sentence
     * @param query
     * @return
     */
    public double getEditDistanceScore(String sentence, String query) {
        CharArray sentenceArr = new CharArray(sentence.toCharArray());
        CharArray queryArr = new CharArray(query.toCharArray());
        if (sentence == null || sentence.length() < 2) {
            return 0.0;
        } else {
            return sentenceArr.similarity(queryArr);
        }

    }


}
