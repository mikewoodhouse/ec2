from nicegui import ui

from ec2.scorebook import Ball, ScoreCard, Scorer


class Display:
    def __init__(self) -> None:
        self.scorer = Scorer(ScoreCard())
        self.card = self.scorer.card

    def update_scorer(self):
        self.scorer.update(Ball(batter_runs=1, striker="JJ Roy", non_striker="AD Hales", bowler="S Badree"))

    def show(self):
        with ui.row():
            self.ball_creator()
            self.innings_card()

    def ball_creator(self):
        with ui.card():
            ui.button("Add Ball", on_click=self.update_scorer)

    def innings_card(self):
        with ui.column():
            with ui.card().tight():
                ui.label("Score")
                ui.html().bind_content_from(self.card, "score")
            with ui.card().tight():
                ui.label("Batting")
                for pos in range(1, 12):
                    ui.html().bind_content_from(
                        self.card.batting_order, f"batter_{pos}", backward=lambda batter: batter().html
                    )
            with ui.card().tight():
                ui.label("Bowling")
                for pos in range(1, 12):
                    ui.html().bind_content_from(
                        self.card.bowling_order, f"bowler_{pos}", backward=lambda bowler: bowler().html
                    )
