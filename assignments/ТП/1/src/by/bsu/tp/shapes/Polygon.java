package by.bsu.tp.shapes;

import java.awt.*;
import java.util.ArrayList;

public class Polygon extends Shape2D {
    private ArrayList<Point> points;

    public Polygon(Color borderColor, Point theCenter, Color fillColor, ArrayList<Point> points) {
        super(borderColor, theCenter, fillColor);
        this.points = points;
    }

    public Polygon(Color borderColor, Point theCenter, Color fillColor, Point p) {
        super(borderColor, theCenter, fillColor);
        points = new ArrayList<>();
        points.add(p);
    }

    @Override
    public void updateLastPoint(Point point) {
        if (points.size() > 0) {
            points.set(points.size() - 1, point);
        }
    }

    public void addPoint(Point point) {
        points.add(point);
    }

    public ArrayList<Point> getPoints() {
        return points;
    }

    public void setPoints(ArrayList<Point> points) {
        this.points = points;
    }

    @Override
    public boolean containsPoint(Point p) {
        return createAwtPolygon().contains(p);
    }

    @Override
    public void move(Point newCenter) {
        int delta_x = newCenter.x - getTheCenter().x;
        int delta_y = newCenter.y - getTheCenter().y;
        super.move(newCenter);
        points.forEach((p)->{
            p.x += delta_x;
            p.y += delta_y;
        });

    }

    @Override
    public void draw(Graphics2D g2d) {
        var polygon = createAwtPolygon();
        g2d.setColor(getFillColor());
        g2d.fillPolygon(polygon);
        g2d.setColor(getBorderColor());
        g2d.drawPolygon(polygon);
    }

    private java.awt.Polygon createAwtPolygon() {
        java.awt.Polygon polygon = new java.awt.Polygon();
        polygon.addPoint(getTheCenter().x, getTheCenter().y);
        points.forEach(p -> polygon.addPoint(p.x, p.y));
        return polygon;
    }
}
