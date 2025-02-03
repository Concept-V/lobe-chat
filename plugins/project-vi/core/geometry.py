"""
core/geometry.py:
Geometric functions for The Box system, including connection interface generation.
"""

import trimesh
import numpy as np

def create_female_trapezoidal_port_mesh(port_config, port_name="female_trapezoidal_port"):
    """
    Generates an STL mesh for a Female Trapezoidal Port using parameters from a configuration dictionary.
    
    Args:
        port_config (dict): Contains:
            - depth (float): Depth of the port.
            - small_edge_width (float): Width of the narrow (small) edge.
            - base_width (float): Width of the base (wider) edge of the trapezoid.
            - height (float): Height of the port.
            - angle_degrees (float): Dovetail angle in degrees.
        port_name (str): Name of the port.
    
    Returns:
        trimesh.Mesh: Mesh object representing the port.
    """
    depth = port_config["depth"]
    small_edge_width = port_config["small_edge_width"]
    base_width = port_config["base_width"]
    height = port_config["height"]
    angle_deg = port_config["angle_degrees"]
    angle_rad = np.deg2rad(angle_deg)

    # Define 2D trapezoidal vertices in the XY plane.
    # Here, we construct a trapezoid centered at (0,0). The narrow edge is at one side.
    vertices_2d = np.array([
        [-base_width/2, -height/2],
        [ base_width/2, -height/2],
        [ small_edge_width/2,  height/2],
        [-small_edge_width/2,  height/2]
    ])
    # Create a 2D polygon from these vertices.
    polygon = trimesh.creation.Polygon(vertices_2d)
    # Extrude the 2D polygon along the X-axis (so that the port extends along X).
    port_mesh = polygon.extrude(direction=[depth, 0, 0])
    # Center the port mesh along the extrusion axis.
    port_mesh.vertices -= [depth/2, 0, 0]
    port_mesh.name = port_name

    return port_mesh

def create_double_male_dovetail_connector_mesh(connector_config, connector_name="double_male_dovetail_connector"):
    """
    Generates an STL mesh for a Double Male Dovetail Connector based on configuration parameters.
    
    Args:
        connector_config (dict): Contains parameters similar to the port config.
            For example, depth, small_edge_width, base_width, height, angle_degrees.
        connector_name (str): Name of the connector mesh.
    
    Returns:
        trimesh.Mesh: Mesh object for the connector.
    """
    # For simplicity, use the same geometry as the female port, but extruded to twice the depth.
    depth = connector_config["depth"] * 2  # Double the depth for a male connector
    small_edge_width = connector_config["small_edge_width"]
    base_width = connector_config["base_width"]
    height = connector_config["height"]
    angle_deg = connector_config["angle_degrees"]
    angle_rad = np.deg2rad(angle_deg)

    vertices_2d = np.array([
        [-base_width/2, -height/2],
        [ base_width/2, -height/2],
        [ small_edge_width/2,  height/2],
        [-small_edge_width/2,  height/2]
    ])
    polygon = trimesh.creation.Polygon(vertices_2d)
    connector_mesh = polygon.extrude(direction=[depth, 0, 0])
    connector_mesh.vertices -= [depth/2, 0, 0]
    connector_mesh.name = connector_name

    return connector_mesh

if __name__ == '__main__':
    # Example usage for testing:
    port_config_example = {
        "depth": 2.0,
        "small_edge_width": 2.6,
        "base_width": 6.6,
        "height": 10.0,
        "angle_degrees": 45.0
    }
    female_port = create_female_trapezoidal_port_mesh(port_config_example, port_name="female_port_example")
    female_port.visual.face_colors = [0, 200, 200, 255]
    female_port.export("female_trapezoidal_port.stl")

    connector_config_example = port_config_example  # For simplicity, use same values.
    male_connector = create_double_male_dovetail_connector_mesh(connector_config_example, connector_name="male_connector_example")
    male_connector.visual.face_colors = [200, 200, 0, 255]
    male_connector.export("double_male_dovetail_connector.stl")

    scene = trimesh.Scene([female_port, male_connector])
    scene.show()
    print("Port and Connector STL files generated and displayed.")