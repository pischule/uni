import java.io.*;
import java.util.ArrayList;

public class Main {

    public static void main(String[] args) throws IOException {
        ArrayList<Long> arrayList = new ArrayList<>();

        BufferedReader br = new BufferedReader(new FileReader("input.txt"));
        String s;
        while ((s = br.readLine())!=null) {
            arrayList.add(Long.parseLong(s));
        }

        long sum = arrayList
                .stream()
                .sorted()
                .distinct()
                .reduce(0L, Long::sum);

        PrintWriter pw = new PrintWriter(new FileWriter("output.txt"));
        pw.println(sum);

        br.close();
        pw.close();
    }
}
