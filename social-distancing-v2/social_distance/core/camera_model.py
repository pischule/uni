import dataclasses
from typing import List, Tuple
import json


@dataclasses.dataclass
class Camera:
    name: str
    address: str
    side_length: float
    roi: List[Tuple[int, int]]
    square: List[List[float]]
    preview_square: List[List[float]]

    def to_json(self):
        return json.dumps(dataclasses.asdict(self))

    @staticmethod
    def from_json(json_str: str):
        return Camera(**json.loads(json_str))