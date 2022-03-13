from dataclasses import dataclass

from vision.mappers.util.custom_types import Box


@dataclass
class DetectedObject(object):
    box: Box
    class_name: str
    confidence: float
