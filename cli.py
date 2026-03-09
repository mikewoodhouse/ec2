from ec2.scorebook import ScoreCard, Scorer, Ball

card = ScoreCard()
scorer = Scorer()

striker: str = ""
non_striker: str = ""
bowler: str = ""


def prompt() -> str:
    return f"{bowler} to {striker}: "


while True:
    cmd = input(prompt())
    match cmd:
        case ".":
            scorer.update(Ball(striker=striker, non_striker=non_striker, bowler=bowler))
        case s if cmd.startswith("str"):
            striker = cmd.split()[1]
        case s if cmd.startswith("non"):
            non_striker = cmd.split()[1]
        case s if s.startswith("bow"):
            bowler = cmd.split()[1]
        case s if s in ["1", "2", "3", "4", "6"]:
            scorer.update(Ball(striker=striker, non_striker=non_striker, bowler=bowler, batter_runs=int(s)))
        case "q":
            break
    print(scorer.card.score)
