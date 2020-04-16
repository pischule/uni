import java.io.*;
import java.util.*;
import java.util.stream.Collectors;


public class Main implements Runnable {

    public static void main(String[] args) {
        new Thread(null, new Main(), "", 128 * 1024 * 1024).start();
    }

    public void run() {
        Tree t = new Tree();
        String s;
        try (BufferedReader br = new BufferedReader(new FileReader("in.txt"))) {
            while ((s = br.readLine()) != null) {
                t.add(Integer.parseInt(s));
            }
        } catch (IOException e) {
            e.printStackTrace();
        }

        t.magick();

        try (BufferedWriter bw = new BufferedWriter(new FileWriter("out.txt"))) {
            t.show(bw);
        } catch (IOException e) {
            e.printStackTrace();
        }
    }
}

class Tree {

    void magick() {
        calcHeights(root);

        ArrayList<Node> treeAsArray = new ArrayList<>();
        exportTreeToArray(treeAsArray, root);

        long maxSemipathLength = treeAsArray
                .stream()
                .mapToLong(n->n.semipathLength)
                .max()
                .orElse(0);

        ArrayList<Node> biggestSeimpathRoots = treeAsArray
                .stream()
                .filter(x->x.semipathLength == maxSemipathLength)
                .collect(Collectors.toCollection(ArrayList::new));

        for (Node n: biggestSeimpathRoots) {
            long l = 1, r = 1;
            if (n.left != null) {
                l = calcTempLeafCount(n.left);
            }
            if (n.right != null) {
                r = calcTempLeafCount(n.right);
            }

            if (n.right == null && n.left == null) // мало ли
                l = 0;

            n.tempLeafCount = l * r;
            multiplyTempLeafCount(n.left, r);
            multiplyTempLeafCount(n.right, l);

            n.leafCount += n.tempLeafCount;
            n.tempLeafCount = 0;
            addTempLeafCountToTotal(n.left);
            addTempLeafCountToTotal(n.right);
        }

        long theBiggestLeafCount = treeAsArray
                .stream()
                .mapToLong(x->x.leafCount)
                .max()
                .orElse(0);

        treeAsArray
                .stream()
                .filter(x->x.leafCount == theBiggestLeafCount)
                .forEach(x->x.toDelete = true);

        deleteMany(root);
    }

    private void deleteMany(Node node) {
        if (node == null)
            return;

        deleteMany(node.left);
        deleteMany(node.right);


        if (node.toDelete) {
            if (node.left == null && node.right == null) {
                replaceChild(node.parent, node, null);
            } else if (node.left == null) {
                node.right.parent = node.parent;
                replaceChild(node.parent, node, node.right);
            } else if (node.right == null) {
                node.left.parent = node.parent;
                replaceChild(node.parent, node, node.left);
            } else {
                Node mostLeft = node.right;

                while (mostLeft.left != null) {
                    mostLeft = mostLeft.left;
                }

                if (mostLeft.right != null)
                    mostLeft.right.parent = mostLeft.parent;


                replaceChild(node.parent, node, mostLeft);
                replaceChild(mostLeft.parent, mostLeft, mostLeft.right);
                mostLeft.parent = node.parent;
                node.left.parent = mostLeft;
                mostLeft.left = node.left;
                mostLeft.right = node.right;
                if (mostLeft.right == mostLeft)
                    mostLeft.right = null;

            }
        }

    }

    static void addTempLeafCountToTotal(Node node) {
        if (node == null) return;
        ArrayDeque<Node> toVisitStack = new ArrayDeque<>();
        toVisitStack.addLast(node);
        Node n;

        while (!toVisitStack.isEmpty()) {
            n = toVisitStack.removeLast();
            if (n.left != null && n.height == n.left.height + 1)
                toVisitStack.addLast(n.left);
            if (n.right != null && n.height == n.right.height + 1)
                toVisitStack.addLast(n.right);
            n.leafCount += n.tempLeafCount;
            n.tempLeafCount = 0;
        }
    }

    static void multiplyTempLeafCount(Node node, long multiplier) {
        if (node == null)
            return;

        if (node.left != null && node.height == 1+ node.left.height)
            multiplyTempLeafCount(node.left, multiplier);
        if (node.right != null && node.height == 1 + node.right.height)
            multiplyTempLeafCount(node.right, multiplier);

        node.tempLeafCount *= multiplier;
    }

