package Main;

import java.io.BufferedReader;
import java.io.File;
import java.io.FileReader;
import java.util.ArrayList;
import java.util.List;

/**
 * Created by Lucas on 11.11.2017.
 */
public class IoTTrace {

  /**
   * Open and read a file, and return the lines in the file as a list
   * of Strings.
   */
  public static List<String> readFile(String filename)
  {
    List<String> allData = new ArrayList<String>();
    try
    {
      BufferedReader reader = new BufferedReader(new FileReader(filename));
      String line;
      while ((line = reader.readLine()) != null)
      {
        allData.add(line);
      }
      reader.close();
      return allData;
    }
    catch (Exception e)
    {
      System.err.format("Exception occurred trying to read '%s'.", filename);
      e.printStackTrace();
      return null;
    }
  }

  public static void main(String[] args) {

    List smartHomeData = new ArrayList<String>();

    smartHomeData = readFile("data/bsp.csv");

    for (int i = 0; i < smartHomeData.size()-1; i++) {
      String line = (String) smartHomeData.get(i);

      System.out.println(line);
    }
  }
}
