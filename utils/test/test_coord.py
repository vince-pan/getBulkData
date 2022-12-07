# coding: utf-8
from unittest import TestCase
from utils.coord import Vector, Coord

import numpy as np


class TestCoord(TestCase):
    def setUp(self):
        origin = np.array([0., 0., 0.])
        z_axis = np.array([0.61, -0.22, 0.76])
        xz_plane = np.array([0.79, 0.24, -0.56])
        self.coord = Coord(origin, z_axis, xz_plane)

    def test_y_axis(self):
        self.assertTrue(np.allclose(np.round(self.coord.y_axis, 2), np.array([-0.06, 0.95, 0.32])))

    def test_matrix(self):
        self.assertTrue(np.allclose(np.round(self.coord.matrix, 2), np.array([[0.79, -0.06, 0.61],
                                                                              [0.24, 0.95, -0.22],
                                                                              [-0.56, 0.32, 0.76]])))

    def test_rotation_matrix(self):
        self.assertTrue(np.allclose(np.round(self.coord.rotation_matrix, 2), np.array([[0.79, 0.24, -0.56],
                                                                                       [-0.06, 0.95, 0.32],
                                                                                       [0.61, -0.22, 0.76]])))


class TestVector(TestCase):
    def setUp(self):
        point1 = np.array([3, 6, -9])
        point2 = np.array([33, -9, 21])
        self.vector = Vector(point1, point2)

    def test_coord(self):
        self.assertTrue(np.allclose(self.vector.coord, [30, -15, 30]))

    def test_magnitude(self):
        self.assertEqual(self.vector.magnitude, 45.0)

    def test_normalize_coord(self):
        self.assertTrue(np.allclose(np.round(self.vector.normalize(), 2), np.array([0.67, -0.33, 0.67])))

    def test_normalize_magnitude(self):
        mag = np.sqrt(self.vector.normalize()[0]**2 + self.vector.normalize()[1]**2 + self.vector.normalize()[2]**2)
        self.assertEqual(mag, 1)
