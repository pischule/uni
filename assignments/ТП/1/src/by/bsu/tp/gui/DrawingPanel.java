package by.bsu.tp.gui;

import by.bsu.tp.shapes.Shape;

import javax.swing.*;
import java.awt.*;
import java.util.ArrayList;

public class DrawingPanel extends JPanel {
    private ArrayList<Shape> shapes;

    public DrawingPanel(ArrayList<Shape> shapes) {
        super();
        this.shapes = shapes;
    }

    public ArrayList<Shape> getShapes() {
        return shapes;
    }

    public void setShapes(ArrayList<Shape> shapes) {
        this.shapes = shapes;
    }

    @Override
    protected void paintComponent(Graphics g) {
        super.paintComponent(g);
        Graphics2D g2d = (Graphics2D) g;
        g2d.setRenderingHint(RenderingHints.KEY_ANTIALIASING, RenderingHints.VALUE_ANTIALIAS_ON);
        for (Shape s : shapes)
            s.draw(g2d);
    }
}
