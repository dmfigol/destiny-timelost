from typing import TYPE_CHECKING, Tuple

if TYPE_CHECKING:
    from destiny_timelost.side import Side


class Link:
    def __init__(self, *sides: Tuple["Side", ...]) -> None:
        self.sides = sorted(sides, key=lambda side: side.idx)

    @property
    def first_side(self) -> "Side":
        return self.sides[0]

    @property
    def second_side(self) -> "Side":
        return self.sides[1]

    def __eq__(self, other) -> bool:
        return (self.first_side, self.second_side) == (
            other.first_side,
            other.second_side,
        )

    def __hash__(self) -> int:
        return hash((self.first_side, self.second_side))
