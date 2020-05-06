import java.util.ArrayList;

/**
 * Created by rememberthelesson on 2018/12/7.
 */
public class Cluster {

    private String clusterName; // 类簇名
    private Medoid medoid; // 类簇的质点
    private ArrayList<DataPoint> dataPoints; // 类簇中各样本点
    private int medoidNumber = 0;

    public Cluster(String clusterName) {
        this.clusterName = clusterName;
        this.medoid = null; // will be set by calling setCentroid()
        dataPoints = new ArrayList<DataPoint>();
    }

    public void setMedoid(Medoid c) {
        medoid = c;
    }

    public Medoid getMedoid() {
        return medoid;
    }


    public void addDataPoint(DataPoint dp) { // called from CAInstance
        dp.setCluster(this);// 标注该类簇属于某点,计算欧式距离
        this.dataPoints.add(dp);
    }

    public void removeDataPoint(DataPoint dp) {
        this.dataPoints.remove(dp);
    }

    public int getNumDataPoints() {
        return this.dataPoints.size();
    }

    public DataPoint getDataPoint(int pos) {
        return (DataPoint) this.dataPoints.get(pos);
    }


    public String getName() {
        return this.clusterName;
    }

    public ArrayList<DataPoint> getDataPoints() {
        return this.dataPoints;
    }

    public String getClusterName() {
        return clusterName;
    }

    public void setClusterName(String clusterName) {
        this.clusterName = clusterName;
    }

    public void setDataPoints(ArrayList<DataPoint> dataPoints) {
        this.dataPoints = dataPoints;
    }

    public int getMedoidNumber() {
        return medoidNumber;
    }

    public void setMedoidNumber(int medoidNumber) {
        this.medoidNumber = medoidNumber;
    }
}
