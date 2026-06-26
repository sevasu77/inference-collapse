# engine/simulation.py
from engine.threat import ThreatEngine

class SimulationEngine:
    """
    Pure Simulation Loop Driver
    
    【依存性逆転の極み】
    AIの存在を知らず、供給された PhysicsParameters だけを使って
    ゲーム世界の座標更新や描画バッファの計算を淡々とこなす。
    """
    def __init__(self, threat_engine: ThreatEngine):
        self.threat_engine = threat_engine

    def update(self):
        """毎フレーム実行される、ピュアな物理世界線の更新ループ"""
        # 依存性逆転：ThreatEngineから、不変の物理パラメータを生成してもらう
        physics = self.threat_engine.generate_physics()
        
        # 完全に分離された物理モデル（models.physics）だけで世界を駆動
        self._move_enemies(physics.enemy_speed, physics.enemy_fov)
        self._apply_coordinate_noise(physics.glitch_intensity)
        self._restrict_viewport(physics.visibility)

    def _move_enemies(self, speed: float, fov: float):
        pass

    def _apply_coordinate_noise(self, intensity: float):
        pass

    def _restrict_viewport(self, visibility: float):
        pass
