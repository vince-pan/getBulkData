# coding: utf-8
"""

"""
import numpy as np


class Coord:
    """
    """
    def __init__(self, origin_point, z_axis_point, xz_plane_point):
        """
        """
        # local coordinate system vectors defined in global coordinate system
        self.x_vector = Vector(origin_point, xz_plane_point)
        self.z_vector = Vector(origin_point, z_axis_point)
        self.y_vector = self._get_coord_y_vector()

        # local coordinate system matrix defined in global coordinate system
        self.matrix = np.array([[self.x_vector.x, self.y_vector.x, self.z_vector.x],
                               [self.x_vector.y, self.y_vector.y, self.z_vector.y],
                               [self.x_vector.z, self.y_vector.z, self.z_vector.z]])

        # calculate transformation matrix
        self.transformation_matrix = np.dot(np.eye(3), np.linalg.inv(self.matrix))

    def _get_coord_y_vector(self):
        """

        Returns
        -------

        """
        vector_y = np.cross([self.x_vector.x, self.x_vector.y, self.x_vector.z],
                            [self.z_vector.x, self.z_vector.y, self.z_vector.z])

        return Vector(Point(0, 0, 0), Point(vector_y[0], vector_y[1], vector_y[2]))


class Vector:
    """
    """
    def __init__(self, point1, point2):
        self.x = point2.x - point1.x
        self.y = point2.y - point1.y
        self.z = point2.z - point1.z
        self.magnitude = np.sqrt(self.x**2 + self.y**2 + self.z**2)


class Point:
    """
    """
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z
