package by.bsu.tp.shapes;

import java.awt.*;

public class Ellipse extends WidthHeightShape {
    public Ellipse(Color borderColor, Point theCenter, Color fillColor, int width, int height) {
        super(borderColor, theCenter, fillColor, width, height);
    }

    public Ellipse(Color borderColor, Point theCenter, Color fillColor, Point antherPoint) {
        super(borderColor, theCenter, fillColor, antherPoint);
    }

    @Override
    public boolean containsPoint(Point p) {
        if (getWidth() == 0 || getHeight() == 0) {
            return false;
        } else {
            return Math.pow((p.x - 1.0 * getTheCenter().x) / getWidth(), 2) +
                    Math.pow((p.y - 1.0 * getTheCenter().y) / getHeight(), 2) < 1;
        }
    }

    @Override
    public void draw(Graphics2D g2d) {
        g2d.setStroke(getStroke());
        g2d.setColor(getFillColor());
        g2d.fillOval(getTheCenter().x - getWidth() / 2, getTheCenter().y - getHeight() / 2,
                getWidth(), getHeight());
        g2d.setColor(getBorderColor());
        g2d.drawOval(getTheCenter().x - getWidth() / 2, getTheCenter().y - getHeight() / 2,
                getWidth(), getHeight());
    }

}
