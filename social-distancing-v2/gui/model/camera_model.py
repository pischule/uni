import dataclasses
from typing import List, Tuple
import json


@dataclasses.dataclass
class Camera:
    address: str
    transform_matrix: List[List[float]]
    roi: List[Tuple[int, int]]

    def to_json(self):
        return json.dumps(dataclasses.asdict(self))

    @staticmethod
    def from_json(json_str: str):
        return Camera(**json.loads(json_str))


if __name__ == "__main__":
    c = Camera('0', [[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 1, 0], [0, 0, 0, 1]], [(0, 0), (0, 0)])
    print(json.dumps(c.__dict__))
    j = json.dumps(c.__dict__)
    print(Camera.from_json(j))
