---
aliases:
  - Edge Internal Mechanisms
tags:
  - component
  - edge
  - mechanisms
  - spiral_mechanisms
  - state_management
related_nodes:
  - "edge-unit-10x10x100mm"
  - "core-structure"
  - "mechanical-systems"
  - "spiral-mechanisms"
  - "state-management"
---
# 1.1.2 Internal Mechanisms

## Description

**Internal Mechanisms** refer to the active functional systems housed within the [[edge-unit-10x10x100mm|Edge Unit]]. These mechanisms are key to the Node-Edge System's dynamic capabilities, enabling motion transfer, configuration changes, and controlled interactions between components. They are strategically located within the [[core-structure|layered core structure]] of the Edge Unit.

## Key Mechanisms

- **[[spiral-mechanisms|Spiral Mechanisms]]**
    - **Primary Spiral:** Located in the [[core-structure|Inner Ring]]. Primarily responsible for linear actuation ([[push-rod-systems|push rods]]) and rotational motion transfer.
    - **Secondary Spiral:** Located in the [[core-structure|Outer Ring]]. Facilitates force transfer, variable pitch implementation, and interaction with adjacent components and [[node-unit-10x100x100mm|Nodes]].

- **[[state-management|State Management System]]**
    - Located at both termini (ends) of the Edge Unit, within the [[core-structure|Outer Shell]].
    - Controls engagement and disengagement of mechanisms.
    - Enables state transitions (Locked, Force Transfer, Rotation Enabled, Free).
    - Manages lock engagement and [[connection-networks|connection states]] between Edges and Nodes.

- **Locking Mechanism (Cylindrical Object):**
    - Integrated within the [[state-management|State Management System]].
    - Prevents rotation or motion when engaged, ensuring stability and fixed configurations.

## Layered Housing of Mechanisms

The [[core-structure|layered concentric ring structure]] is intentionally designed to house these mechanisms in a spatially organized manner:

- **Layer 1 (Inner Ring):** Primarily houses - **Primary Spiral Mechanism**.
- **Layer 2 (Outer Ring):** Houses - **Secondary Spiral Mechanism**, **Force Transfer**, and **Variable Pitch** mechanisms.
- **Layer 3 (Outer Shell):** Houses - **Lock Points** and **State Control** mechanisms.
- **Core (Central Void):** Functions as a **Control Hub**, and pathway for [[push-rod-systems|push rods]] or wiring.

## Functional Integration

These Internal Mechanisms are not isolated components but are designed to work in a highly integrated manner:

- **Spiral Interaction:** [[spiral-mechanisms|Spirals]] interact directly to transfer rotational motion and convert it to linear motion (push rod actuation).
- **State Management Control:** The [[state-management|State Management System]] governs the engagement and disengagement of the [[spiral-mechanisms|Spirals]], allowing for precise control over motion and configuration changes.
- **Layered Functionality:** The [[core-structure|layered design]] ensures that different mechanisms operate in defined zones, minimizing interference and maximizing efficiency within the constrained space of the Edge Unit.