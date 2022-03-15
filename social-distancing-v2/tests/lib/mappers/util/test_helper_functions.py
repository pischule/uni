from lib.util import *


def test_box_bottom_center():
    assert box_bottom_center_point(((0, 0), (10, 10))) == (5, 10)
    assert box_bottom_center_point(((0, 0), (1, 1))) == (0, 1)


def test_polygon_to_numpy_array():
    actual = polygon_to_ndarray([(0, 0), (10, 0), (10, 10), (0, 10)])

    assert isinstance(actual, np.ndarray)
    assert actual.shape == (4, 1, 2)
