# models/physics.py
from dataclasses import dataclass

@dataclass(frozen=True)
class PhysicsParameters:
    """
    Immutable physical parameters generated from AI cognitive state.
    SimulationEngine depends only on this model, never on the LLM or cognitive state directly.
    """
    enemy_speed: float
    enemy_fov: float
    visibility: float
    glitch_intensity: float
