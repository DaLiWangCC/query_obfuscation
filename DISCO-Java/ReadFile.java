import java.io.*;
import java.util.ArrayList;
import java.util.List;

/**
 * Created by rememberthelesson on 2018/12/7.
 */
public class ReadFile {

    public static ArrayList<DataPoint> getDataFromTxt(String filename) throws IOException {
        final int BUFFER_SIZE = 20 * 1024 * 1024;
        String encoding = "UTF-8";
        ArrayList<DataPoint> modelArray = new ArrayList<DataPoint>();

        File file = new File(filename);
        BufferedInputStream inp = new BufferedInputStream(new FileInputStream(file), BUFFER_SIZE);
        BufferedReader reader = new BufferedReader(new InputStreamReader(inp, encoding));
//            System.out.println(filename);

        String line = reader.readLine();
        Integer index = 0;
        while (line != null){
            String[] values = line.split("\t\t");

            DataPoint dp = new DataPoint(values[0],values[1],values[2],index);
            modelArray.add(dp);
//            System.out.println(line);
            line = reader.readLine();
            index++;
//            System.out.println(index);
        }

        return modelArray;
    }


    public static ArrayList<DataPoint> getDataFromSimTxt(String filename) throws IOException {
        final int BUFFER_SIZE = 20 * 1024 * 1024;
        String encoding = "UTF-8";
        ArrayList<DataPoint> modelArray = new ArrayList<DataPoint>();

        String filePath = filename;
        File file = new File(filePath);
        BufferedInputStream inp = new BufferedInputStream(new FileInputStream(file), BUFFER_SIZE);
        BufferedReader reader = new BufferedReader(new InputStreamReader(inp, encoding));

        String line = reader.readLine();
        Integer index = 0;
        while (line != null){
            ArrayList<Float> distancelist = new ArrayList<Float>();

            String[] values = line.split("\t\t");
            String[] floats = values[2].split(",");
            for (int i = 0; i < floats.length; i++) {
                distancelist.add(Float.valueOf(floats[i]));
            }
            // type query distancelist number
            DataPoint dp = new DataPoint(values[0],values[1],distancelist,index);

            modelArray.add(dp);
//            System.out.println(line);
            line = reader.readLine();
            index++;
        }

        return modelArray;
    }
}
