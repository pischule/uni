import numpy as np

from vision.mappers.util.custom_types import Box, Point, Polygon


def box_bottom_center(box: Box) -> Point:
    return (
        box[0][0] + (box[1][0] - box[0][0]) // 2,
        box[1][1],
    )


def polygon_to_numpy_array(polygon: Polygon) -> np.ndarray:
    return np.asarray(polygon, np.int32).reshape((-1, 1, 2))
