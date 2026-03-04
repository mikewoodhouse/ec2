from dataclasses import field
from dataclasses_json import DataClassJsonMixin
from nicegui import binding
from .batting_order import BattingOrder
from .bowling_order import BowlingOrder
from .extra import Extra
from .batter import Batter
from .bowler import Bowler

@binding.bindable_dataclass
class ScoreCard(DataClassJsonMixin):
    runs: int = 0
    wickets: int = 0
    batting_order: BattingOrder = field(default_factory=BattingOrder)
    bowling_order: BowlingOrder = field(default_factory=BowlingOrder)
    extras: dict[Extra, int] = field(default_factory=dict)
    history: list[str] = field(default_factory=list)
    over: int = 0
    ball: int = 0

    def add_batter(self, name: str) -> Batter:
        return self.batting_order.add(name)

    def add_bowler(self, name: str) -> Bowler:
        return self.bowling_order.add(name)

    @property
    def batters(self) -> dict[str, Batter]:
        return self.batting_order.batters

    @property
    def bowlers(self) -> dict[str, Bowler]:
        return self.bowling_order.bowlers

    @property
    def fours(self) -> int:
        return sum(batter.fours for batter in self.batting_order.batters.values())

    @property
    def sixes(self) -> int:
        return sum(batter.sixes for batter in self.batting_order.batters.values())

    @property
    def score(self) -> str:
        return f"{self.runs}/{self.wickets} ({self.over}.{self.ball})"

    @property
    def last_6(self) -> str:
        return "\n".join(self.history[:-7:-1])
