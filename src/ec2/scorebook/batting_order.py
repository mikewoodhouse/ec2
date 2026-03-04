from dataclasses import field
from nicegui import binding
from .batter import Batter

@binding.bindable_dataclass
class BattingOrder:
    next_position: int = 1
    batters: dict[str, Batter] = field(default_factory=dict)

    def __post_init__(self) -> None:
        for i in range(1, 12):
            setattr(self, f"batter_{i}", self.make_batter_lookup_func(i))

    def add(self, name: str) -> Batter:
        if not self.batters.get(name, None):
            self.batters[name] = Batter(name=name, position=self.next_position)
            self.next_position += 1
        return self.batters[name]

    def make_batter_lookup_func(self, index: int):
        def batter_lookup() -> Batter:
            for p in self.batters.values():
                if p.position == index:
                    return p
            return Batter()

        return batter_lookup
