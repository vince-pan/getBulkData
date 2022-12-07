# coding: utf-8
"""
Main Coord class
"""
import numpy as np


class Coord:
    """
    Coord object, coordinate system defined by three points
    """
    def __init__(self, origin_point, z_axis_point, xz_plane_point):
        """
        Initialize the Coord object

        Parameters
        ----------
        origin_point: ndarray
            origin point coordinates in global coordinate system
        z_axis_point: ndarray
            z-axis point coordinates in global coordinate system
        xz_plane_point: ndarray
            xz-plane point coordinates in global coordinate system
        """
        # local coordinate system vectors defined in global coordinate system
        self.z_axis = Vector(origin_point, z_axis_point).normalize()
        self.x_axis = Vector(origin_point, xz_plane_point).normalize()
        self.y_axis = np.cross(self.z_axis, self.x_axis)

        # local coordinate system matrix defined in global coordinate system
        self.matrix = np.array([self.x_axis, self.y_axis, self.z_axis]).transpose()

        # calculate rotation matrix
        self.rotation_matrix = np.dot(np.eye(3), np.linalg.inv(self.matrix))


class Vector:
    """
    Vector object defined by two points
    """
    def __init__(self, point1, point2):
        """
        Initialize the Vector object

        Parameters
        ----------
        point1: ndarray
            first vector point coordinates in global coordinate system
        point2: ndarray
            second vector point coordinates in global coordinate system
        """
        # vector coordinates in global coordinate system
        self.coord = point2 - point1
        # vector magnitude
        self.magnitude = np.linalg.norm(self.coord)

    def normalize(self):
        """
        Return coordinates of normalized vector (x, y, z): ndarray
        """
        return self.coord / self.magnitude
