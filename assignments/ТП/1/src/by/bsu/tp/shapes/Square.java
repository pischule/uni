package by.bsu.tp.shapes;

import by.bsu.tp.Util;

import java.awt.*;

public class Square extends Shape2D {
    private int size;

    public Square(Color borderColor, Point theCenter, Color fillColor, Point anotherPoint) {
        super(borderColor, theCenter, fillColor);
        updateLastPoint(anotherPoint);
    }

    public Square(Color borderColor, Point theCenter, Color fillColor, int size) {
        super(borderColor, theCenter, fillColor);
        this.size = size;
    }

    @Override
    public void updateLastPoint(Point point) {
        size = Util.maxPerpendDistance(point, getTheCenter()) * 2;
    }

    @Override
    public boolean containsPoint(Point p) {
        return Util.maxPerpendDistance(p, getTheCenter()) * 2 < size;
    }

    @Override
    public void draw(Graphics2D g2d) {
        g2d.setColor(getFillColor());
        g2d.fillRect(getTheCenter().x - size / 2, getTheCenter().y - size / 2, size, size);
        g2d.setColor(getBorderColor());
        g2d.drawRect(getTheCenter().x - size / 2, getTheCenter().y - size / 2, size, size);
    }
}
