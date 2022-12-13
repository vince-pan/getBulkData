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
        self.x_vector = Vector(origin_point, xz_plane_point).normalize()
        self.z_vector = Vector(origin_point, z_axis_point).normalize()
        self.y_vector = self._get_coord_y_vector(origin_point)

        # local coordinate system matrix defined in global coordinate system
        self.matrix = np.array([[self.x_vector[0], self.y_vector[0], self.z_vector[0]],
                                [self.x_vector[1], self.y_vector[1], self.z_vector[1]],
                                [self.x_vector[2], self.y_vector[2], self.z_vector[2]]])
        # calculate transformation matrix
        self.transformation_matrix = np.dot(np.eye(3), np.linalg.inv(self.matrix))

    def _get_coord_y_vector(self, origin_point):
        """

        Returns
        -------

        """
        return np.cross([self.z_vector[0], self.z_vector[1], self.z_vector[2]],
                        [self.x_vector[0], self.x_vector[1], self.x_vector[2]])


class Vector:
    """
    Vector object
    """

    def __init__(self, point1, point2):
        """
        """
        # define dictionnary of vector coordinates
        self.coords = {"x": point2.x - point1.x,
                       "y": point2.y - point1.y,
                       "z": point2.z - point1.z, }
        # compute vector magnitude
        self.magnitude = np.linalg.norm(list(self.coords.values()))

    def normalize(self):
        """
        Normalize vector by dividing each of its components by its magnitude
        """
        return np.array([self.coords["x"] / self.magnitude,
                         self.coords["y"] / self.magnitude,
                         self.coords["z"] / self.magnitude])


class Point:
    """
    """
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z
