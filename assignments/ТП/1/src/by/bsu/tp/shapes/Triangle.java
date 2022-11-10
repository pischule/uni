package by.bsu.tp.shapes;

import java.awt.Polygon;
import java.awt.*;

public class Triangle extends WidthHeightShape {
    public Triangle(Color borderColor, Point theCenter, Color fillColor, int width, int height) {
        super(borderColor, theCenter, fillColor, width, height);
    }

    public Triangle(Color borderColor, Point theCenter, Color fillColor, Point antherPoint) {
        super(borderColor, theCenter, fillColor, antherPoint);
    }

    @Override
    public boolean containsPoint(Point p) {
        return createAwtPolygon().contains(p);
    }

    @Override
    public void draw(Graphics2D g2d) {
        Polygon trianglePolygon = createAwtPolygon();
        g2d.setStroke(getStroke());
        g2d.setColor(getFillColor());
        g2d.fillPolygon(trianglePolygon);
        g2d.setColor(getBorderColor());
        g2d.drawPolygon(trianglePolygon);
    }

    private Polygon createAwtPolygon() {
        Polygon trianglePolygon = new Polygon();
        trianglePolygon.addPoint(getTheCenter().x - getWidth() / 2, getTheCenter().y + getHeight() / 2);
        trianglePolygon.addPoint(getTheCenter().x + getWidth() / 2, getTheCenter().y + getHeight() / 2);
        trianglePolygon.addPoint(getTheCenter().x, getTheCenter().y - getHeight() / 2);
        return trianglePolygon;
    }
}
