package by.bsu.tp.shapes;

import by.bsu.tp.Util;

import java.awt.*;

public abstract class WidthHeightShape extends Shape2D {
    private int width;
    private int height;

    public WidthHeightShape(Color borderColor, Point theCenter, Color fillColor, int width, int height) {
        super(borderColor, theCenter, fillColor);
        this.width = width;
        this.height = height;
    }

    public WidthHeightShape(Color borderColor, Point theCenter, Color fillColor, Point antherPoint) {
        super(borderColor, theCenter, fillColor);
        updateLastPoint(antherPoint);
    }

    @Override
    public void updateLastPoint(Point point) {
        width = 2 * Util.xDistance(getTheCenter(), point);
        height = 2 * Util.yDistance(getTheCenter(), point);
    }


    public int getWidth() {
        return width;
    }

    public void setWidth(int width) {
        this.width = width;
    }

    public int getHeight() {
        return height;
    }

    public void setHeight(int height) {
        this.height = height;
    }

    @Override
    public boolean containsPoint(Point p) {
        return Math.abs(p.x - getTheCenter().x) < width / 2 &&
                Math.abs(p.y - getTheCenter().y) < height / 2;
    }
}
