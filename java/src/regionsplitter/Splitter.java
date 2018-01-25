package regionsplitter;

import java.io.FileNotFoundException;

public class Splitter {
	
	private double endLon, endLat, startLon, startLat, stepLon, stepLat, rangeLon, rangeLat;
	private int regionsLon, regionsLat, noMatchCount;
	private Region[][] regions;
	private Reader reader;
	private String path;

	public Splitter() {
		init();
		initCoords();
		setup();
	}
	
	public Splitter(String inputPath, String regionsLat, String regionsLon) {
		path = inputPath;
		noMatchCount = 0;
		try {
			this.regionsLat = Integer.parseInt(regionsLat);
			this.regionsLon = Integer.parseInt(regionsLon);
		}
		catch(NumberFormatException nfe) {
			nfe.printStackTrace();
		}
		initCoords();
		setup();
	}
	
	public Splitter(String inputPath, String regionsLat, String regionsLon, String endLat, String endLon, String startLat, String startLon) {
		path = inputPath;
		noMatchCount = 0;
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
		if(endLon < startLon || endLat < startLat) {
			System.out.println("WARNING: maximum values must be bigger than minimum values!");
		}
		try {
			reader = new Reader(path);
		}
		catch(FileNotFoundException fne) {
			System.out.println("FATAL: input file not found. Terminating.");
			System.exit(0);
		}
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
		System.out.println("Processing begins.");
		while((line = reader.read()) != null) {
			matched = false;
			lineCount++;
			double lat = getLat(line);
			double lon = getLon(line);
			// System.out.println("checking coords " + lon + " " + lat);
			double x = (lon - startLon) / stepLon;
			double y = (lat - startLat) / stepLat;
			int xreg = (int) x;
			int yreg = (int) y;
			// System.out.println(x + " " + y);
			if(x == regionsLon) xreg--;
			if(y == regionsLat) yreg--;
			if(xreg < regionsLon && xreg >= 0 && yreg < regionsLat && yreg >= 0) {
				regions[xreg][yreg].add(line);
				// System.out.println("added to region " + regions[xreg][yreg].getID());
				matched = true;
			}
			if(matched == false) {
				// System.out.println("no match");
				noMatchCount++;
			}
		}
		System.out.println("Processing terminated.");
		System.out.println("splitted " + lineCount + " datasets.");
		closeAll();
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
		regionsLon = 4;
		regionsLat = 4;
	}
	
	private void initCoords() {
		startLon = 121.38;
		endLon = 121.57;
		startLat = 31.15;
		endLat = 31.32;
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
		System.out.println(noMatchCount + " datasets couldn't be added to a region.");
	}
}