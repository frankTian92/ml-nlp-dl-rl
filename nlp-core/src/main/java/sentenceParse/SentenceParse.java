package sentenceParse;

import java.util.List;

/**
 * Created by stormor on 2017/11/6.
 */
public interface SentenceParse {
    /**
     * 句子处理接口
     * @param sentence
     * @return
     */
    String parseSentence2Sting(String sentence);


    List<String>  parseSentence2List(String sentence);

}
