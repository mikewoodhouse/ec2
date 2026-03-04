from dataclasses import field
from nicegui import binding
from .ball import Ball
from .how_out import HowOut

@binding.bindable_dataclass
class Bowler:
    position: int = 0
    name: str = ""
    balls: list[Ball] = field(default_factory=list)
    wickets: int = 0

    @property
    def runs(self) -> int:
        return sum(ball.bowler_runs for ball in self.balls)

    @property
    def balls_bowled(self) -> int:
        return len(self.balls)

    def add(self, ball: Ball) -> None:
        self.balls.append(ball)
        if ball.player_out and ball.how_out in [
            HowOut.BOWLED,
            HowOut.CAUGHT,
            HowOut.LBW,
            HowOut.STUMPED,
        ]:
            self.wickets += 1

    @property
    def html(self) -> str:
        return (
            (
                f"""<div style='display: flex; justify-content: space-between; width: 300px;'>"""
                f"""<div>{self.name}</div>"""
                f"""<div>{self.wickets}-{self.runs} ({self.balls_bowled})</div>"""
            )
            if self.position > 0
            else ""
        )
