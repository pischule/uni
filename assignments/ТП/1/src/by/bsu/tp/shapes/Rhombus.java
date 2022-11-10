package by.bsu.tp.shapes;

import java.awt.Polygon;
import java.awt.*;

public class Rhombus extends WidthHeightShape {

    public Rhombus(Color borderColor, Point theCenter, Color fillColor, int width, int height) {
        super(borderColor, theCenter, fillColor, width, height);
    }

    public Rhombus(Color borderColor, Point theCenter, Color fillColor, Point antherPoint) {
        super(borderColor, theCenter, fillColor, antherPoint);
    }

    @Override
    public void draw(Graphics2D g2d) {
        Polygon rhombusPolygon = createAwtPolygon();
        g2d.setStroke(getStroke());
        g2d.setColor(getFillColor());
        g2d.fillPolygon(rhombusPolygon);
        g2d.setColor(getBorderColor());
        g2d.drawPolygon(rhombusPolygon);
    }

    private Polygon createAwtPolygon() {
        Polygon rhombusPolygon = new Polygon();
        rhombusPolygon.addPoint(getTheCenter().x - getWidth() / 2, getTheCenter().y);
        rhombusPolygon.addPoint(getTheCenter().x, getTheCenter().y - getHeight() / 2);
        rhombusPolygon.addPoint(getTheCenter().x + getWidth() / 2, getTheCenter().y);
        rhombusPolygon.addPoint(getTheCenter().x, getTheCenter().y + getHeight() / 2);
        return rhombusPolygon;
    }

}
