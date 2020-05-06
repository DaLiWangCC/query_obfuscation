import java.util.List;

/**
 * Created by rememberthelesson on 2018/12/7.
 */
public class QueryModel {
    private String type; // user tmn
    private String query; // 搜索的文本
    private String date; // 搜索时间
    private Integer number; // 编号
    private String clusterNumber; // 被聚类的组号
    private List<Float> distance; // 和其他元素的距离

    public QueryModel(String type, String query, String date, Integer number){
        this.query = query;
        this.type = type;
        this.date = date;
        this.number = number;
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

    public String getClusterNumber() {
        return clusterNumber;
    }

    public void setClusterNumber(String clusterNumber) {
        this.clusterNumber = clusterNumber;
    }

    public Integer getNumber() {
        return number;
    }

    public void setNumber(Integer number) {
        this.number = number;
    }

    public List<Float> getDistance() {
        return distance;
    }

    public void setDistance(List<Float> distance) {
        this.distance = distance;
    }
}
