from collections import deque
from heapq import heappush, heappop

from loguru import logger

from searchalg.node import Node


def expand_all_nodes(init_node: Node):
    lifo = deque([init_node])

    cnt_expanded = 0
    while len(lifo) > 0:
        if cnt_expanded % 10000 == 0:
            logger.debug(f"Length of lifo: {len(lifo)}, cnt_exp: {cnt_expanded}")
        node = lifo.pop()
        if not node.is_terminal() and not node.is_expanded:
            cnt_expanded += 1
            next_nodes = node.expand()
            lifo.extend(next_nodes)


def astar(init_node: Node) -> int:
    """ Uses A*-algorithm to search for the least cost way to a terminal-state node.

    For A* to produce optimal result, requires that the estimated target cost from any node to a
    terminal state is a lower bound for the true cost.
    """
    logger.info(f"Starting A* search")
    heap = []
    heappush(heap, (init_node.get_estimated_cost(), init_node))
    cur_min_cost = None

    while len(heap) > 0:
        est_cost, cur_node = heappop(heap)
        if cur_min_cost is not None and est_cost >= cur_min_cost:
            break

        if cur_node.is_terminal():
            if cur_min_cost is None or cur_node.get_cost < cur_min_cost:
                cur_min_cost = cur_node.get_cost()
                logger.info(f"Found terminal node with min cost {cur_min_cost}")
        else:
            for next_node in cur_node.expand():
                heappush(heap, (next_node.get_estimated_cost(), next_node))

    logger.info(f"Finished A* search, min cost: {cur_min_cost}")
    return cur_min_cost
