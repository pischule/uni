from unittest import TestCase
from vision.mappers.util.helper_functions import *


class Test(TestCase):
    def test_box_bottom_center(self):
        self.assertEqual((5, 10), box_bottom_center(((0, 0), (10, 10))))

    def test_polygon_to_numpy_array(self):
        actual = polygon_to_numpy_array([(0, 0), (10, 0), (10, 10), (0, 10)])

        self.assertIsInstance(actual, np.ndarray)
        self.assertEqual((4, 1, 2), actual.shape)
