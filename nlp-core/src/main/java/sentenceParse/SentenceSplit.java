package sentenceParse;

import java.util.LinkedList;
import java.util.List;

/**
 * Created by stormor on 2017/11/7.
 */
public class SentenceSplit {
    /**
     * 分句
     * @param content
     * @return
     */
    public static List<String> toSentenceList(String content) {
        char[] chars = content.toCharArray();
        StringBuilder sb = new StringBuilder();

        List<String> sentences = new LinkedList<String>();

        for (int i = 0; i < chars.length; ++i) {
            if (sb.length() == 0 && (Character.isWhitespace(chars[i]) || chars[i] == ' ')) {
                continue;
            }

            sb.append(chars[i]);
            switch (chars[i]) {
                case '.':
                    if (i < chars.length - 1 && chars[i + 1] > 128) {
                        insertIntoList(sb, sentences);
                        sb = new StringBuilder();
                    }
                    break;
                case '…': {
                    if (i < chars.length - 1 && chars[i + 1] == '…') {
                        sb.append('…');
                        ++i;
                        insertIntoList(sb, sentences);
                        sb = new StringBuilder();
                    }
                }
                break;
                case ' ':
                case '	':
                case ' ':
                case '。':
                    insertIntoList(sb, sentences);
                    sb = new StringBuilder();
                    break;
                case ';':
                case '；':
                    insertIntoList(sb, sentences);
                    sb = new StringBuilder();
                    break;
                case '!':
                case '！':
                    insertIntoList(sb, sentences);
                    sb = new StringBuilder();
                    break;
                case '?':
                case '？':
                    insertIntoList(sb, sentences);
                    sb = new StringBuilder();
                    break;
                case '\n':
                case '\r':
                    insertIntoList(sb, sentences);
                    sb = new StringBuilder();
                    break;
            }
        }

        if (sb.length() > 0) {
            insertIntoList(sb, sentences);
        }

        return sentences;
    }

    private static void insertIntoList(StringBuilder sb, List<String> sentences) {
        String content = sb.toString().trim();
        if (content.length() > 0) {
            sentences.add(content);
        }
    }
}
