from dataclasses import dataclass, field
from enum import StrEnum

from dataclasses_json import DataClassJsonMixin
from nicegui import binding


class Extra(StrEnum):
    NO_EXTRA = "None"
    WIDE = "w"
    NOBALL = "nb"
    BYE = "b"
    LEGBYE = "lb"


class HowOut(StrEnum):
    NOTOUT = "no"
    BOWLED = "b"
    CAUGHT = "c"
    LBW = "lbw"
    STUMPED = "st"
    RUN_OUT = "ro"
    OTHER = "other"


@dataclass
class Ball(DataClassJsonMixin):
    striker: str = ""
    non_striker: str = ""

    bowler: str = ""

    batter_runs: int = 0

    extra_type: Extra = Extra.NO_EXTRA
    extra_runs: int = 0

    penalty_runs: int = 0

    player_out: str = ""

    how_out: HowOut = HowOut.NOTOUT
    fielder: str = ""

    @property
    def total_runs(self) -> int:
        return self.batter_runs + self.extra_runs + self.penalty_runs

    @property
    def bowler_runs(self) -> int:
        return self.batter_runs + (self.extra_runs if self.extra_type in [Extra.WIDE, Extra.NOBALL] else 0)


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
    def sixes(self) -> int:
        return sum(ball.batter_runs == 6 for ball in self.balls)


@binding.bindable_dataclass
class ScoreCard:
    runs: int = 0
    wickets: int = 0
    batters: dict[str, Batter] = field(default_factory=dict)
    bowlers: dict[str, Bowler] = field(default_factory=dict)
    extras: dict[Extra, int] = field(default_factory=dict)

    def add_batter(self, name: str) -> Batter:
        if not self.batters.get(name, None):
            self.batters[name] = Batter(name=name, position=len(self.batters) + 1)
        return self.batters[name]

    def add_bowler(self, name: str) -> Bowler:
        if not self.bowlers.get(name, None):
            self.bowlers[name] = Bowler(name=name, position=len(self.bowlers) + 1)
        return self.bowlers[name]

    @property
    def fours(self) -> int:
        return sum(batter.fours for batter in self.batters.values())

    @property
    def sixes(self) -> int:
        return sum(batter.sixes for batter in self.batters.values())


class Scorer:
    def __init__(self, card: ScoreCard) -> None:
        self.card = card
        self.batters_seen: int = 0

    def update(self, ball: Ball):
        striker = self.card.add_batter(ball.striker)
        non_striker = self.card.add_batter(ball.non_striker)
        bowler = self.card.add_bowler(ball.bowler)

        self.card.runs += ball.total_runs

        striker.add(ball)
        bowler.add(ball)

        if ball.player_out:
            self.card.wickets += 1
            if ball.player_out == ball.non_striker:
                non_striker.record_out(ball)

        if ball.extra_runs > 0:
            self.card.extras[ball.extra_type] = self.card.extras.get(ball.extra_type, 0) + ball.extra_runs
