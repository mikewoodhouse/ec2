from dataclasses import dataclass
from dataclasses_json import DataClassJsonMixin
from .extra import Extra
from .how_out import HowOut

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
        return self.batter_runs + (self.extra_runs if self.is_extra else 0) + self.penalty_runs

    @property
    def bowler_runs(self) -> int:
        return self.batter_runs + (self.extra_runs if self.extra_type in [Extra.WIDE, Extra.NOBALL] else 0)

    @property
    def is_extra(self) -> bool:
        return self.extra_type != Extra.NO_EXTRA
