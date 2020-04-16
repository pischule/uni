import java.io.*;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.Objects;

public class Main {

    public static void main(String[] args) throws IOException {
        BufferedReader br = new BufferedReader(new FileReader("in.txt"));
        PrintWriter pw = new PrintWriter("out.txt");

        String s = br.readLine();
        int n = Integer.parseInt(br.readLine());
        ArrayList<String> words = new ArrayList<>(n);
        for (int i = 0; i < n; ++i) {
            words.add(br.readLine());
        }

        Task task = new Task(s, words);

        IntWithString iws = task.f(0, s.length()-1);
        if (iws.i != Integer.MAX_VALUE) {
            pw.println(iws.i);
            pw.println(iws.s);
        } else {
            pw.println("No solution");
        }

        br.close();
        pw.close();
    }
}

class Pair{
    int a, b;

    public Pair(int a, int b) {
        this.a = a;
        this.b = b;
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

class Task {
    String line;
    HashMap<Pair, IntWithString> cache;
    HashMap<String, String> numToWord;

    public Task(String line, ArrayList<String> words) {
        this.line = line;
        this.cache = new HashMap<>();
        this.numToWord = new HashMap<>();
        for (String w: words) {
            numToWord.putIfAbsent(WordTransformer.transform(w), w);
        }
    }

    IntWithString f(int start, int end) {
        if (cache.containsKey(new Pair(start, end)))
            return cache.get(new Pair(start, end));
        if (numToWord.containsKey(line.substring(start, end+1)))
            return new IntWithString(1, numToWord.get(line.substring(start, end+1)));


        IntWithString minVal = new IntWithString(Integer.MAX_VALUE, "");
        for (int j = start; j < end; ++j) {
            IntWithString a = f(start, j);
            IntWithString b = f(j+1, end);
            if (a.i != Integer.MAX_VALUE && b.i != Integer.MAX_VALUE) {
                if (a.i + b.i < minVal.i) {
                    minVal = a.add(b);
                }
            }
        }
        cache.put(new Pair(start, end), minVal);
        return minVal;
    }
}
class IntWithString {
    public IntWithString(int i, String s) {
        this.i = i;
        this.s = s;
    }

    public IntWithString add(IntWithString second) {
        return new IntWithString(i + second.i, s + " " + second.s);
    }

    int i;
    String s;
}


class WordTransformer {
    static HashMap<Character, Character> charMap;
    static String transform(String chars) {
        StringBuilder sb = new StringBuilder();
        for (int i = 0; i < chars.length(); ++i) {
            sb.append(charMap.get(chars.charAt(i)));
        }
        return sb.toString();
    }

    static {
        charMap = new HashMap<>();
        charMap.put('1', '1');
        charMap.put('2', '2');
        charMap.put('3', '3');
        charMap.put('4', '4');
        charMap.put('5', '5');
        charMap.put('6', '6');
        charMap.put('7', '7');
        charMap.put('8', '8');
        charMap.put('9', '9');
        charMap.put('I', '1');
        charMap.put('J', '1');
        charMap.put('A', '2');
        charMap.put('B', '2');
        charMap.put('C', '2');
        charMap.put('D', '3');
        charMap.put('E', '3');
        charMap.put('F', '3');
        charMap.put('G', '4');
        charMap.put('H', '4');
        charMap.put('K', '5');
        charMap.put('L', '5');
        charMap.put('M', '6');
        charMap.put('N', '6');
        charMap.put('P', '7');
        charMap.put('R', '7');
        charMap.put('S', '7');
        charMap.put('T', '8');
        charMap.put('U', '8');
        charMap.put('V', '8');
        charMap.put('W', '9');
        charMap.put('X', '9');
        charMap.put('Y', '9');
        charMap.put('O', '0');
        charMap.put('Q', '0');
        charMap.put('Z', '0');
    }
}
