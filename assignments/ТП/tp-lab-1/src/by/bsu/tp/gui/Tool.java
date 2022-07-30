package by.bsu.tp.gui;

import by.bsu.tp.shapes.*;

public enum Tool {
    RECTANGLE("Rectangle", Rectangle.class),
    SQUARE("Square", Square.class),
    CIRCLE("Circle", Circle.class),
    ELLIPSE("Ellipse", Ellipse.class),
    TRIANGLE("Triangle", Triangle.class),
    RIGHT_TRIANGLE("Right trinagle", RightTriangle.class),
    RHOMBUS("Rhombus", Rhombus.class),
    REGULAR_POLYGON("Regular polygon", RegularPolygon.class),
    POLYGON("Polygon", Polygon.class),
    SEGMENT("Segment", Segment.class),
    LINE("Line", Line.class),
    RAY("Ray", Ray.class),
    MOVE("Move", null);


    private final String name;
    private final Class<? extends Shape> shapeClass;

    Tool(String name, Class<? extends Shape> shapeClass) {
        this.name = name;
        this.shapeClass = shapeClass;
    }

    public String getName() {
        return name;
    }

    public Class<? extends Shape> getShapeClass() {
        return shapeClass;
    }
}
