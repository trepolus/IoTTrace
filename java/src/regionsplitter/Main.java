package regionsplitter;

public class Main {

	public static void main(String[] args) {
		Splitter splitter;
		if(args.length == 0) splitter = new Splitter();
		else {
			splitter = new Splitter(args[0], args[1], args[2], args[3], args[4], args[5], args[6]);
		}
		splitter.run();
	}
}
