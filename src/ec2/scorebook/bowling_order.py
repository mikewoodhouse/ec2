from dataclasses import field
from nicegui import binding
from .bowler import Bowler

@binding.bindable_dataclass
class BowlingOrder:
    next_position: int = 1
    bowlers: dict[str, Bowler] = field(default_factory=dict)

    def __post_init__(self) -> None:
        for i in range(1, 12):
            setattr(self, f"bowler_{i}", self.make_bowler_lookup_func(i))

    def add(self, name: str) -> Bowler:
        if not self.bowlers.get(name, None):
            self.bowlers[name] = Bowler(name=name, position=self.next_position)
            self.next_position += 1
        return self.bowlers[name]

    def make_bowler_lookup_func(self, index: int):
        def bowler_lookup() -> Bowler:
            for p in self.bowlers.values():
                if p.position == index:
                    return p
            return Bowler()

        return bowler_lookup
