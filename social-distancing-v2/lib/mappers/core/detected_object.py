from dataclasses import dataclass
from typing import Optional

import numpy as np

from lib.mappers.util.custom_types import Box, Point


@dataclass
class DetectedObject(object):
    box: Box
    confidence: float
    track_id: int = 0
    absolute_position: Optional[Point] = None
    safe = True

    def to_dict(self):
        return {
            'box': np.array(self.box, dtype=int).tolist(),
            'confidence': float(self.confidence),
            'track_id': int(self.track_id),
            'absolute_position': np.array(self.absolute_position, dtype=float).tolist(),
            'safe': bool(self.safe)
        }
