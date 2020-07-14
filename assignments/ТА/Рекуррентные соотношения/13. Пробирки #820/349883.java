import java.io.*;
import java.util.ArrayDeque;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.stream.Collectors;

public class Main implements Runnable{

    public static void main(String[] args) throws IOException {
        new Thread(null, new Main(), "", 64 * 1024 * 1024).start();
    }

    public void run() {
        int x, k, l;

        try {
            BufferedReader br = new BufferedReader(new FileReader("in.txt"));

            PrintWriter pw = new PrintWriter("out.txt");

            x = Integer.parseInt(br.readLine());
            k = Integer.parseInt(br.readLine());
            l = Integer.parseInt(br.readLine());
            ArrayList<Integer> d = Arrays.stream(br.readLine().split(" "))
                    .map(Integer::parseInt)
                    .collect(Collectors.toCollection(ArrayList::new));
            d.remove(d.size()-1);

            Task t = new Task(k, l, x, d);
            int answer = t.calculate();
            pw.println(answer >= 0 ? Integer.toString(answer) : "No solution");

            br.close();
            pw.close();
        } catch (IOException e) {
            e.printStackTrace();
        }

    }
}

class Task {
    boolean[][] matrix;
    ArrayList<Integer> ds;
    int first, second;
    int goal;

    int calculate() {
        ArrayDeque<State> queue = new ArrayDeque<>();
        queue.addLast(new State(first, second, 0));
        State s;
        int k, l, nD;
        while (!queue.isEmpty()) {
            s = queue.removeFirst();
            if (!s.isCorrect() || matrix[s.k][s.l])
                continue;

            matrix[s.k][s.l] = true;

            if (s.isGoal()) {
                return s.d;
            }

            k = s.k;
            l = s.l;
            nD = s.d + 1;
            queue.addLast(new State(0,k + l, nD));
            queue.addLast(new State(k + l, 0, nD));
            queue.addLast(new State(k, 0, nD));
            queue.addLast(new State(0, l, s.d +1));
            queue.addLast(new State(100-l, l, nD));
            queue.addLast(new State(k, 100 - k, nD));

            for (int d: ds) {
                queue.addLast(new State(d, l + k - d, nD));
                queue.addLast(new State(l + k - d, d, nD));
                queue.addLast(new State(d, l, nD));
                queue.addLast(new State(k, d, nD));
            }
        }
        return -1;
    }


    Task(int k, int l, int x, ArrayList<Integer> delimiters) {
        this.first = k;
        this.second = l;
        this.goal = 100 - x;

        this.ds = delimiters;

        matrix = new boolean[101][101];
    }

    void showMatrix() {
        for (int i  = 0; i < 101; ++i) {
            for (int j = 0; j < 101; ++j) {
                System.out.print(matrix[i][j] + " ");
            }
            System.out.println();
        }
    }

    class State {
        int k;
        int l;
        int d;

        boolean isCorrect() {
            return k >= 0 && l >= 0 && k <= 100 && l <= 100 && k + l <= 100;
        }

        public State(int k, int l, int step) {
            this.k = k;
            this.l = l;
            this.d = step;
        }

        boolean isGoal() {
            return k + l == goal;
        }
    }
}
