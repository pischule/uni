import java.io.*;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.Objects;

public class Main {

    static HashMap<Pair, Long> cache = new HashMap<>();

    static ArrayList<Pair> a = new ArrayList<>();

    public static void main(String[] args) throws IOException {
        BufferedReader br = new BufferedReader(new FileReader("input.txt"));
        PrintWriter pw = new PrintWriter(new FileWriter("output.txt"));

        String[] s_arr;
        int x, y;

        int n = Integer.parseInt(br.readLine());
        for (int i = 0; i < n; ++i) {
            s_arr = br.readLine().split(" ");
            x = Integer.parseInt(s_arr[0]);
            y = Integer.parseInt(s_arr[1]);
            a.add(new Pair(x, y));
        }

        pw.println(f(0, n));

        br.close();
        pw.close();
    }

    static long f(int s, int e) {
        if (cache.containsKey(new Pair(s, e))) {
            return cache.get(new Pair(s, e));
        }
        int n = e - s;
        long ops;

        if (n == 1) {
            ops = 0;
        } else {
            ops = Long.MAX_VALUE;
            for (int i = s+1; i < e; ++i) {
                ops = Math.min(ops, f(s,i) + f(i,e) +
                        a.get(s).a * a.get(i).a * a.get(e-1).b);
            }
        }

        cache.put(new Pair(s,e), ops);
        return ops;
    }
}

class Pair {
    int a;
    int b;

    public Pair(int a, int b) {
        this.a = a;
        this.b = b;
    }

    @Override
    public String toString() {
        return "Pair{" +
                "a=" + a +
                ", b=" + b +
                '}';
    }

    @Override
    public boolean equals(Object o) {
        if (this == o) return true;
        if (o == null || getClass() != o.getClass()) return false;
        Pair pair = (Pair) o;
        return a == pair.a &&
                b == pair.b;
    }

    @Override
    public int hashCode() {
        return Objects.hash(a, b);
    }
}
