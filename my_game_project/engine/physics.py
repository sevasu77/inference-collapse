# engine/physics.py
from dataclasses import dataclass

@dataclass
class PhysicsParameters:
    """
    Pure Physics Matrix
    
    AIの存在を一切知らない、シミュレーション世界を動かすための純粋な物理数値。
    """
    enemy_speed: float
    enemy_fov: float
    visibility: float
    glitch_intensity: float
    # 将来的には以下のような拡張が自然に行える：
    # gravity: float = 1.0
    # weather_fog: float = 0.0
