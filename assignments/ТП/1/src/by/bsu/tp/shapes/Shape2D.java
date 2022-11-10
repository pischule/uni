package by.bsu.tp.shapes;

import java.awt.*;

public abstract class Shape2D extends Shape {
    private Color fillColor;

    public Shape2D(Color borderColor, Point theCenter, Color fillColor) {
        super(borderColor, theCenter);
        this.fillColor = fillColor;
    }

    public Color getFillColor() {
        return fillColor;
    }


    public void setFillColor(Color fillColor) {
        this.fillColor = fillColor;
    }

}
