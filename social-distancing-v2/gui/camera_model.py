import dataclasses
from typing import List, Tuple
import json

import cv2
import numpy as np


@dataclasses.dataclass
class Camera:
    name: str
    address: str
    transform_matrix: List[List[float]]
    roi: List[Tuple[int, int]]

    def to_json(self):
        return json.dumps(dataclasses.asdict(self))

    @staticmethod
    def from_json(json_str: str):
        return Camera(**json.loads(json_str))

    @staticmethod
    def from_wizard(name, address, square_size, square_points, roi) -> 'Camera':
        input_pts = np.asarray(square_points, dtype=np.float32)
        output_pts = np.asarray([[0, 0],
                                 [0, square_size],
                                 [square_size, square_size],
                                 [square_size, 0]], dtype=np.float32)
        mat = cv2.getPerspectiveTransform(input_pts, output_pts)
        return Camera(name, address, mat.tolist(), roi)


if __name__ == "__main__":
    # c = Camera('0', [[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 1, 0], [0, 0, 0, 1]], [(0, 0), (0, 0)])
    # print(json.dumps(c.__dict__))
    # j = json.dumps(c.__dict__)
    # print(Camera.from_json(j))

    c = Camera.from_wizard("1", 100,
                           [(-132.49023090586147, 173.9253996447602), (-47.57371225577265, 206.66429840142095),
                            (-2.0461811722912966, 162.15985790408524), (-74.1740674955595, 145.27886323268206)],
                           [(-172.38336347197108, 69.7866184448463), (-86.45207956600362, 48.95479204339964),
                            (13.01989150090416, 55.725135623869804), (12.499095840867994, 146.86437613019893),
                            (-172.38336347197108, 147.90596745027125)])
