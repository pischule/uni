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