    static long calcTempLeafCount(Node node) {
        long sum = 0;

        if (node.left == null && node.right == null) {
            sum = 1;
        }

        if (node.left != null && node.height == node.left.height + 1) {
            calcTempLeafCount(node.left);
            sum += node.left.tempLeafCount;
        }

        if (node.right != null && node.height == node.right.height + 1) {
            calcTempLeafCount(node.right);
            sum += node.right.tempLeafCount;
        }

        node.tempLeafCount = sum;
        return node.tempLeafCount;
    }

    static void exportTreeToArray(ArrayList<Node> arrayList, Node node) {
        if (node == null)
            return;

        exportTreeToArray(arrayList, node.left);
        exportTreeToArray(arrayList, node.right);
        arrayList.add(node);
    }

    static int calcHeights(Node node) {
        if (node.left == null && node.right == null) {
            node.height = 0;
            node.semipathLength = 0;
        }
        else if (node.left == null) {
            node.height = calcHeights(node.right) + 1;
            node.semipathLength = node.height;
        } else if (node.right == null) {
            node.height = calcHeights(node.left) + 1;
            node.semipathLength = node.height;
        } else {
            int l = calcHeights(node.left) + 1;
            int r = calcHeights(node.right) + 1;
            node.height = Math.max(l, r);
            node.semipathLength = l + r;
        }
        return node.height;
    }

    protected Node root;

    Tree() {
        root = null;
    }

    /**
     * Добавляет вершину со значением value в дерево
     * @param value значение вершины
     */
    void add(int value) {
        if (root == null) {
            root = new Node(value, null);
        } else {
            Node currentNode = root;
            while (currentNode.value != value) {
                if (value < currentNode.value) {
                    if (currentNode.left == null) {
                        currentNode.left = new Node(value, currentNode);
                    }
                    currentNode = currentNode.left;
                } else { // if value > currentNode.v
                    if (currentNode.right == null) {
                        currentNode.right = new Node(value, currentNode);
                    }
                    currentNode = currentNode.right;
                }
            }
        }
    }



    private static Node findMostLeft(Node node) {
        if (node.left == null)
            return node;
        return findMostLeft(node.left);
    }

    /**
     * Меняет сына oldNode вершины parentNode на newNode
     */
    private void replaceChild(Node parentNode, Node oldNode, Node newNode) {
        if (parentNode == null) {
            root = newNode;
        } else if (parentNode.left == oldNode) {
            parentNode.left = newNode;
        } else if (parentNode.right == oldNode) {
            parentNode.right = newNode;
        }
    }

    /**
     * Выводит дерево в writer
     * @param writer
     * @throws IOException
     */
    void show(Writer writer) throws IOException {
        if (root == null) {
            return;
        }

        Deque<Node> nodeStack = new ArrayDeque<>();
        nodeStack.addLast(root);
        Node node;
        while (!nodeStack.isEmpty()) {
            node = nodeStack.removeLast();

            if (!node.toDelete)
                writer.write(node.value + "\n");

            // System.out.prlongln(node);

            if (node.right != null) {
                nodeStack.addLast(node.right);
            }

            if (node.left != null) {
                nodeStack.addLast(node.left);
            }
        }
    }
}

class Node {
    Node left;
    Node right;

    Node parent;
    int value;
    int height;
    int semipathLength;
    long leafCount;
    long tempLeafCount;
    boolean toDelete;

    Node(int value, Node parent) {
        left = null;
        right = null;
        this.value = value;
        this.parent = parent;
        this.height = 0;
        this.semipathLength = 0;
        this.leafCount = 0;
        this.tempLeafCount = 0;
        this.toDelete = false;
    }

    @Override
    public String toString() {
        return "Node{" +
                "value=" + value +
                ", height=" + height +
                ", semipathLenght=" + semipathLength +
                ", leafCount=" + leafCount +
                ", tempLeafCount=" + tempLeafCount +
                ", toDelete=" + toDelete +
                '}';
    }

    @Override
    public boolean equals(Object o) {
        if (this == o) return true;
        if (o == null || getClass() != o.getClass()) return false;
        Node node = (Node) o;
        return value == node.value;
    }

    @Override
    public int hashCode() {
        return Objects.hash(value);
    }
}
