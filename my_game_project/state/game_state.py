# state/game_state.py
from .world_state import WorldState
from .cognitive_state import CognitiveState
from .simulation_state import SimulationState
from .telemetry_state import TelemetryState

class GameState:
    """
    State Aggregator
    
    4つの独立したドメインStateを統括する、状態管理の単一進入点。
    ロジックを持たず、純粋な集約（Aggregation）に徹する。
    """
    def __init__(self):
        self.world = WorldState()
        self.cognitive = CognitiveState()
        self.simulation = SimulationState()
        self.telemetry = TelemetryState()
