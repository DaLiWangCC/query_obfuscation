import java.util.ArrayList;
import java.util.Arrays;
import java.util.Comparator;

/**
 * Created by rememberthelesson on 2018/12/7.
 */
public class ClusterAnalysis {

    private Cluster[] clusters;// 所有类簇
    private int miter;// 迭代次数
    private ArrayList<DataPoint> dataPoints = new ArrayList<DataPoint>();// 所有样本点
    private int dimNum;//维度

    public ClusterAnalysis(int k, int iter, ArrayList<DataPoint> dataPoints) {
        clusters = new Cluster[k];// 类簇种类数
        for (int i = 0; i < k; i++) {
            // 创建k个簇
            clusters[i] = new Cluster("Cluster:" + i);
        }
        this.miter = iter;
        this.dataPoints = dataPoints;

    }

    public int getIterations() {
        return miter;
    }

    public ArrayList<DataPoint>[] getClusterOutput() {
        ArrayList<DataPoint> v[] = new ArrayList[clusters.length];
        // 由多到少排序
//        int[] numArray = new int[clusters.length];
//        for (int i = 0; i < clusters.length; i++) {
//            numArray[i] = clusters[i].getDataPoints().size();
//        }
        for (int i = 0; i < clusters.length; i++) {
            v[i] = clusters[i].getDataPoints();
        }
        Arrays.sort(v,new MyComprator());

        return v;
    }


    public void startAnalysis(int[] medoids) {

        setInitialMedoids(medoids);

        int[] newMedoids=medoids;
        int[] oldMedoids= new int[medoids.length];


        // 已经最优，或者达到迭代次数
        int miterCount = 0;
        while(!isEqual(oldMedoids,newMedoids) && miterCount<miter){
            miterCount ++;
            for(int m = 0; m < clusters.length; m++){//每次迭代开始情况各类簇的点
                clusters[m].getDataPoints().clear();
            }
            for (int j = 0; j < dataPoints.size(); j++) {
                int clusterIndex=0;
                double maxCos=Double.MIN_VALUE;

                for (int k = 0; k < clusters.length; k++) {//判断样本点属于哪个类簇，点应与簇的中心有最大相似度
                    double cosDistance=dataPoints.get(j).testEuclideanDistance(clusters[k].getMedoid());
                    if(maxCos<cosDistance){
                        maxCos=cosDistance;
                        clusterIndex=k;
                    }
                }

                //将该样本点添加到该类簇
                clusters[clusterIndex].addDataPoint(dataPoints.get(j));
                dataPoints.get(j).setClusters(clusters);
                dataPoints.get(j).setCluster(clusters[clusterIndex]);
            }

            for(int m = 0; m < clusters.length; m++){
                clusters[m].getMedoid().calcMedoid();//重新计算各类簇的质点
            }

            for(int i=0;i<medoids.length;i++){

                    oldMedoids[i]=newMedoids[i];

            }


            for(int n=0;n<clusters.length;n++){
                // 新的质心
                newMedoids[n]=clusters[n].getMedoid().number;
            }
        }


    }

    private void setInitialMedoids(int[] medoids) {
        for (int n = 0; n < clusters.length; n++) {
            Medoid medoid = new Medoid(medoids[n]);
            clusters[n].setMedoid(medoid);
            medoid.setCluster(clusters[n]);
        }
    }


    private boolean isEqual(int[] oldMedoids,int[] newMedoids){
        boolean flag=false;
        for(int i=0;i<oldMedoids.length;i++){

            if(oldMedoids[i]!=newMedoids[i]){
                return flag;

            }
        }
        flag=true;
        return flag;
    }
}

class MyComprator implements Comparator {
    public int compare(Object arg0, Object arg1) {
        ArrayList<DataPoint> t1=(ArrayList<DataPoint>)arg0;
        ArrayList<DataPoint> t2=(ArrayList<DataPoint>)arg1;


        return t1.size()>t2.size()? 1:-1;

    }
}
