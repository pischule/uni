package by.bsu.tp;

import java.awt.*;

public class Util {
    public static int perpendicularDistance(Point p1, Point p2) {
        return Math.min(xDistance(p1, p2), yDistance(p1, p2));
    }

    public static int maxPerpendDistance(Point p1, Point p2) {
        return Math.max(xDistance(p1, p2), yDistance(p1, p2));
    }

    public static double distance(Point p1, Point p2) {
        return Math.hypot(p1.getX() - p2.getX(), p1.getY() - p2.getY());
    }

    public static int xDistance(Point p1, Point p2) {
        return (int) Math.abs(p1.getX() - p2.getX());
    }

    public static int yDistance(Point p1, Point p2) {
        return (int) Math.abs(p1.getY() - p2.getY());
    }
}
