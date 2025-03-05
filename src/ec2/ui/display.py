from dataclasses import dataclass, field

from nicegui import ui

from ec2.scorebook import Ball, Extra, HowOut, ScoreCard, Scorer


class InningsCard:
    def __init__(self, card: ScoreCard):
        self.card = card

    def innings_card(self):
        with ui.column().classes("w-full"):
            with ui.card().tight().props("flat border-none"):
                with ui.row():
                    ui.html().bind_content_from(self.card, "score").classes("text-emerald-800 text-3xl")

            with ui.card().tight().props("flat border-none"):
                ui.label("Batting").classes("text-rose-800")
                for pos in range(1, 12):
                    ui.html().bind_content_from(
                        self.card.batting_order, f"batter_{pos}", backward=lambda batter: batter().html
                    )

            with ui.card().tight().props("flat border-none"):
                ui.label("Bowling").classes("text-rose-800")
                for pos in range(1, 12):
                    ui.html().bind_content_from(
                        self.card.bowling_order, f"bowler_{pos}", backward=lambda bowler: bowler().html
                    )


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
        self.inns1 = InningsCard(ScoreCard())
        self.inns2 = InningsCard(ScoreCard())
        self.scorer = Scorer(self.inns1.card)
        self.card = self.inns1.card

    def show(self):
        ui.page_title("ec2")
        with ui.row():
            with ui.column():
                with ui.card():
                    self.ball_creator()
                with ui.card():
                    self.player_selection()
            with ui.column():
                with ui.tabs().classes("w-full") as tabs:
                    self.first_inns = ui.tab("First")
                    second_inns = ui.tab("Second")
                with ui.tab_panels(tabs, value=self.first_inns).classes("w-full"):
                    with ui.tab_panel(self.first_inns):
                        with ui.column().classes("w-96"):
                            with ui.card().classes("w-full"):
                                self.inns1.innings_card()
                            with ui.card().classes("w-full"):
                                self.innings_log()
                            ui.button("Innings Closed").on_click(self.innings_closed)
                    with ui.tab_panel(second_inns):
                        with ui.column().classes("w-96"):
                            with ui.card().classes("w-full"):
                                self.inns2.innings_card()
                            with ui.card().classes("w-full"):
                                self.innings_log()

    def innings_closed(self):
        self.scorer = Scorer(self.inns2.card)
        self.card = self.inns2.card

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
            self.change_ends()
            self.update_dismissed_player_options()
        self.reset()
        self.striker_select.value = self.striker
        self.non_striker_select.value = self.non_striker
        self.ball_desc.update()

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

    def innings_log(self):
        ui.label("Recent history").classes("text-sky-400")
        ui.textarea().bind_value_from(self.card, "last_6").classes("w-full")
