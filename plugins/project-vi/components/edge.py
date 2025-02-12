"""
Edge module for The Box system.
Defines the Edge class, which inherits from Component,
and integrates layered structure, mechanisms, and parameterized connection features.
"""

from components import Component
from components.mechanisms import SpiralMechanism, LinearActuator, StateManager
from core.geometry import create_female_trapezoidal_port_mesh
from core.transformation_utils import determine_port_transformation
import trimesh
import numpy as np
from config_loader import load_config

class Edge(Component):
    def __init__(self, name="Edge_E1", length=100.0, width=10.0, height=10.0, layer_config=None, connection_interface=None, mechanisms_config=None, **kwargs):
        component_dimensions = {
            "length": length,
            "width": width,
            "height": height
        }
        super().__init__(name=name, component_type="edge", dimensions=component_dimensions, params=kwargs)
        
        if layer_config is None:
            self.layers = {
                "outer_shell": 1.25,
                "outer_ring": 1.25,
                "inner_ring": 1.25,
                "central_void_diameter": 2.5
            }
        else:
            self.layers = layer_config

        self.connection_interface = connection_interface if connection_interface is not None else {
            "connector_type": "double_male_dovetail"
        }
        self.mechanisms = {
            "spiral": SpiralMechanism(name="Edge_Spiral_Default"),
            "linear_actuator": LinearActuator(name="Edge_Linear_Actuator_Default"),
            "state_manager": StateManager(name="Edge_State_Manager_Default")
        }
        if mechanisms_config is not None:
            self.configure_mechanisms_from_config(mechanisms_config)

    def configure_mechanisms_from_config(self, mechanisms_config):
        spiral_config = mechanisms_config.get("spiral", {})
        linear_actuator_config = mechanisms_config.get("linear_actuator", {})
        state_manager_config = mechanisms_config.get("state_manager", {})

        self.configure_mechanism("spiral", params=spiral_config)
        self.configure_mechanism("linear_actuator", params=linear_actuator_config)
        self.configure_mechanism("state_manager", params=state_manager_config)

    def configure_mechanism(self, mech_type, params=None, **kwargs):
        mech_class = None
        if mech_type == "spiral":
            mech_class = SpiralMechanism
        elif mech_type == "linear_actuator":
            mech_class = LinearActuator
        elif mech_type == "state_manager":
            mech_class = StateManager
        else:
            print(f"Warning: Mechanism type '{mech_type}' not recognized for Edge.")
            return

        final_params = {**(params if params else {}), **kwargs}
        self.mechanisms[mech_type] = mech_class(name=f"Edge_{self.name}_{mech_type}", **final_params)

    def generate_stl(self):
        # Generate base Edge box mesh
        base_edge_mesh = trimesh.creation.box(extents=[self.dimensions["length"], self.dimensions["width"], self.dimensions["height"]])
        
        # Load global config for connection features
        config = load_config()
        features_to_subtract = []
        
        # Process Face Grooves on Width Faces (assume connection feature key "face_grooves_width_faces")
        edge_conn_features = config["components"]["edge_unit_e1"].get("connection_features", {})
        face_grooves_config = edge_conn_features.get("face_grooves_width_faces")
        if face_grooves_config:
            port_config_ref = face_grooves_config["port_config_ref"]
            port_config = config["connection_interfaces"][port_config_ref]
            num_grooves = face_grooves_config["count"]
            locations = face_grooves_config["locations"]
            for i in range(num_grooves):
                loc_config = locations[i]
                port_mesh = create_female_trapezoidal_port_mesh(port_config=port_config, port_name=f"edge_face_groove_{i}")
                translation_vector, rotation_matrix = determine_port_transformation(loc_config, self.dimensions)
                port_mesh.apply_translation(translation_vector)
                port_mesh.apply_transform(rotation_matrix)
                features_to_subtract.append(port_mesh)
        
        # Subtract generated features from the base Edge mesh.
        edge_with_features = base_edge_mesh.difference(features_to_subtract)

        # Add mechanism placeholders
        mech_meshes = []
        spiral_mesh = self.mechanisms["spiral"].generate_stl()
        spiral_mesh.apply_translation([0, 0, self.dimensions["height"] / 2])
        mech_meshes.append(spiral_mesh)
        
        actuator_mesh = self.mechanisms["linear_actuator"].generate_stl()
        actuator_mesh.apply_translation([self.dimensions["length"], 0, self.dimensions["height"] / 2])
        mech_meshes.append(actuator_mesh)
        
        state_mesh = self.mechanisms["state_manager"].generate_stl()
        state_mesh.apply_translation([self.dimensions["length"] / 2, self.dimensions["width"] / 2, self.dimensions["height"]])
        mech_meshes.append(state_mesh)
        
        combined = trimesh.util.concatenate([edge_with_features] + mech_meshes)
        return combined

    def save_stl(self, filename):
        mesh = self.generate_stl()
        mesh.export(filename)
        print(f"Edge STL '{filename}' saved.")

    def __str__(self):
        mech_names = ", ".join([m.name for m in self.mechanisms.values() if m])
        return f"Edge: {self.name}, Dimensions: {self.dimensions}, Layers: {self.layers}, Mechanisms: {mech_names}"