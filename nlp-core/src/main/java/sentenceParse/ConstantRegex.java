package sentenceParse;

/**
 * Created by stormor on 2017/11/8.
 */
public class ConstantRegex {

    //中文正则表达式
   public static String ZhRegex = "[(\\u4e00-\\u9fa5)]+";

   //英文字母正则表达式
    public static String EnglishRegex = "[a-zA-Z]";

    //标点、空格的正则表达式
    public static String punctuationBlanKRegex = "[\\p{Punct}\\s]+";
}
