from nicegui import ui

from ec2.scorebook.scorer import Scorer
from src.ec2.ui.display import Display
from src.ec2.ui.scorecard import ScoreCard

card = ScoreCard()
book = Scorer(card)

display = Display(card, book)

display.show()

ui.run()
