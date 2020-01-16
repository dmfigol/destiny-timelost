from typing import TYPE_CHECKING, Tuple, Optional

from destiny_timelost import utils

if TYPE_CHECKING:
    from destiny_timelost.node import Node  # noqa: F401


class Side:
    def __init__(self, idx: int, value: str, is_open: bool, node_url: str) -> None:
        self.idx = idx
        self.value = value.upper()
        self.node_url = node_url
        self.is_open = is_open

        self.connected_to: Optional[Side] = None

    def __repr__(self) -> str:
        return utils.create_repr(self, ("node_url", "idx", "value", "is_open"))

    @property
    def num(self) -> int:
        return self.idx + 1

    @property
    def other_idx(self) -> int:
        return (self.idx + 3) % 6

    @property
    def other_id(self) -> Tuple[str, int]:
        return (self.value, self.other_idx)

    @property
    def is_wall(self) -> bool:
        return self.value in ("BBBBBB", "BBBBBBB")

    @property
    def id(self) -> Tuple[str, int]:
        return self.value, self.idx

    def connect_to(self, another_side: "Side") -> None:
        self.connected_to = another_side
        another_side.connected_to = self
