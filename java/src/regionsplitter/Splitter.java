package regionsplitter;

public class Splitter {
	
	private double endLon, endLat, startLon, startLat, stepLon, stepLat, rangeLon, rangeLat;
	private int regionsLon, regionsLat;
	private Region[][] regions;
	private Reader reader;
	private String path;

	public Splitter() {
		init();
		setup();
	}
	
	public Splitter(String inputPath, String regionsLat, String regionsLon, String endLat, String endLon, String startLat, String startLon) {
		path = inputPath;
		try {
			this.regionsLat = Integer.parseInt(regionsLat);
			this.regionsLon = Integer.parseInt(regionsLon);
			this.endLat = Double.parseDouble(endLat);
			this.endLon = Double.parseDouble(endLon);
			this.startLat = Double.parseDouble(startLat);
			this.startLon = Double.parseDouble(startLon);
		}
		catch(NumberFormatException nfe) {
			nfe.printStackTrace();
		}
		setup();
	}
	
	public void setup() {
		reader = new Reader(path);
		rangeLon = endLon - startLon;
		rangeLat = endLat - startLat;
		stepLon = rangeLon / regionsLon;
		stepLat = rangeLat / regionsLat;
		regions = new Region[regionsLon][regionsLat];
		int regCount = 0;
		for(int i=0; i<regionsLon; i++) {
			for(int k=0; k<regionsLat; k++) {
				regions[i][k] = new Region(regCount, startLat + (k+1)*stepLat, startLon + (i+1)*stepLon, startLat + k*stepLat, startLon + i*stepLon);
				regCount++;
			}
		}
	}
	
	public void run() {
		String line = null;
		boolean matched = false;
		int lineCount = 0;
		while((line = reader.read()) != null) {
			lineCount++;
			double lat = getLat(line);
			double lon = getLon(line);
			System.out.println("checking coords " + lon + " " + lat);
			double x = (lon - startLon) / stepLon;
			double y = (lat - startLat) / stepLat;
			int xreg, yreg;
			if((xreg = (int) x) <= regionsLon && (yreg = (int) y) <= regionsLat) {
				if(x == regionsLon) xreg = ((int) x) - 1;
				if(y == regionsLat) yreg = ((int) y) - 1;
				regions[xreg][yreg].add(line);
				System.out.println("added to region " + regions[xreg][yreg].getID());
				matched = true;
			}
			if(matched == false) {
				System.out.println("no match");
			}
		}
		closeAll();
		System.out.println("splitted " + lineCount + " datasets");
	}
	
	private double getLat(String line) {
		return Double.parseDouble(getItems(line)[4]);
	}
	
	private double getLon(String line) {
		return Double.parseDouble(getItems(line)[3]);
	}
	
	private String[] getItems(String line) {
		return line.split(",");
	}
	
	private void init() {
		path = "taxi.csv";
		startLon = 121.38;
		endLon = 121.57;
		startLat = 31.15;
		endLat = 31.32;
		regionsLon = 4;
		regionsLat = 4;
	}
	
	private void closeAll() {
		int count = 0;
		for(int i=0; i<regionsLon; i++) {
			for(int k=0; k<regionsLat; k++) {
				regions[i][k].close();
				System.out.println("region " + count + ": " + regions[i][k].getCount() + " datasets");
				count++;
			}
		}
	}
}