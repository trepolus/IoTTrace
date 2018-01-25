package regionsplitter;
import java.io.BufferedWriter;
import java.io.File;
import java.io.FileWriter;
import java.io.IOException;

public class Region {

	private double endLat, endLon, startLat, startLon;
	private String path;
	private BufferedWriter writer;
	private int count, id;
	
	public Region(int id, double endLat, double endLon, double startLat, double startLon) {
		count = 0;
		this.id = id;
		this.endLat = endLat;
		this.endLon = endLon;
		this.startLat = startLat;
		this.startLon = startLon;
		File dir = new File("regions");
		if(!dir.exists()) {
			dir.mkdir();
		}
		path = "regions/region" + id + ".txt";
		try {
			writer = new BufferedWriter(new FileWriter(path));
		}
		catch(IOException ioe) {
			ioe.printStackTrace();
		}
		//write("Region from latitude " + startLat + " to " + endLat + " and longitude " + startLon + " to " + endLon + "\n");
	}
	
	public void add(String data) {
		count++;
		write(data);
	}
	
	public void write(String content) {
		try {
			writer.write(content + "\n");
		}
		catch(IOException ioe) {
			ioe.printStackTrace();
		}
	}
	
	public void close() {
		try {
			writer.close();
		} catch (IOException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		}
	}
	
	public String getCoords() {
		return startLon + " " + endLon + " " + startLat + " " + endLat;
	}
	
	public boolean isElement(double lat, double lon) {
		if(lat > startLat && lat < endLat && lon > startLon && lon < endLon) return true;
		return false;
	}
	
	public int getCount() {
		return count;
	}
	
	public int getID() {
		return id;
	}
}
