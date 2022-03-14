from dataclasses import dataclass
from typing import Optional

from lib.mappers.util.custom_types import Box


@dataclass
class DetectedObject(object):
    box: Box
    class_name: str
    confidence: float
    track_id: int = 0
