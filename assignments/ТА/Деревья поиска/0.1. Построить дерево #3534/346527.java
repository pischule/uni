import java.io.*;
import java.util.ArrayDeque;
import java.util.ArrayList;
import java.util.Deque;

public class Main {

    public static void main(String[] args) throws IOException {
        Tree t = new Tree();

        String line;
        BufferedReader br = new BufferedReader(new FileReader("input.txt"));
        while ((line = br.readLine()) != null) {
            t.add(Integer.parseInt(line));
        }


        BufferedWriter bw = new BufferedWriter(new FileWriter("output.txt"));

        t.show(bw);

        br.close();
        bw.close();
    }

}

class Tree {
    private Node root;

    Tree() {
        root = null;
    }

    void add(int value) {
        if (root == null) {
            root = new Node(value);
        } else {
            Node currentNode = root;
            while (currentNode.v != value) {
                if (value < currentNode.v) {
                    if (currentNode.l == null) {
                        currentNode.l = new Node(value);
                    }
                    currentNode = currentNode.l;
                } else { // if value > currentNode.v
                    if (currentNode.r == null) {
                        currentNode.r = new Node(value);
                    }
                    currentNode = currentNode.r;
                }
            }
        }
    }

    void show(Writer writer) throws IOException {
        if (root == null) {
            return;
        }

        Deque<Node> nodeStack = new ArrayDeque<>();
        nodeStack.addLast(root);
        Node node;
        while (!nodeStack.isEmpty()) {
            node = nodeStack.removeLast();

            writer.write(node.v + "\n");

            if (node.r != null) {
                nodeStack.addLast(node.r);
            }

            if (node.l != null) {
                nodeStack.addLast(node.l);
            }

        }
    }

    public static void recursiveShow(Node node, Writer writer) throws IOException {
        if (node == null) {
            return;
        }

        writer.write(node.v + "\n");
        recursiveShow(node.l, writer);
        recursiveShow(node.r, writer);

    }

}

class Node {
    Node l;
    Node r;
    int v;

    Node(int value) {
        l = null;
        r = null;
        v = value;
    }
}
