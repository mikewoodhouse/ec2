from nicegui import ui

from ec2.scorebook import ScoreCard
from src.ec2.ui.display import Display

display = Display(card_1=ScoreCard(), card_2=ScoreCard())

display.show()

ui.run()
