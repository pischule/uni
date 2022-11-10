package by.bsu.tp.shapes;

import by.bsu.tp.Util;

import java.awt.*;

public class Circle extends Shape2D {
    private int radius;

    public Circle(Color borderColor, Point theCenter, Color fillColor, int radius) {
        super(borderColor, theCenter, fillColor);
        this.radius = radius;
    }

    public Circle(Color borderColor, Point theCenter, Color fillColor, Point anotherPoint) {
        super(borderColor, theCenter, fillColor);
        updateLastPoint(anotherPoint);
    }

    public int getRadius() {
        return radius;
    }

    public void setRadius(int radius) {
        this.radius = radius;
    }

    @Override
    public void updateLastPoint(Point point) {
        radius = (int) Util.distance(getTheCenter(), point);
    }

    @Override
    public void draw(Graphics2D g2d) {
        g2d.setStroke(getStroke());
        g2d.setColor(getFillColor());
        g2d.fillOval(getTheCenter().x - radius, getTheCenter().y - radius, radius * 2, radius * 2);
        g2d.setColor(getBorderColor());
        g2d.drawOval(getTheCenter().x - radius, getTheCenter().y - radius, radius * 2, radius * 2);
    }

    @Override
    public boolean containsPoint(Point p) {
        return Util.distance(p, getTheCenter()) < radius;
    }
}
