import de.linguatools.disco.*;

import java.io.IOException;
import java.util.Map;

public class SentenceVector {
    public DISCO disco;

    public void similar() throws IOException, CorruptConfigFileException, WrongWordspaceTypeException {
        disco = DISCO.load("enwiki-20130403-word2vec-lm-mwl-lc-sim.denseMatrix");

        // 将查询分解为多个单词
        // 求和取平均，聚合为句子向量
        Map<String,Float> wv = disco.getWordvector("you");
        String[] querySentence = {"you", "have", "had"};
        Compositionality.computeWordVector(querySentence,disco,Compositionality.VectorCompositionMethod.COMBINED);
    System.out.println(wv);
    }
}
