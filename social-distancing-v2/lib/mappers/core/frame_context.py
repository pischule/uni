from dataclasses import dataclass, field
from typing import List, Mapping

import numpy as np

from lib.mappers.core.detected_object import DetectedObject


@dataclass(init=False)
class FrameContext(object):
    frame: np.ndarray = None
    frame_number: int = 0
    detected_objects: List[DetectedObject] = field(default_factory=list)
    fps: float = 0.0

    distances: Mapping[int, float] = field(default_factory=dict)
