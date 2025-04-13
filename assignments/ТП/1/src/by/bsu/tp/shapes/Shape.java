package by.bsu.tp.shapes;

import java.awt.*;

public abstract class Shape {
    private Color borderColor;
    private Point theCenter;
    private Stroke stroke;

    public Shape(Color borderColor, Point theCenter) {
        this.borderColor = borderColor;
        this.theCenter = new Point(theCenter);
        this.stroke = new BasicStroke(3);
    }

    public Stroke getStroke() {
        return stroke;
    }

    public void setStroke(Stroke stroke) {
        this.stroke = stroke;
    }

    public abstract void updateLastPoint(Point point);

    public boolean containsPoint(Point p) {
        return false;
    }

    public Color getBorderColor() {
        return borderColor;
    }

    public void setBorderColor(Color borderColor) {
        this.borderColor = borderColor;
    }

    public abstract void draw(Graphics2D g2d);

    public void move(Point newCenter) {
        this.theCenter = newCenter;
    }

    public Point getLocation() {
        return theCenter;
    }

    public Point getTheCenter() {
        return theCenter;
    }

    public void setTheCenter(Point theCenter) {
        this.theCenter = theCenter;
    }


}
