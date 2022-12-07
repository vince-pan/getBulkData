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
        self.y_vector = self._get_coord_y_vector(origin_point)

        # local coordinate system matrix defined in global coordinate system
        self.matrix = np.array([[self.x_vector.coords["x"], self.y_vector.coords["x"], self.z_vector.coords["x"]],
                                [self.x_vector.coords["y"], self.y_vector.coords["y"], self.z_vector.coords["y"]],
                                [self.x_vector.coords["z"], self.y_vector.coords["z"], self.z_vector.coords["z"]]])
        # calculate transformation matrix
        self.transformation_matrix = np.dot(np.eye(3), np.linalg.inv(self.matrix))

    def _get_coord_y_vector(self, origin_point):
        """

        Returns
        -------

        """
        vector_y = np.cross([self.x_vector.coords["x"], self.x_vector.coords["y"], self.x_vector.coords["z"]],
                            [self.z_vector.coords["x"], self.z_vector.coords["y"], self.z_vector.coords["z"]])

        return Vector(origin_point, Point(vector_y[0], vector_y[1], vector_y[0]))


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
        self.magnitude = self.magnitude(np.array(list(self.coords.values())))

    def magnitude(self, vector):
        """
        Compute vector magnitude
        """
        return np.linalg.norm(vector)

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
