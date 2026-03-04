from dataclasses import dataclass, field
from .score_card import ScoreCard
from .ball import Ball
from .extra import Extra

@dataclass
class Scorer:
    card: ScoreCard = field(default_factory=ScoreCard)

    def over_bowled(self):
        self.card.over += 1
        self.card.ball = 0

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

        if ball.extra_type not in [Extra.WIDE, Extra.NOBALL]:
            self.card.ball += 1
        extras = "" if ball.extra_type == Extra.NO_EXTRA else f"+{ball.extra_runs}{ball.extra_type}"
        desc = f"{self.card.over}.{self.card.ball} {ball.bowler} to {ball.striker}: {ball.batter_runs} runs {extras}"
        self.card.history.append(desc)
