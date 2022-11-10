package by.bsu.tp.shapes;

import java.awt.*;

public class Rectangle extends WidthHeightShape {

    public Rectangle(Color borderColor, Point theCenter, Color fillColor, int width, int height) {
        super(borderColor, theCenter, fillColor, width, height);
    }

    public Rectangle(Color borderColor, Point theCenter, Color fillColor, Point antherPoint) {
        super(borderColor, theCenter, fillColor, antherPoint);
    }

    @Override
    public void draw(Graphics2D g2d) {
        g2d.setStroke(getStroke());
        g2d.setColor(getFillColor());
        g2d.fillRect(getTheCenter().x - getWidth() / 2, getTheCenter().y - getHeight() / 2, getWidth(), getHeight());
        g2d.setColor(getBorderColor());
        g2d.drawRect(getTheCenter().x - getWidth() / 2, getTheCenter().y - getHeight() / 2, getWidth(), getHeight());
    }
}
