from dataclasses import dataclass
from typing import Optional

from lib.mappers.util.custom_types import Box, Point


@dataclass
class DetectedObject(object):
    box: Box
    confidence: float
    track_id: int = 0
    absolute_position: Optional[Point] = None
