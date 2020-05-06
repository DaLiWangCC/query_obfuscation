import de.linguatools.disco.*;

import java.io.*;
import java.math.BigDecimal;
import java.util.ArrayList;
import java.util.Iterator;
import java.util.List;
import java.util.Map;

/**
 * Created by rememberthelesson on 2018/12/7.
 */

public class main {

    public DISCO disco;
    public String fileName;
    public String userNumber = "user_07/";
    public String mixDataPath = "/saveData/nothing/mix/";// 读取文件的地方，TMN与User混合的文件
    public String simDataPath = "/Users/rememberthelesson/wanghao/Firefox/simData/"+userNumber;// 计算出相似度的临时文件
    public String clusterDataPath = "/Users/rememberthelesson/wanghao/Firefox/clusterData/"+userNumber;// 聚类好的结果，可以直接画图


    private TextSimilarity ts;
    public static void main(String[] args) throws WrongWordspaceTypeException, IOException, CorruptConfigFileException {
        main m = new main();

        m.similar();// sample

        // 数据源
        String path = "/Users/rememberthelesson/wanghao/Firefox/saveData/similar/mix/";
        // 读取目录下所有文件
        File file = new File(path);		//获取其file对象
        File[] fs = file.listFiles();	//遍历path下的文件和目录，放在File数组中
        for(File f:fs){					//遍历File[]数组
            if(!f.isDirectory() && f.getPath().contains(".txt")){
                //若非目录(即文件)，则打印
//                System.out.println("当前文件: "+f.getPath());
//                m.startWithTxt(f.getPath());
            }

        }

//        m.startWithTxt("/Users/rememberthelesson/wanghao/Firefox/saveData/nothing/mix/TMN_queries_01_9_2018.12.22_mix500.txt");
//        m.startWithTxt("/Users/rememberthelesson/wanghao/Firefox/saveData/nothing/mix/TMN_queries_03_9_2018.12.29_mix500.txt");

//        m.startWithSimTxt();

    }
    public void similar() throws IOException, CorruptConfigFileException, WrongWordspaceTypeException {
        disco = DISCO.load("enwiki-20130403-word2vec-lm-mwl-lc-sim.denseMatrix");
        ts = new TextSimilarity();
        String word1 = "heisman";
        String word2 = "heisman";
        float simts = TextSimilarity.textSimilarity(word1,word2,disco,DISCO.SimilarityMeasure.COSINE);
        Map<String,Float> wv = disco.getWordvector("you");
        System.out.println(wv);
        float sim = disco.semanticSimilarity(word1, word2, DISCO.getVectorSimilarity(DISCO.SimilarityMeasure.COSINE));
        System.out.println("similarity between "+word1 +" " +word2 +": "+sim);
        System.out.println("TextSimilarity between "+word1 +" " +word2 +": "+sim);

    }

