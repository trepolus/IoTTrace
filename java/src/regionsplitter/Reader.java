package regionsplitter;
import java.io.BufferedReader;
import java.io.FileNotFoundException;
import java.io.FileReader;
import java.io.IOException;

public class Reader {

	private BufferedReader reader;
	
	public Reader(String path) throws FileNotFoundException {
		reader = new BufferedReader(new FileReader(path));
		System.out.println("Reader is ready.");
	}
	
	public String read() {
		String content = "";
		try {
			content = reader.readLine();
		} catch (IOException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		}
		// System.out.println("Read line: " + content);
		return content;
	}
}
