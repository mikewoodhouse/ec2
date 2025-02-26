"""
class definitions for importing JSON match files

Extracted from extracover, but for testing purposes, hence these are data-only,
methods, properties etc have been removed.

"""

from dataclasses import dataclass, field
from datetime import date

from dataclasses_json import DataClassJsonMixin, config, dataclass_json

from ec2.scorebook.scorer import Ball, Extra, HowOut


def date_field():
    return field(
        metadata=config(encoder=date.isoformat, decoder=date.fromisoformat),
        default=date(1900, 1, 1),
    )


def date_list_decoder(dts: list[str]) -> list[date]:
    return [date.fromisoformat(s) for s in dts]


@dataclass_json
@dataclass
class Meta:
    created: date = date_field()
    data_version: str = "0"
    revision: int = 0


@dataclass_json
@dataclass
class Event:
    name: str = ""
    stage: str = ""
    match_number: str = ""


@dataclass_json
@dataclass
class Toss:
    decision: str = ""
    winner: str = ""


@dataclass_json
@dataclass
class Registry:
    people: dict[str, str] = field(default_factory=dict)


@dataclass_json
@dataclass
class Info:
    dates: list[date] = field(metadata=config(decoder=date_list_decoder), default_factory=list)
    balls_per_over: int = 0
    gender: str = ""
    match_type: str = ""
    match_type_number: int = 0
    overs: int = 0
    venue: str = ""
    toss: Toss = field(default_factory=Toss)
    registry: Registry = field(default_factory=Registry)
    event: Event = field(default_factory=Event)
    players: dict[str, list[str]] = field(default_factory=dict)
    teams: list[str] = field(default_factory=list)
    city: str = ""
    file_path: str = ""


@dataclass_json
@dataclass
class Extras:
    noballs: int = 0
    wides: int = 0
    legbyes: int = 0
    byes: int = 0
    penalty: int = 0

    def to_extra(self) -> Extra:
        if self.noballs:
            return Extra.NOBALL
        if self.wides:
            return Extra.WIDE
        if self.byes:
            return Extra.BYE
        if self.legbyes:
            return Extra.LEGBYE
        return Extra.NO_EXTRA


@dataclass_json
@dataclass
class Runs:
    batter: int = 0
    extras: int = 0
    total: int = 0


@dataclass_json
@dataclass
class Dismissal:
    player_out: str = ""
    kind: str = ""
    fielders: list[dict] = field(default_factory=list)

    def to_how_out(self) -> HowOut:
        return {
            "caught": HowOut.CAUGHT,
            "caught and bowled": HowOut.CAUGHT,
            "bowled": HowOut.BOWLED,
            "lbw": HowOut.LBW,
            "stumped": HowOut.STUMPED,
            "run out": HowOut.RUN_OUT,
            "retired": HowOut.OTHER,
            "retired not out": HowOut.OTHER,
            "hit wicket": HowOut.OTHER,
            "obstructing the field": HowOut.OTHER,
            "handled the ball": HowOut.OTHER,
            "timed out": HowOut.OTHER,
            "hit the ball twice": HowOut.OTHER,
            "absent hurt": HowOut.OTHER,
            "retired hurt": HowOut.OTHER,
        }.get(self.kind, HowOut.OTHER)


@dataclass
class Delivery(DataClassJsonMixin):
    ball_seq: int = 0
    legal_ball_seq: int = 0
    batter: str = ""
    bowler: str = ""
    non_striker: str = ""
    runs: Runs = field(default_factory=Runs)
    extras: Extras = field(default_factory=Extras)
    wickets: list[Dismissal] = field(default_factory=list)

    def to_ball(self) -> Ball:
        return Ball(
            striker=self.batter,
            non_striker=self.non_striker,
            bowler=self.bowler,
            batter_runs=self.runs.batter,
            extra_type=self.extras.to_extra(),
            extra_runs=self.runs.extras,
            penalty_runs=self.extras.penalty,
            player_out=self.wickets[0].player_out if self.wickets else "",
            how_out=HowOut.NOTOUT if not self.wickets else self.wickets[0].to_how_out(),
            fielder=self.wickets[0].fielders[0]["name"] if self.wickets and self.wickets[0].fielders else "",
        )


@dataclass_json
@dataclass
class Over:
    over: int
    deliveries: list[Delivery] = field(default_factory=list, metadata=config(field_name="deliveries"))


@dataclass_json
@dataclass
class PowerPlay:
    type: str
    ball_from: float = field(metadata=config(field_name="from"))
    ball_to: float = field(metadata=config(field_name="to"))


@dataclass_json
@dataclass
class Target:
    overs: int = 0
    runs: int = 0


@dataclass
class Innings(DataClassJsonMixin):
    team: str = ""
    overs: list[Over] = field(default_factory=list)
    powerplays: list[PowerPlay] = field(default_factory=list)
    target: Target = field(default_factory=Target)


@dataclass
class Match(DataClassJsonMixin):
    meta: Meta
    info: Info
    innings: list[Innings] = field(default_factory=list)

    def balls(self, innings_no: int):
        for over in self.innings[innings_no].overs:
            for delivery in over.deliveries:
                yield delivery.to_ball()


@dataclass
class Person:
    identifier: str
    name: str
    unique_name: str
    key_bcci: str = ""
    key_bcci_2: str = ""
    key_bigbash: str = ""
    key_cricbuzz: str = ""
    key_cricheroes: str = ""
    key_crichq: str = ""
    key_cricinfo: str = ""
    key_cricinfo_2: str = ""
    key_cricingif: str = ""
    key_cricketarchive: str = ""
    key_cricketarchive_2: str = ""
    key_nvplay: str = ""
    key_nvplay_2: str = ""
    key_opta: str = ""
    key_opta_2: str = ""
    key_pulse: str = ""
    key_pulse_2: str = ""
