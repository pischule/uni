from dataclasses import dataclass, field
from typing import Tuple, Iterable, List, Optional, Dict

import numpy as np
from PySide6 import QtCore

Color = Tuple[int, int, int]

Point = Tuple[int, int]

Tetragon = Tuple[Point, Point, Point, Point]


class Polygon(list):
    def __init__(self, points: Iterable[Point]):
        super().__init__(points)

    def __repr__(self):
        return f"Polygon({super().__repr__()})"

    def to_ndarray(self, dtype=np.int32) -> np.ndarray:
        return np.asarray(self, dtype).reshape((-1, 1, 2))


@dataclass
class Rectangle:
    x: int
    y: int
    width: int
    height: int

    @property
    def bottom_center(self) -> Point:
        return (self.x + self.width // 2, self.y + self.height)

    def to_points(self) -> List[Point]:
        return [
            (self.x, self.y),
            (self.x + self.width, self.y),
            (self.x + self.width, self.y + self.height),
            (self.x, self.y + self.height)
        ]

    def to_ndarray(self, dtype=np.int32) -> np.ndarray:
        return np.asarray(self.to_points(), dtype).reshape((-1, 1, 2))

    def __mul__(self, scaling_factor: float) -> "Rectangle":
        return Rectangle(*(int(x * scaling_factor) for x in (self.x, self.y, self.width, self.height)))

    def to_qrect(self) -> QtCore.QRect:
        return QtCore.QRect(self.x, self.y, self.width, self.height)


@dataclass
class DetectedObject(object):
    rect: Rectangle
    absolute_position: Optional[Point] = None
    safe: bool = True
    distance_to_others: List[float] = field(default_factory=list)

    def to_dict(self):
        return {
            'rect': self.rect.to_points(),
            'absolute_position': np.array(self.absolute_position, dtype=float).tolist(),
            'safe': bool(self.safe)
        }


@dataclass
class FrameContext(object):
    frame: np.ndarray = None
    frame_number: int = 0
    detected_objects: List[DetectedObject] = field(default_factory=list)
    fps: float = 0.0
    statistics: Dict[str, int] = field(default_factory=dict)