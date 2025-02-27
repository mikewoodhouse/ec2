from copy import copy

from nicegui import ui

from ec2.scorebook import Ball, HowOut, ScoreCard, Scorer


class Display:
    def __init__(self) -> None:
        self.scorer = Scorer(ScoreCard())
        self.card = self.scorer.card

    def show(self):
        ui.page_title("ec2")
        with ui.row():
            self.ball = Ball(striker="", non_striker="", bowler="")
            with ui.column():
                with ui.card():
                    self.ball_creator()
                with ui.card():
                    self.player_selection()
            with ui.column():
                with ui.card():
                    self.innings_card()
                with ui.card():
                    self.innings_log()

    def update_player_out(self):
        self.player_out.options = ["", self.ball.striker, self.ball.non_striker]
        self.player_out.update()

    def ball_creator(self):
        def update_scorer():
            self.scorer.update(copy(self.ball))
            self.ball.reset()

        def over_bowled():
            self.ball.striker, self.ball.non_striker = self.ball.non_striker, self.ball.striker

        ui.label("Ball Creator").classes("text-blue-800 bg-blue-100 text-xl")

        with ui.grid(columns="auto 1fr"):
            ui.label("Batter Runs")
            ui.toggle([0, 1, 2, 3, 4, 5, 6], value=0).bind_value(self.ball, "batter_runs")

            ui.label("Extra Type")
            ui.toggle(["", "nb", "w", "b", "lb"], value="").bind_value(self.ball, "extra_type")

            ui.label("Extra Runs")
            ui.toggle([0, 1, 2, 3, 4, 5, 6], value=0).bind_value(self.ball, "extra_runs").bind_enabled(
                self.ball, "is_extra"
            )

            ui.label("Out")
            self.player_out = ui.toggle(["", self.ball.striker, self.ball.non_striker]).bind_value(
                self.ball, "player_out"
            )

            ui.label("How")
            ui.toggle([e.value for e in HowOut]).bind_value(self.ball, "how_out")

            ui.label().bind_text_from(self.ball, "to_string").classes("bg-sky-200 col-span-full")

        with ui.row():
            ui.button("Add Ball", on_click=update_scorer)
            ui.button("Over Bowled", on_click=over_bowled)

    def player_selection(self):
        with ui.column():
            ui.select(
                [],
                label="Striker",
                new_value_mode="add-unique",
            ).style("borderless: true").bind_value(self.ball, "striker").on_value_change(self.update_player_out)
            ui.select(
                [],
                label="Non-striker",
                new_value_mode="add-unique",
            ).bind_value(self.ball, "non_striker").on_value_change(self.update_player_out)
            ui.select(
                [],
                label="Bowler",
                new_value_mode="add-unique",
            ).bind_value(self.ball, "bowler")

    def innings_card(self):
        with ui.column():
            with ui.card().tight():
                with ui.row():
                    ui.label("Score")
                    ui.html().bind_content_from(self.card, "score")

            with ui.card().tight():
                ui.label("Batting")
                for pos in range(1, 12):
                    with ui.element():
                        ui.html().bind_content_from(
                            self.card.batting_order, f"batter_{pos}", backward=lambda batter: batter().html
                        )

            with ui.card().tight():
                ui.label("Bowling")
                for pos in range(1, 12):
                    ui.html().bind_content_from(
                        self.card.bowling_order, f"bowler_{pos}", backward=lambda bowler: bowler().html
                    )

    def innings_log(self):
        ui.label("Recent history").classes("text-sky-400")
        ui.textarea().bind_value_from(self.card, "last_6")
