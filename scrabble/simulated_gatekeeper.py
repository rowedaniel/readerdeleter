from .gatekeeper import GateKeeper

class SimulatedGateKeeper(GateKeeper):
    def set_player(self, player_number: int) -> None:
        self._player_number = player_number
