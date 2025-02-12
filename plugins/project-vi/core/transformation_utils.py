"""
Transformation Utilities module for The Box system.
Provides functions for determining transformations including translations and rotations of geometric entities.
"""

import numpy as np

class TransformationUtils:
    @staticmethod
    def determine_translation_vector(point_a, point_b):
        """
        Computes the translation vector to align point A with point B.

        :param point_a: Starting point
        :param point_b: Target point
        :return: Translation vector
        """
        return np.subtract(point_b, point_a)

    @staticmethod
    def determine_rotation_matrix(axis, theta_rad):
        """
        Computes the rotation matrix for a given axis and angle.

        :param axis: Axis of rotation (should be a normalized vector)
        :param theta_rad: Angle in radians
        :return: Rotation matrix
        """
        axis = np.asarray(axis)
        axis = axis / np.linalg.norm(axis)
        cos_theta = np.cos(theta_rad)
        sin_theta = np.sin(theta_rad)
        u = axis
        R = np.array([[cos_theta + u[0]**2 * (1 - cos_theta), u[0]*u[1]*(1-cos_theta) - u[2]*sin_theta, u[0]*u[2]*(1-cos_theta) + u[1]*sin_theta],
                      [u[1]*u[0]*(1-cos_theta) + u[2]*sin_theta, cos_theta + u[1]**2 * (1 - cos_theta), u[1]*u[2]*(1-cos_theta) - u[0]*sin_theta],
                      [u[2]*u[0]*(1-cos_theta) - u[1]*sin_theta, u[2]*u[1]*(1-cos_theta) + u[0]*sin_theta, cos_theta + u[2]**2 * (1 - cos_theta)]])
        return R

    @staticmethod
    def determine_port_transformation(port_config, component_dimensions):
        """
        Determines transformation needed for a port feature.

        :param port_config: Configuration details of the port
        :param component_dimensions: Dimensions of the component
        :return: A tuple of translation vector and rotation matrix
        """
        # Placeholder implementation: extract and return transform values from configurations
        translation_vector = [port_config.get("x_offset", 0), port_config.get("y_offset", 0), port_config.get("z_offset", 0)]
        axis = port_config.get("rotation_axis", [0, 0, 1])
        angle_rad = np.deg2rad(port_config.get("rotation_angle", 0))
        rotation_matrix = TransformationUtils.determine_rotation_matrix(axis, angle_rad)
        return translation_vector, rotation_matrix