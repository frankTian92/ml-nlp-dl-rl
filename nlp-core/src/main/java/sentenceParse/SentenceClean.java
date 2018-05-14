package sentenceParse;


import com.hankcs.hanlp.HanLP;

import java.util.HashSet;
import java.util.List;
import java.util.stream.Collectors;

/**
 * Created by stormor on 2017/11/6.
 */
public class SentenceClean implements SentenceParse {

    private final int MIN_LENGTH = 5;
    //停用词
    private HashSet<String> stopWords;


    public SentenceClean(HashSet<String> stopWords){
        this.stopWords = stopWords;
    }

    public SentenceClean(){

    }


    //去除停用词
    @Override
    public String parseSentence2Sting(String sentence) {
        if (stopWords != null && stopWords.size()>0 && sentence!=null && sentence.length()>1){
            for (String removeWord : stopWords) {
                String m = sentence.replace(removeWord, "1");
                sentence = m;
            }
        }
        return sentence;
    }

    //通过词性对句子进行过滤
    @Override
    public List<String> parseSentence2List(String sentence) {
        if (sentence !=null && sentence.length()>=MIN_LENGTH){
            return HanLP.segment(sentence).stream()
                    .filter( t -> t.nature.startsWith("n") || t.nature.startsWith("v"))
                    .map(t ->t.word)
                    .filter( t -> t.length()>1)
                    .collect(Collectors.toList());
        }else {
            return null;
        }


    }



    public HashSet<String> getStopWords() {
        return stopWords;
    }

    public void setStopWords(HashSet<String> stopWords) {
        this.stopWords = stopWords;
    }

}
