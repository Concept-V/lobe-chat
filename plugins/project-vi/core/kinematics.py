"""
Kinematics module for The Box system.
Defines utility functions for calculations related to motion of components and mechanisms.
"""

import numpy as np

class Kinematics:
    @staticmethod
    def calculate_velocity(distance, time):
        """
        Calculates the velocity of a moving component.

        :param distance: The distance traveled
        :param time: The time taken
        :return: Velocity
        """
        return distance / time

    @staticmethod
    def calculate_acceleration(velocity_initial, velocity_final, time):
        """
        Calculates the acceleration of a moving component.

        :param velocity_initial: Initial velocity
        :param velocity_final: Final velocity
        :param time: The time taken
        :return: Acceleration
        """
        return (velocity_final - velocity_initial) / time

    @staticmethod
    def calculate_rotational_motion(radius, angular_velocity):
        """
        Calculates the linear velocity for rotational motion.

        :param radius: Radius of the circular path
        :param angular_velocity: Angular velocity in radians per second
        :return: Linear velocity
        """
        return radius * angular_velocity