import cv2
import numpy as np

from lib.mappers.util.custom_types import Box, Point, Polygon, Tetragon


def box_bottom_center_point(box: Box) -> Point:
    """
    Calculate the bottom center point of a box.
    :param box:
    :return:
    """
    return (
        box[0][0] + (box[1][0] - box[0][0]) // 2,
        box[1][1],
    )


def polygon_to_ndarray(polygon: Polygon) -> np.ndarray:
    """
    Convert a polygon to a numpy array.
    :param polygon:
    :return:
    """
    return np.asarray(polygon, np.int32).reshape((-1, 1, 2))


def box_to_ndarray(box: Box, dtype: type = np.int32) -> np.ndarray:
    """
    Convert a box to a numpy array.
    :param box:
    :param dtype:
    :return:
    """
    return np.asarray(box, dtype).reshape((-1, 1, 2))


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
        src=box_to_ndarray(box, dtype=np.float32),
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
