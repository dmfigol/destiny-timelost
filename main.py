import asyncio
import logging
import logging.config
import os
from collections import deque
from typing import Tuple, List, Dict, Set

import aiofiles
import uvloop
import httpx

from destiny_timelost import constants
from destiny_timelost import exceptions
from destiny_timelost.link import Link
from destiny_timelost.node import Node
from destiny_timelost.side import Side


logger = logging.getLogger(__name__)


async def fetch_and_parse_sheet() -> Tuple[
    Dict[str, Node], Dict[Tuple[str, int], Side]
]:

    url_to_node: Dict[str, Node] = {}
    alt_id_to_node: Dict[Tuple[str, str], Node] = {}
    side_id_to_node: Dict[Tuple[str, int], Side] = {}
    http_client = httpx.AsyncClient()
    url = constants.GOOGLE_SHEET_URL.format(
        sheet_id=os.environ["GOOGLE_SHEET_ID"], table_name="Main",
    )
    params = {"key": os.environ["GOOGLE_SHEET_KEY"]}
    response = await http_client.get(url, params=params)
    response.raise_for_status()
    data = response.json()

    for row_num, row in enumerate(data["values"], 1):
        cells = row
        if not (len([cell for cell in cells if cell]) > 4 and "https" in cells[0]):
            continue

        try:
            node = Node.create(cells, row_num=row_num)
            if node.url in url_to_node:
                found_node = url_to_node[node.url]
                logger.error("Node %s is duplicate of node %s", node, found_node)
                continue

            url_to_node[node.url] = node
        except exceptions.IncorrectSideError:
            continue

        if node.alt_id in alt_id_to_node:
            found_node = alt_id_to_node[node.alt_id]
            logger.error("Node %s is duplicate of the node %s", node, found_node)
        else:
            alt_id_to_node[node.alt_id] = node
            for side in node.sides:
                if side.is_wall:
                    continue

                if side.id in side_id_to_node:
                    found_node = side_id_to_node[side.id]
                    logger.error(
                        "%s and %s have dup sides: potential duplicate or incorrect transcription",
                        node,
                        found_node,
                    )
                else:
                    side_id_to_node[side.id] = node

    return url_to_node, side_id_to_node


def parse_nodes(
    url_to_node: Dict[str, Node], side_id_to_node: Dict[Tuple[str, int], Node]
) -> Tuple[List[Link], List[Set[Node]]]:
    found_links: List[Link] = []
    found_links_set: Set[Link] = set()
    visited_nodes: Set[Node] = set()
    clusters: List[Set[Node]] = []
    all_nodes = deque(sorted(url_to_node.values(), key=lambda node: node.is_blank))

    logger.info("Found %d unique nodes", len(url_to_node))

    def _traverse_node(node: Node, cluster: Set[Node]):
        cur_cluster.add(node)
        visited_nodes.add(node)
        for side in node.sides:
            if side.is_wall:
                continue

            other_side_id = side.other_id
            if other_side_id in side_id_to_node:
                other_node = side_id_to_node[other_side_id]
                other_side = other_node.sides[side.other_idx]
                link = Link(side, other_side)
                if link in found_links_set:
                    continue
                side.connect_to(other_side)
                found_links_set.add(link)
                found_links.append(link)  # TODO
                if other_node not in visited_nodes:
                    _traverse_node(other_node, cluster)

    while all_nodes:
        node = all_nodes.popleft()
        cur_cluster: Set[Node] = set()
        if node not in visited_nodes:
            _traverse_node(node, cur_cluster)
        if cur_cluster:
            clusters.append(cur_cluster)

    return found_links, clusters


async def main() -> None:
    url_to_node, side_id_to_node = await fetch_and_parse_sheet()

    found_links, clusters = parse_nodes(url_to_node, side_id_to_node)
    async with aiofiles.open("output/clusters.txt", "w") as f:
        for cluster in sorted(clusters, key=len, reverse=True):
            if len(cluster) >= 2:
                for node in cluster:
                    await f.write(str(node) + "\n")
                await f.write("\n")


if __name__ == "__main__":
    logging.config.dictConfig(constants.LOGGING_DICT)
    uvloop.install()
    asyncio.run(main())
