from pathlib import Path

import pytest
from classes import Match

from ec2.scorebook import Extra, HowOut, ScoreCard, Scorer


@pytest.fixture
def match() -> Match:
    path = Path(__file__).parent / "951373.json"
    with path.open() as f:
        return Match.from_json(f.read())


def innings_card(match, inns: int) -> ScoreCard:
    card = ScoreCard()
    scorer = Scorer(card)
    for ball in match.balls(inns):
        scorer.update(ball)
    return card


@pytest.fixture
def first_innings_card(match) -> ScoreCard:
    return innings_card(match, 0)


def test_scorebook(match: Match):
    assert match.info.overs == 20
    assert match.info.balls_per_over == 6
    balls = match.balls(0)
    ball = next(balls)
    assert ball.batter_runs == 0
    assert ball.striker == "JJ Roy"
    assert ball.non_striker == "AD Hales"
    assert ball.bowler == "S Badree"
    ball = next(balls)
    assert ball.how_out == "b"
    ball = next(balls)
    assert ball.striker == "JE Root"
    assert ball.batter_runs == 1


def test_scorer(match: Match, first_innings_card: ScoreCard):
    inns_0_runs = sum(ball.total_runs for ball in match.balls(0))
    inns_0_wkts = sum(bool(ball.player_out) for ball in match.balls(0))

    assert first_innings_card.runs == inns_0_runs
    assert first_innings_card.wickets == inns_0_wkts

    assert first_innings_card.batters.get("JJ Roy", None)

    assert first_innings_card.batters["AD Hales"].position == 2
    assert len(first_innings_card.batters) == 11
    assert first_innings_card.wickets == 9
    assert first_innings_card.batters["JJ Roy"].how_out == HowOut.BOWLED
    assert first_innings_card.fours > 0
    assert first_innings_card.batters["AD Hales"].how_out == HowOut.CAUGHT
    assert first_innings_card.batters["AD Hales"].fielder == "S Badree"
    assert first_innings_card.bowlers["S Badree"].wickets == 2
    assert first_innings_card.batters["AD Hales"].balls_faced == 3

    jj_roy = first_innings_card.batters["JJ Roy"]
    assert jj_roy.position == 1

    je_root = first_innings_card.batters["JE Root"]
    assert je_root.position == 3
    assert je_root.fours == 7

    jc_buttler = first_innings_card.batters["JC Buttler"]
    assert jc_buttler.sixes == 3

    s_badree = first_innings_card.bowlers["S Badree"]
    assert s_badree.wickets == 2
    assert s_badree.runs == 16

    cr_brathwaite = first_innings_card.bowlers["CR Brathwaite"]
    assert cr_brathwaite.balls_bowled == 25
    assert cr_brathwaite.runs == 23

    assert first_innings_card.extras[Extra.LEGBYE] == 4
    assert first_innings_card.extras[Extra.WIDE] == 1


def test_complete_innings(match: Match):
    inns_1 = innings_card(match, 0)
    inns_2 = innings_card(match, 1)
    assert inns_1.runs == 155
    assert inns_1.wickets == 9
    assert inns_2.runs == 161
    assert inns_2.wickets == 6
