"""
Mechanics Math module for The Box system.
This module provides functions to calculate mechanical principles, such as forces and motion analysis.
"""

import numpy as np

class MechanicsMath:
    @staticmethod
    def force_calculation(mass, acceleration):
        """
        Computes force using Newton's second law.

        :param mass: The mass of the object
        :param acceleration: The acceleration of the object
        :return: Force
        """
        return mass * acceleration

    @staticmethod
    def torque_calculation(force, lever_arm_length, angle_rad):
        """
        Computes the torque produced by a force applied at a distance.

        :param force: The force applied
        :param lever_arm_length: The length of the lever arm
        :param angle_rad: Angle in radians between force and lever arm
        :return: Torque
        """
        return force * lever_arm_length * np.sin(angle_rad)