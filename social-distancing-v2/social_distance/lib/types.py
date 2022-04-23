from dataclasses import dataclass, field
from typing import Tuple, Iterable, List, Mapping, Optional

import numpy as np

Color = Tuple[int, int, int]

Point = Tuple[int, int]
Box = Tuple[Point, Point]
Polygon = Iterable[Point]

Tetragon = Tuple[Point, Point, Point, Point]


@dataclass
class DetectedObject(object):
    box: Box
    confidence: float
    track_id: int = 0
    absolute_position: Optional[Point] = None
    safe: bool = True
    distance_to_others: List[float] = field(default_factory=list)

    def to_dict(self):
        return {
            'box': np.array(self.box, dtype=int).tolist(),
            'confidence': float(self.confidence),
            'track_id': int(self.track_id),
            'absolute_position': np.array(self.absolute_position, dtype=float).tolist(),
            'safe': bool(self.safe)
        }


@dataclass(init=False)
class FrameContext(object):
    frame: np.ndarray = None
    frame_number: int = 0
    detected_objects: List[DetectedObject] = field(default_factory=list)
    fps: float = 0.0

    violations: int = 0
    violators: int = 0
    violation_clusters: int = 0

    @staticmethod
    def from_frame(frame: np.ndarray, detected_objects=None) -> "FrameContext":
        if detected_objects is None:
            detected_objects = list()
        fc = FrameContext()
        fc.frame = frame.copy()
        fc.detected_objects = detected_objects.copy()
        return fc


class ContextMapper:
    def map(self, context: FrameContext) -> FrameContext:
        pass

    def cleanup(self):
        pass
