import logging
from typing import Tuple, List, Set

import attr

from destiny_timelost import exceptions
from destiny_timelost.side import Side
from destiny_timelost import utils

logger = logging.getLogger(__name__)


@attr.s(auto_attribs=True, kw_only=True, repr=False, eq=False)
class Node:
    url: str
    row_num: int
    center: str
    sides: Tuple[Side]

    def __repr__(self) -> str:
        return utils.create_repr(self, ("row_num, url"))

    def __str__(self) -> str:
        sides_pieces = []
        for side in self.sides:
            value = side.value
            if side.connected_to:
                value = f"**{value}**"
            if side.is_open:
                value = f"-{value}-"
            sides_pieces.append(value)
        sides_str = " | ".join(sides_pieces)
        return f"row: {self.row_num} | {self.url} | {self.center} | {sides_str}"

    @property
    def is_blank(self) -> bool:
        return not self.center or self.center == "blank"

    @property
    def side_values(self) -> Tuple[str, ...]:
        return tuple(side.value for side in self.sides)

    @property
    def alt_id(self) -> Tuple[str, Tuple[str, ...]]:
        return self.center, self.side_values

    def __eq__(self, other) -> bool:
        return self.url == other.url

    def __hash__(self) -> int:
        return hash(self.url)

    @classmethod
    def create(cls, cells: List[str], row_num: int):
        url, center, openings_str, *sides_raw = cells
        center = center.lower()
        sides = Node.create_sides(sides_raw, openings_str, node_url=url)
        node = cls(url=url, row_num=row_num, center=center, sides=sides)
        return node

    @staticmethod
    def create_sides(
        sides_raw: List[str], openings_str: str, node_url: str
    ) -> Tuple[Side, ...]:
        openings: Set[int] = set()
        if openings_str:
            for opening in openings_str.split(","):
                try:
                    op_int = int(opening)
                    openings.add(op_int)
                except ValueError as e:
                    logger.error(
                        "Node url %s openings have incorrect format", node_url,
                    )
                    raise exceptions.IncorrectSideError from e

        sides = []
        for i, side_v in enumerate(sides_raw[:6]):
            side_value = side_v.upper()
            if not side_value or (len(side_value) != 7 and side_value != "BBBBBB"):
                logger.error("Node %s has incorrect side %r", node_url, side_value)
                raise exceptions.IncorrectSideError
            is_open = (i + 1) in openings
            side = Side(idx=i, value=side_value, is_open=is_open, node_url=node_url)
            sides.append(side)
        return tuple(sides)
