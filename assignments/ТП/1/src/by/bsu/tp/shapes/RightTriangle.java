package by.bsu.tp.shapes;

import java.awt.Polygon;
import java.awt.*;

public class RightTriangle extends WidthHeightShape {
    public RightTriangle(Color borderColor, Point theCenter, Color fillColor, int width, int height) {
        super(borderColor, theCenter, fillColor, width, height);
    }

    public RightTriangle(Color borderColor, Point theCenter, Color fillColor, Point antherPoint) {
        super(borderColor, theCenter, fillColor, antherPoint);
    }

    @Override
    public void draw(Graphics2D g2d) {
        Polygon poly = createAwtPolygon();
        g2d.setStroke(getStroke());
        g2d.setColor(getFillColor());
        g2d.fillPolygon(poly);
        g2d.setColor(getBorderColor());
        g2d.drawPolygon(poly);
    }

    private Polygon createAwtPolygon() {
        Polygon poly = new Polygon();
        poly.addPoint(getTheCenter().x - getWidth() / 2, getTheCenter().y + getHeight() / 2);
        poly.addPoint(getTheCenter().x - getWidth() / 2, getTheCenter().y - getHeight() / 2);
        poly.addPoint(getTheCenter().x + getWidth() / 2, getTheCenter().y + getHeight() / 2);
        return poly;
    }
}
