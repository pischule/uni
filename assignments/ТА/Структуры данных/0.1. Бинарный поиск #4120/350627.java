import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.stream.Collectors;

public class Main {

    static int binarySearch(ArrayList<Integer> arrayList, int value) {
        int l = 0, r = arrayList.size();
        int k;
        while (l < r) {
            k = (l + r) / 2;
            if (value <= arrayList.get(k)) {
                r = k;
            } else {
                l = k + 1;
            }
        }
        return l;
    }

    public static void main(String[] args) throws IOException {
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));

        br.readLine();
        ArrayList<Integer> arrayList = Arrays.stream(br.readLine().split(" "))
                .map(Integer::parseInt)
                .collect(Collectors.toCollection(ArrayList::new));

        br.readLine();
        ArrayList<Integer> requests = Arrays.stream(br.readLine().split(" "))
                .map(Integer::parseInt)
                .collect(Collectors.toCollection(ArrayList::new));

        StringBuilder sb = new StringBuilder();
        for (int r: requests) {
            int lowerBoundary = binarySearch(arrayList, r);
            int nextNumLowerBoundary = binarySearch(arrayList, r+1);
            if (lowerBoundary >= arrayList.size() || arrayList.get(lowerBoundary) != r) {
                sb.append("0 ");
            } else {
                sb.append("1 ");
            }
            sb.append(lowerBoundary).append(" ").append(nextNumLowerBoundary).append("\n");
        }
        System.out.print(sb.toString());

        br.close();
    }


}