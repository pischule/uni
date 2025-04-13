import java.io.*;
import java.util.ArrayDeque;
import java.util.Deque;

public class Main {

    public static void main(String[] args) throws IOException {
        Tree t = new Tree();

        String line;
        BufferedReader br = new BufferedReader(new FileReader("input.txt"));

        int nodeToDelete = Integer.parseInt(br.readLine());
        br.readLine();

        while ((line = br.readLine()) != null) {
            t.add(Integer.parseInt(line));
        }

        t.deleteNode(nodeToDelete);

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

    public void deleteNode(int nodeVal) {
        Node parentNode = null;
        Node node = root;

        while (true) {
            if (node == null) {
                return;
            }
            if (nodeVal < node.v) {
                parentNode = node;
                node = node.l;
            } else if (nodeVal > node.v) {
                parentNode = node;
                node = node.r;
            } else {
                break;
            }
        }

        if (node.l == null && node.r == null) {
            replace_node(parentNode, node, null);
        } else if (node.l == null) {
            replace_node(parentNode, node, node.r);
        } else if (node.r == null) {
            replace_node(parentNode, node, node.l);
        } else {
            Node minNodeParent = node;
            Node minNode = node.r;

            while (minNode.l != null) {
                minNodeParent = minNode;
                minNode = minNode.l;
            }

            node.v = minNode.v;
            replace_node(minNodeParent, minNode, minNode.r);
        }
    }

    private void replace_node(Node parentNode, Node oldNode, Node newNode) {
        if (parentNode == null) {
            root = newNode;
        } else if (parentNode.l == oldNode) {
            parentNode.l = newNode;
        } else if (parentNode.r == oldNode) {
            parentNode.r = newNode;
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
