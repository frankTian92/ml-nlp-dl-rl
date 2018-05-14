package sentenceParse;

import java.util.regex.Matcher;
import java.util.regex.Pattern;

/**
 * Created by stormor on 2017/11/6.
 */
public class SetenceParseRegex {


    /**
     * 对文本中的word进行提取，并统计其个数
     * @param word
     * @param text
     * @return
     */
    public static double getWordCount(String word,String text){
        String regexWord = "(" + word + ")";
        return  getRegexExStrNum(text,regexWord);
    }

    /**
     * 正则表达式抽取值,对该值进行计数
     *
     * @param text
     * @param regex
     * @return
     */
    public static double getRegexExStrNum(String text, String regex) {
        Pattern p = Pattern.compile(regex);
        Matcher m = p.matcher(text);
        double i = 0.0;
        while (m.find()) {
            i++;
        }
        return i;
    }

    /**
     * 正则表达式抽取值
     * @param sentence
     * @param regex
     * @return
     */
    public static String getRegexExStr (String sentence,String regex){
        StringBuffer stringBuffer = new StringBuffer();
        Pattern p = Pattern.compile(regex);
        Matcher m = p.matcher(sentence);
        while (m.find()){
            int i =0;
            stringBuffer.append(m.group(i).trim());
            i++;
        }
        return stringBuffer.toString();
    }
}
