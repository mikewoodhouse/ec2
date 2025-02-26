from pathlib import Path

import pytest
from classes import Match

from ec2.scorebook.scorer import Extra, HowOut, ScoreCard, Scorer


@pytest.fixture
def match() -> Match:
    path = Path(__file__).parent / "951373.json"
    with path.open() as f:
        return Match.from_json(f.read())


@pytest.fixture
def card(match) -> ScoreCard:
    card = ScoreCard()
    scorer = Scorer(card)
    for ball in match.balls(0):
        scorer.update(ball)
    return card


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


def test_scorer(match: Match, card: ScoreCard):
    inns_0_runs = sum(ball.total_runs for ball in match.balls(0))
    inns_0_wkts = sum(bool(ball.player_out) for ball in match.balls(0))

    assert card.runs == inns_0_runs
    assert card.wickets == inns_0_wkts
    assert card.batters.get("JJ Roy", None)

    assert card.batters["AD Hales"].position == 2
    assert len(card.batters) == 11
    assert card.wickets == 9
    assert card.batters["JJ Roy"].how_out == HowOut.BOWLED
    assert card.fours > 0
    assert card.batters["AD Hales"].how_out == HowOut.CAUGHT
    assert card.batters["AD Hales"].fielder == "S Badree"
    assert card.bowlers["S Badree"].wickets == 2
    assert card.batters["AD Hales"].balls_faced == 3

    jj_roy = card.batters["JJ Roy"]
    assert jj_roy.position == 1

    je_root = card.batters["JE Root"]
    assert je_root.position == 3
    assert je_root.fours == 7

    jc_buttler = card.batters["JC Buttler"]
    assert jc_buttler.sixes == 3

    sj_benn = card.bowlers["SJ Benn"]
    assert sj_benn.sixes == 3

    s_badree = card.bowlers["S Badree"]
    assert s_badree.wickets == 2
    assert s_badree.runs == 16

    cr_brathwaite = card.bowlers["CR Brathwaite"]
    assert cr_brathwaite.balls_bowled == 25
    assert cr_brathwaite.runs == 23

    assert card.extras[Extra.LEGBYE] == 4
    assert card.extras[Extra.WIDE] == 1
