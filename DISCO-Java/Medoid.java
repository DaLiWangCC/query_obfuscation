import java.util.ArrayList;
import java.util.List;

/**
 * Created by rememberthelesson on 2018/12/7.
 */
public class Medoid {
    private double dimension[]; // 质点的维度
    private Cluster cluster; //所属类簇
    private Cluster[] clusters; //所有类簇
    private List<Float> distanceList; // 和其他元素的距离

    private double etdDisSum;//Medoid到本类簇中所有的欧式距离之和

    private String type; // user tmn
    private String query; // 搜索的文本
    private String date; // 搜索时间
    public Integer number; // 编号


    public Medoid(int number) {
        this.number = number;
    }

    public void setCluster(Cluster c) {
        this.cluster = c;
    }

    public double[] getDimension() {
        return this.dimension;
    }

    public Cluster getCluster() {
        return this.cluster;
    }

    public void calcMedoid() {// 取代价最小的点为本簇的中心
        calcEtdDisSum();
        double maxSi = 0;
        ArrayList<DataPoint> dps = this.cluster.getDataPoints();
        for (int i = 0; i < dps.size(); i++) {
            // 每个点的s(i)
            DataPoint dp = dps.get(i);
            double tempSi = dp.calSi();
            // 取s(i)最大的点
            if (maxSi < tempSi) {
                number = dp.number;
                maxSi=tempSi;
            }
        }
        // 设置本簇的中心
        cluster.setMedoidNumber(number);
        Medoid newMedoid = new Medoid(number);
        newMedoid.setCluster(cluster);
        cluster.setMedoid(newMedoid);
    }

    // 计算该Medoid的si
    private void calcEtdDisSum() {
        double sum=0.0;
        Cluster cluster=this.getCluster();
//        ArrayList<DataPoint> dataPoints=cluster.getDataPoints();

        etdDisSum= sum;
    }

    public Cluster[] getClusters() {
        return clusters;
    }

    public void setClusters(Cluster[] clusters) {
        this.clusters = clusters;
    }

    public List<Float> getDistanceList() {
        return distanceList;
    }

    public void setDistanceList(List<Float> distanceList) {
        this.distanceList = distanceList;
    }

    public Integer getNumber() {
        return number;
    }

    public void setNumber(Integer number) {
        this.number = number;
    }
}
