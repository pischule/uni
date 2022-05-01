import cv2
import numpy as np

from social_distance.core.types import Point, Tetragon


def polygon_to_ndarray(polygon) -> np.ndarray:
    return np.asarray(polygon, np.int32).reshape((-1, 1, 2))


def point_to_tetragon(point: Point) -> Tetragon:
    return (
        (0, 0),  # Top left
        (point[0], 0),  # Top right
        (point[0], point[1]),  # Bottom right
        (0, point[1]),  # Bottom left
    )


def square_perspective_transform_matrix(box: Tetragon, target_square_side: float) -> np.ndarray:
    """
    Calculate a perspective transform matrix for a square to be transformed to a target square side.
    :param box: The box to be transformed.
    :param target_square_side: The target square side.
    :return: The perspective transform matrix.
    """
    # Calculate the perspective transform matrix.
    perspective_transform_matrix = cv2.getPerspectiveTransform(
        src=box.to_ndarray(dtype=np.float32),
        dst=np.array(
            [
                [0, 0],
                [target_square_side, 0],
                [target_square_side, target_square_side],
                [0, target_square_side],
            ],
            dtype=np.float32,
        ),
    )

    return perspective_transform_matrix
