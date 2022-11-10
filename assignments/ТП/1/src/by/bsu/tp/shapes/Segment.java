package by.bsu.tp.shapes;

import java.awt.*;

public class Segment extends Ray {
    public Segment(Color borderColor, Point theCenter, Color fillColor, Point p) {
        super(borderColor, theCenter, fillColor, p);
    }

    @Override
    public void draw(Graphics2D g2d) {
        int xDelta = (getP().x - getTheCenter().x);
        int yDelta = (getP().y - getTheCenter().y);

        g2d.setStroke(getStroke());
        g2d.setColor(getBorderColor());
        g2d.drawLine(getTheCenter().x - xDelta, getTheCenter().y - yDelta,
                getTheCenter().x + xDelta, getTheCenter().y + yDelta);
    }
}
