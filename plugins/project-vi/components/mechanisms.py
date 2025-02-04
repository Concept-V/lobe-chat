"""
Mechanisms module for The Box system.
Defines the abstract Mechanism class (inheriting from Component) and concrete subclasses:
SpiralMechanism, LinearActuator, and StateManager.
"""

import numpy as np
import trimesh
from abc import ABC, abstractmethod
from components import Component

class Mechanism(Component, ABC):
    def __init__(self, name, mechanism_type, dimensions=None, params=None, **kwargs):
        super().__init__(name=name, component_type=mechanism_type, dimensions=dimensions, params=params)
    
    @abstractmethod
    def generate_stl(self):
        pass

class SpiralMechanism(Mechanism):
    def __init__(self, name="Spiral_Mech_Default", pitch=20.0, radius=2.0, thread_depth=0.5, helix_length=25.0,
                 segments_per_rotation=72, flank_angle_deg=30.0, thread_crest_width=1.0, thread_root_width=0.5, **kwargs):
        mech_dimensions = {
            "radius": radius,
            "helix_length": helix_length
        }
        mech_params = {
            "pitch": pitch,
            "segments_per_rotation": segments_per_rotation,
            "flank_angle_deg": flank_angle_deg,
            "thread_crest_width": thread_crest_width,
            "thread_root_width": thread_root_width,
            "thread_depth": thread_depth
        }
        super().__init__(name=name, mechanism_type="spiral_mechanism", dimensions=mech_dimensions, params=mech_params, **kwargs)
        self.pitch = self.params.get("pitch", pitch)
        self.radius = self.dimensions.get("radius", radius)
        self.thread_depth = self.params.get("thread_depth", thread_depth)
        self.helix_length = self.dimensions.get("helix_length", helix_length)
        self.segments_per_rotation = self.params.get("segments_per_rotation", segments_per_rotation)
        self.flank_angle_deg = self.params.get("flank_angle_deg", flank_angle_deg)
        self.thread_crest_width = self.params.get("thread_crest_width", thread_crest_width)
        self.thread_root_width = self.params.get("thread_root_width", thread_root_width)

    def pitch_function(self, theta_rad):
        delta_p = 0.5 * self.pitch
        return self.pitch + delta_p * np.sin(theta_rad)

    def linear_extension(self, state_manager_rotation_deg):
        return (self.pitch / 360.0) * state_manager_rotation_deg

    def generate_stl(self):
        # Complete STL generation using trapezoidal thread profile with variable pitch.
        # For brevity, we use a simplified model from core/geometry (this can be expanded as needed).
        from core.geometry import create_female_trapezoidal_port_mesh
        # Use our mechanism parameters to generate a helix mesh:
        # Here, we generate a helix-like structure as a placeholder.
        points = []
        faces = []
        vertex_count = 0
        total_rotations = self.helix_length / self.pitch
        total_segments = int(self.segments_per_rotation * total_rotations)

        for i in range(total_segments + 1):
            theta_deg = (360.0 * i) / self.segments_per_rotation
            theta_rad = np.deg2rad(theta_deg)
            # Variable pitch integration:
            delta_p = 0.5 * self.pitch
            z = (self.pitch / (2*np.pi))*theta_rad + (delta_p/(2*np.pi))*(1 - np.cos(theta_rad))
            if z > self.helix_length:
                break

            # Generate trapezoidal thread profile vertices in local XY plane:
            r = self.radius
            D = self.thread_depth
            Wc = self.thread_crest_width
            Wr = self.thread_root_width
            alpha = np.deg2rad(self.flank_angle_deg)
            pts_local = [
                [(r + D/2) - (Wc/2)*np.cos(alpha), (Wc/2)*np.sin(alpha)],
                [(r + D/2) + (Wc/2)*np.cos(alpha), (Wc/2)*np.sin(alpha)],
                [(r - D/2) + (Wr/2)*np.cos(alpha), - (Wr/2)*np.sin(alpha)],
                [(r - D/2) - (Wr/2)*np.cos(alpha), - (Wr/2)*np.sin(alpha)]
            ]
            # Rotate *each* point by theta_rad:
            rot = np.array([[np.cos(theta_rad), -np.sin(theta_rad)],
                            [np.sin(theta_rad), np.cos(theta_rad)]])
            pts_rot = [np.dot(rot, np.array(pt)) for pt in pts_local]
            for pt in pts_rot:
                points.append([pt[0], pt[1], z])
            if i > 0:
                idx = vertex_count - 4
                faces.extend([
                    [idx, idx+1, vertex_count+1],
                    [idx, vertex_count+1, vertex_count],
                    [idx+1, idx+2, vertex_count+2],
                    [idx+1, vertex_count+2, vertex_count+1],
                    [idx+2, idx+3, vertex_count+3],
                    [idx+2, vertex_count+3, vertex_count+2],
                    [idx+3, idx, vertex_count],
                    [idx+3, vertex_count, vertex_count+3]
                ])
            vertex_count += 4

        vertices = np.array(points)
        faces = np.array(faces)
        mesh = trimesh.Trimesh(vertices=vertices, faces=faces)
        return mesh

class LinearActuator(Mechanism):
    def __init__(self, name="Linear_Actuator_Default", actuator_type="inverted_thread", rod_radius=1.0, rod_length=20.0, **kwargs):
        mech_dimensions = {
            "rod_radius": rod_radius,
            "rod_length": rod_length
        }
        mech_params = {
            "actuator_type": actuator_type
        }
        super().__init__(name=name, mechanism_type="linear_actuator", dimensions=mech_dimensions, params=mech_params, **kwargs)
        self.actuator_type = self.params.get("actuator_type", actuator_type)
        self.rod_radius = self.dimensions.get("rod_radius", rod_radius)
        self.rod_length = self.dimensions.get("rod_length", rod_length)

    def generate_stl(self):
        return trimesh.creation.cylinder(radius=self.rod_radius, height=self.rod_length)

class StateManager(Mechanism):
    def __init__(self, name="State_Manager_Default", rotation_range_deg=360.0, shaft_radius=0.5, shaft_height=10.0, **kwargs):
        mech_dimensions = {
            "shaft_radius": shaft_radius,
            "shaft_height": shaft_height
        }
        mech_params = {
            "rotation_range_deg": rotation_range_deg
        }
        super().__init__(name=name, mechanism_type="state_manager", dimensions=mech_dimensions, params=mech_params, **kwargs)
        self.rotation_range_deg = self.params.get("rotation_range_deg", rotation_range_deg)
        self.shaft_radius = self.dimensions.get("shaft_radius", shaft_radius)
        self.shaft_height = self.dimensions.get("shaft_height", shaft_height)
        self.current_angle_deg = 0.0

    def set_rotation(self, angle_deg):
        self.current_angle_deg = angle_deg % self.rotation_range_deg

    def generate_stl(self):
        return trimesh.creation.cylinder(radius=self.shaft_radius, height=self.shaft_height)
