from lib.mappers.util.helper_functions import *


def test_box_bottom_center():
    assert box_bottom_center(((0, 0), (10, 10))) == (5, 10)
    assert box_bottom_center(((0, 0), (1, 1))) == (0, 1)


def test_polygon_to_numpy_array():
    actual = polygon_to_numpy_array([(0, 0), (10, 0), (10, 10), (0, 10)])

    assert isinstance(actual, np.ndarray)
    assert actual.shape == (4, 1, 2)