    public void startWithTxt(String filename) throws IOException {

        ArrayList<DataPoint> dataPoints = ReadFile.getDataFromTxt(filename);

        // 为每个元素计算到其他人的距离
//        for (int i = 0; i < dataPoints.size(); i++) {
//            DataPoint dp = dataPoints.get(i);
//            for (int j = 0; j < dataPoints.size(); j++) {
//                DataPoint otherDp = dataPoints.get(j);
//                float textsim = TextSimilarity.textSimilarity(dp.getQuery(),otherDp.getQuery(),disco,DISCO.SimilarityMeasure.COSINE);
//                dp.getDistanceList().add(textsim);
//                System.out.println("相似度: "+textsim);
//            }
//        }

        // 将每2个查询的每个词进行比较，选择最接近的相似度
        for (int i = 0; i < dataPoints.size(); i++) {
            DataPoint dp = dataPoints.get(i);
            // 替换掉|，替换两个空格
            String originStr = dp.getQuery();
            String dpQuery = dp.getQuery().replace("|"," ");
            dpQuery = dpQuery.replace("  "," ");
            dpQuery = dpQuery.replace("  "," ");

            String[] words = dpQuery.split(" ");
            for (int j = 0; j < dataPoints.size(); j++) {
                DataPoint otherDp = dataPoints.get(j);
                String otherDpQuery = otherDp.getQuery().replace("|"," ");
                String[] otherwords = otherDpQuery.split(" ");
                float maxSim = 0;

                for (int k = 0; k < words.length; k++) {
                    for (int l = 0; l < otherwords.length; l++) {
                        if(words[k]!=null && otherwords[l]!=null){

                            float simWord = disco.semanticSimilarity(words[k],otherwords[l],
                                    DISCO.getVectorSimilarity(DISCO.SimilarityMeasure.COSINE));
//                            System.out.println(simWord+" "+words[k]+" -- "+otherwords[l]);
                            if (simWord>maxSim){
                                maxSim = simWord;
                            }
                        }

                    }
                }
                if(dp == otherDp){
                    maxSim = 1;// 如果是非字符库中的词汇，与自己的相似度也为-2
                }

                // 保留3位小数
                BigDecimal bd = new BigDecimal(maxSim);
                bd   =   bd.setScale(3,4);
                maxSim   =   bd.floatValue();

                dp.getDistanceList().add(maxSim);


//                System.out.println("相似度2: "+dp.getQuery()+" | "+otherDp.getQuery()+" "+maxSim);
            }
        }

        // 写到文本里
        BufferedWriter writer = null;
        String simFileName = filename.replace("saveData/similar/mix","simData/mywork")  ;
//        createDir(simFileName.replace(".txt",""));

        simFileName = simFileName.replace(".txt","_simData.txt")  ;

        File newFile = new File(simFileName);
        newFile.createNewFile();
        writer = new BufferedWriter(new OutputStreamWriter(new FileOutputStream(newFile, false), "UTF-8"));

        for (int i = 0; i < dataPoints.size(); i++) {
            DataPoint dp = dataPoints.get(i);
            StringBuilder stringBuilder = new StringBuilder();

            stringBuilder.append(dp.getType());
            stringBuilder.append("\t\t");
            stringBuilder.append(dp.getQuery().replace("|"," "));
            stringBuilder.append("\t\t");
            for (int j = 0; j < dp.getDistanceList().size(); j++) {
                double dis = dp.getDistanceList().get(j);
                stringBuilder.append(Double.toString(dis));

                if (j < dp.getDistanceList().size()-1){
                    stringBuilder.append(",");
                }
            }
            String str = stringBuilder.toString();
            writer.write(str);
            writer.write("\n");
        }
        writer.flush();// 不加这个最后一行写不进去


        startWithSimTxt(simFileName);
    }


    public void startWithSimTxt(String simFileName) throws IOException {
        ArrayList<DataPoint> dataPoints = ReadFile.getDataFromSimTxt(simFileName);

        // 聚类初始化
        int k = 15;
        ClusterAnalysis ca=new ClusterAnalysis(k,30, dataPoints);

        // 随机选择k个中心点
        int[] cen = new int[k];
        for (int i = 0; i < k; i++) {
            final double d = Math.random();
            final int ki = (int)(d*k);

            cen[i]=ki;
        }


        // 开始聚类
        ca.startAnalysis(cen);

        ArrayList<DataPoint>[] v = ca.getClusterOutput();

        // 将结果以聚类顺序写入txt
        // 写到文本里
        BufferedWriter writer2 = null;
        String simClusterFileName = simFileName.replace("simData/mywork","clusterData/mywork");
//        createDir(simClusterFileName.replace(".txt",""));
        simClusterFileName = simClusterFileName.replace("_simData.txt","_clusterData.txt");

        File newFile2 = new File(simClusterFileName);
        newFile2.createNewFile();
        writer2 = new BufferedWriter(new OutputStreamWriter(new FileOutputStream(newFile2, false), "UTF-8"));

        ArrayList<String> writeArray = new ArrayList<String>();

        int count = 0;
        for (int ii=0; ii<v.length; ii++){
            ArrayList tempV = v[ii];
            System.out.println("-----------Cluster"+ii+"---------");
            Iterator iter = tempV.iterator();

            while(iter.hasNext()){
//                System.out.println(count);
                count++;
                DataPoint dpTemp = (DataPoint)iter.next();
//                System.out.println(dpTemp);
                writeArray.add(dpTemp.returnLine());
                String num = Integer.toString(dpTemp.number);
                // num是聚类之前的位置，ii是聚类之后的排序
                writer2.write(num+ "\t\t"+ii+"\t\t"+dpTemp.returnLine());
                writer2.write("\n");
            }

        }

        writer2.flush();


        System.out.println("PAM迭代结束");
    }




    public static boolean createDir(String destDirName) {
        File dir = new File(destDirName);
        if (dir.exists()) {
            System.out.println("创建目录" + destDirName + "失败，目标目录已经存在");
            return false;
        }
        if (!destDirName.endsWith(File.separator)) {
            destDirName = destDirName + File.separator;
        }
        //创建目录
        if (dir.mkdirs()) {
            System.out.println("创建目录" + destDirName + "成功！");
            return true;
        } else {
            System.out.println("创建目录" + destDirName + "失败！");
            return false;
        }
    }

}
