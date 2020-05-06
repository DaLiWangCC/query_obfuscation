import java.util.ArrayList;
import java.util.List;

/**
 * Created by rememberthelesson on 2018/12/7.
 */
public class DataPoint {
//    private double dimension[]; //样本点的维度
    private String pointName; //样本点名字
    private Cluster cluster; //类簇
    private Cluster[] clusters; //所有类簇

    private double euDt;//样本点到质点的距离

    private String type; // user tmn
    private String query; // 搜索的文本
    private String date; // 搜索时间
    public Integer number; // 编号

    private ArrayList<Float> distanceList; // 和其他元素的距离

    public DataPoint(double dimension[], String pointName) {
//        this.dimension = dimension;
        this.pointName = pointName;
        this.cluster = null;
    }
    public DataPoint(String type, String query, String date, Integer number){
        this.type = type;
        this.query = query;
        this.date = date;
        this.number = number;
        this.distanceList = new ArrayList<Float>();
    }
    public DataPoint(String type, String query, ArrayList<Float> distanceList, Integer number){
        this.query = query;
        this.type = type;

        this.number = number;
        this.distanceList = distanceList;
    }
    public void setCluster(Cluster cluster) {
        this.cluster = cluster;
    }


    // 计算到簇内其他所有点的欧式距离的和的开方， 这里我修改为计算到簇内所有点的相似度的平均值，也就是计算a(i)
    public double calEuclideanDistanceSum() {
        double sum = 0.0;
        Cluster cluster = this.getCluster();
        ArrayList<DataPoint> dataPoints = cluster.getDataPoints();

//        for (int i = 0; i < dataPoints.size(); i++) {
//            // 计算到所以其他节点的距离
//            double[] dims = dataPoints.get(i).getDimensioin();
//            for (int j = 0; j < dims.length; j++) {
//                double temp = Math.pow((dims[j] - this.dimension[j]), 2);
//                sum = sum + temp;
//            }
//        }
//        // 开方
//        return Math.sqrt(sum);
        for (int i = 0; i < dataPoints.size(); i++) {
            // 计算到所有其他节点的距离
            DataPoint dp = dataPoints.get(i);
            double simility = distanceList.get(dp.number);
            sum = sum + simility;

        }
        // 平均值
        return sum/dataPoints.size();
    }

    // 计算b(i)
    public double calEuclideanDistanceToOtherCluster(Cluster otherCluster){
        ArrayList<DataPoint> dataPoints = otherCluster.getDataPoints();
        double minDistance = 0;// 找最相似的
        for (int i = 0; i < dataPoints.size(); i++) {
            DataPoint dp = dataPoints.get(i);
            double simility = distanceList.get(dp.number);
            if (simility>minDistance){
                minDistance = simility;
            }
        }
        return minDistance;
    }

    // 计算本元素的s(i)
    public double calSi(){
        double sum = 0;
        for (int i = 0; i < clusters.length; i++) {
            Cluster otherCluster = clusters[i];
            if (otherCluster == cluster)break;;

            double a = calEuclideanDistanceSum();
            double b = calEuclideanDistanceToOtherCluster(otherCluster);
            double si = (b - a)/( a>b ? a:b);
            sum += si;
        }


        return sum/clusters.length;
    }

    // 测试本样本点到medoid点的欧式距离
    public double testEuclideanDistance(Medoid c) {


        // 各个维度的平方和的开根号
//        for (int i = 0; i < dimension.length; i++) {
//            double temp = Math.pow((dimension[i] - cDim[i]), 2);
//            sum = sum + temp;
//        }
//
//        return Math.sqrt(sum);

        // 本点到中心点的距离
        return this.distanceList.get(c.number);
    }

//    public double[] getDimension() {
//        return this.dimension;
//    }

    public Cluster getCluster() {
        return this.cluster;
    }

    public double getCurrentEuDt() {
        return this.euDt;
    }

    public String getPointName() {
        return this.pointName;

    }

    public void setPointName(String pointName) {
        this.pointName = pointName;
    }

    public double getEuDt() {
        return euDt;
    }

    public void setEuDt(double euDt) {
        this.euDt = euDt;
    }

    public String getType() {
        return type;
    }

    public void setType(String type) {
        this.type = type;
    }

    public String getQuery() {
        return query;
    }

    public void setQuery(String query) {
        this.query = query;
    }

    public String getDate() {
        return date;
    }

    public void setDate(String date) {
        this.date = date;
    }

    public Integer getNumber() {
        return number;
    }

    public void setNumber(Integer number) {
        this.number = number;
    }

    public List<Float> getDistanceList() {
        return distanceList;
    }

    public void setDistanceList(ArrayList<Float> distanceList) {
        this.distanceList = distanceList;
    }

    public Cluster[] getClusters() {
        return clusters;
    }

    public void setClusters(Cluster[] clusters) {
        this.clusters = clusters;
    }

    @Override
    public String toString() {
        String str = type+ "\t\t" + query + "\t\t";
        for (int i = 0; i < distanceList.size(); i++) {
            float distant = distanceList.get(i);
            str = str.concat(Float.toString(distant));
            if (i < distanceList.size()-1){
                str = str.concat(",");
            }
        }
        return str;
    }

    public String returnLine(){
        String str = type+ "\t\t" + query + "\t\t";


        for (int i = 0; i < distanceList.size(); i++) {
            float distant = distanceList.get(i);
            str = str.concat(Float.toString(distant));

            if (i < distanceList.size()-1){
                str = str.concat(",");
            }
        }
        return str;
    }
}
