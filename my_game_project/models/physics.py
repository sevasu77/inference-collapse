# models/physics.py
from dataclasses import dataclass

@dataclass(frozen=True)
class PhysicsParameters:
    """AIを一切知らない、シミュレーション世界を動かすためだけの純粋な物理定数モデル"""
    enemy_speed: float
    enemy_fov: float
    visibility: float
    glitch_intensity: float
