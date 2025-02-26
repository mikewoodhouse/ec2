from nicegui import ui

from ec2.scorebook import Ball, Scorer

from .scorecard import ScoreCard


class Display:
    def __init__(self, card: ScoreCard, book: Scorer) -> None:
        self.card = card
        self.book = book

    def update_book(self):
        self.book.update(Ball())

    def show(self):
        ui.label("").bind_text_from(self.card, "runs")
        ui.button(on_click=self.update_book)
