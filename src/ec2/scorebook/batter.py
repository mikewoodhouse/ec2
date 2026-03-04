from dataclasses import field
from nicegui import binding
from .ball import Ball

@binding.bindable_dataclass
class Batter:
    position: int = 0
    name: str = ""
    balls: list[Ball] = field(default_factory=list)
    how_out: str = ""
    fielder: str = ""

    def add(self, ball: Ball) -> None:
        self.balls.append(ball)
        if ball.player_out == self.name:
            self.record_out(ball)

    def record_out(self, ball: Ball) -> None:
        self.how_out = ball.how_out
        self.fielder = ball.fielder

    @property
    def balls_faced(self) -> int:
        return len(self.balls)

    @property
    def runs(self) -> int:
        return sum(ball.batter_runs for ball in self.balls)

    @property
    def fours(self) -> int:
        return sum(ball.batter_runs == 4 for ball in self.balls)

    @property
    def sixes(self) -> int:
        return sum(ball.batter_runs == 6 for ball in self.balls)

    @property
    def html(self) -> str:
        return (
            (
                f"""<div style='display: flex; justify-content: space-between; width: 300px;'>"""
                f"""<div>{self.name}</div>"""
                f"""<div>{self.how_out}</div>"""
                f"""<div>{self.runs} ({self.balls_faced})</div>"""
                """</div>"""
            )
            if self.position > 0
            else ""
        )
