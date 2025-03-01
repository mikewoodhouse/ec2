from dataclasses import dataclass, field

from nicegui import ui

from ec2.scorebook import Ball, Extra, HowOut, ScoreCard, Scorer


@dataclass
class Display:
    striker: str = ""
    non_striker: str = ""
    bowler: str = ""
    batter_runs: int = 0
    extra_type: str = ""
    extra_runs: int = 0
    penalty_runs: int = 0
    player_out: str = ""
    how_out: str = "no"
    fielder: str = ""

    batters: set[str] = field(default_factory=set)

    def __post_init__(self) -> None:
        self.scorer = Scorer(ScoreCard())
        self.card = self.scorer.card
        print(self.batters)

    def show(self):
        ui.page_title("ec2")
        with ui.row():
            with ui.column():
                with ui.card():
                    self.ball_creator()
                with ui.card():
                    self.player_selection()
            with ui.column():
                with ui.card():
                    self.innings_card()
                with ui.card().classes("w-max"):
                    self.innings_log()

    @property
    def ball_as_string(self) -> str:
        extras = "" if self.extra_type == Extra.NO_EXTRA else f"+{self.extra_runs}{self.extra_type}"
        return f"{self.bowler} to {self.striker}: {self.batter_runs} runs {extras}"

    def reset(self) -> None:
        self.batter_runs = 0
        self.extra_runs = 0
        self.penalty_runs = 0
        self.extra_type = ""
        self.player_out = ""
        self.how_out = "no"
        self.fielder = ""

    def update_dismissed_player_options(self):
        self.dismissed_player.set_options(["", self.striker, self.non_striker])
        self.update_batters()

    def change_ends(self):
        self.striker, self.non_striker = self.non_striker, self.striker

    def update_scorer(self):
        print("applying", self)
        self.scorer.update(
            Ball(
                striker=self.striker,
                non_striker=self.non_striker,
                bowler=self.bowler,
                batter_runs=self.batter_runs,
                extra_runs=self.extra_runs,
                extra_type=Extra(self.extra_type),
                penalty_runs=self.penalty_runs,
                player_out=self.player_out,
                how_out=HowOut(self.how_out),
                fielder=self.fielder,
            )
        )
        if self.batter_runs % 2 == 1:
            print("changing ends")
            self.change_ends()
            self.update_dismissed_player_options()
        self.reset()
        self.striker_select.value = self.striker
        self.non_striker_select.value = self.non_striker
        self.ball_desc.update()
        print("reset to", self)

    def over_bowled(self):
        self.scorer.over_bowled()
        self.change_ends()

    def ball_creator(self):
        ui.label("Ball Creator").classes("text-blue-800 bg-blue-100 text-xl")

        with ui.grid(columns="auto 1fr"):
            ui.label("Batter Runs")
            ui.toggle([0, 1, 2, 3, 4, 5, 6], value=0).bind_value(self, "batter_runs")

            ui.label("Extra Type")
            ui.toggle(["", "nb", "w", "b", "lb"], value="").bind_value(self, "extra_type")

            ui.label("Extra Runs")
            ui.toggle([0, 1, 2, 3, 4, 5, 6], value=0).bind_value(self, "extra_runs").bind_enabled(self, "is_extra")

            ui.label("Out")
            self.dismissed_player = ui.toggle(["", self.striker, self.non_striker]).bind_value(self, "player_out")

            ui.label("How")
            ui.toggle([e.value for e in HowOut]).bind_value(self, "how_out")

            self.ball_desc = ui.label().bind_text_from(self, "ball_as_string").classes("bg-sky-200 col-span-full")

        with ui.row():
            ui.button("Add Ball", on_click=self.update_scorer)
            ui.button("Over Bowled", on_click=self.over_bowled)

    def player_selection(self):
        with ui.column():
            self.striker_select = (
                ui.select(
                    [],
                    label="Striker",
                    new_value_mode="add-unique",
                )
                .style("dense: true, dense-options: true")
                .bind_value(self, "striker")
                .on_value_change(self.update_dismissed_player_options)
            )
            self.non_striker_select = (
                ui.select(
                    [],
                    label="Non-striker",
                    new_value_mode="add-unique",
                )
                .bind_value(self, "non_striker")
                .on_value_change(self.update_dismissed_player_options)
            )
            ui.select(
                [],
                label="Bowler",
                new_value_mode="add-unique",
            ).bind_value(self, "bowler")

    def update_batters(self):
        def options_from(select: ui.select) -> set[str]:
            options = select.options if isinstance(select.options, list) else select.options.keys()
            return {s for s in options}

        self.batters = self.batters | options_from(self.striker_select) | options_from(self.non_striker_select)

        self.striker_select.set_options(list(self.batters))
        self.non_striker_select.set_options(list(self.batters))

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
        ui.textarea().bind_value_from(self.card, "last_6").classes("flex-auto")
