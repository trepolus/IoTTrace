package regionsplitter;

public class Main {

	public static void main(String[] args) {
		Splitter splitter;
		if(args.length == 0) {
			System.out.println("no specific parameters specified. use default values and input file 'taxi.csv'");
			System.out.println("Use: input file, number of regions longitude, number of regions latitude. This includes the standard coordinates.");
			System.out.println("Use: input file, number of regions longitude, number of regions latitude, highest latitude, highest longitude, lowest latitude, lowest longitude");
			splitter = new Splitter();
		}
		else if(args.length == 7) {
			splitter = new Splitter(args[0], args[1], args[2], args[3], args[4], args[5], args[6]);
		}
		else if(args.length == 3) {
			splitter = new Splitter(args[0], args[1], args[2]);
		}
		else {
			System.out.println("FATAL: impossible to initialize Program.");
			return;
		}
		splitter.run();
	}
}
