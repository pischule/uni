package by.bsu.tp.shapes;

import java.awt.*;

public abstract class Shape1D extends Shape {
    private Point p;

    public Shape1D(Color borderColor, Point theCenter, Color fillColor, Point p) {
        super(borderColor, theCenter);
        this.p = p;
    }

    public Point getP() {
        return p;
    }

    public void setP(Point p) {
        this.p = p;
    }

    @Override
    public void move(Point newCenter) {
        int xDelta = newCenter.x - getTheCenter().x;
        int yDelta = newCenter.y - getTheCenter().y;

        super.move(newCenter);
        p.x += xDelta;
        p.y += yDelta;
    }

    @Override
    public void updateLastPoint(Point point) {
        p = point;
    }
}
