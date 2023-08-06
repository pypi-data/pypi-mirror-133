""" Example code for solving part 2 of https://adventofcode.com/2021/day/21. """

import itertools
from collections import deque
from typing import Iterable, List

from loguru import logger

from searchalg.node import Node
from searchalg.state import State

ROLL_COMB_MAP = {
    k: len([x for x in itertools.product([1, 2, 3], repeat=3) if sum(x) == k]) for k in range(3, 10)
}


class GameState(State):
    def __init__(self, num_combs: int, pos: int, cur_sum: int, num_steps: int):
        self.num_combs = num_combs
        self.pos = pos  # in range [1, 10]
        self.cur_sum = cur_sum
        self.num_steps = num_steps

    def is_terminal(self) -> bool:
        return self.cur_sum >= 21

    def next_states(self) -> Iterable['State']:
        """ Simulate that player plays and return the possible next states."""
        for pos_forward in range(3, 10):
            next_pos = (((self.pos + pos_forward) - 1) % 10) + 1
            next_num_combs = self.num_combs * ROLL_COMB_MAP[pos_forward]  # idx 0 corresponds to 1

            yield GameState(next_num_combs, next_pos, cur_sum=self.cur_sum + next_pos, num_steps=self.num_steps + 1)

    def __repr__(self):
        return f"GameState(pos={self.pos}, combs={self.num_combs}, cur_sum={self.cur_sum}, num_steps={self.num_steps})"


def compute_win_lose_combinations(init_node: Node):
    step_win_combs = {k: 0 for k in range(11)}
    step_lose_combs = {k: 0 for k in range(11)}

    lifo = deque([init_node])

    cnt_expanded = 0
    while len(lifo) > 0:
        node = lifo.pop()
        if node.is_terminal():
            # terminal means won with this number of steps
            step_win_combs[node.state.num_steps] += node.state.num_combs
        else:
            # non-terminal means not yet won with this number of steps
            step_lose_combs[node.state.num_steps] += node.state.num_combs
            assert not node.is_expanded
            cnt_expanded += 1
            next_nodes = node.expand()
            lifo.extend(next_nodes)

    logger.debug(f"Expanded {cnt_expanded} nodes")
    return step_win_combs, step_lose_combs


def compute_total_win_combs(player, player_loses, player_wins):
    total_win_combs = 0
    for num_win_steps in player_wins[player]:
        if num_win_steps > 0:
            total_win_combs += (player_wins[player][num_win_steps] * player_loses[(player + 1) % 2][num_win_steps - 1])
    return total_win_combs


def simulate_universes(positions: List[int]):
    player_wins = {}
    player_loses = {}
    for player in [0, 1]:
        init_state = GameState(1, positions[player], cur_sum=0, num_steps=0)
        init_node = Node(state=init_state)

        win, lose = compute_win_lose_combinations(init_node)

        logger.debug(f"Player {player}: win: {win}")
        logger.debug(f"Player {player}: lose: {lose}")
        player_wins[player] = win
        player_loses[player] = lose

    logger.info(f"Player 0 wins: {player_wins}, player 0 loses: {player_loses}")

    logger.info(f"Finding win / lose combinations for player 0")
    total_win_combs = compute_total_win_combs(0, player_loses, player_wins)
    total_lose_combs = compute_total_win_combs(1, player_loses, player_wins)
    return total_win_combs, total_lose_combs


def main():
    positions = [8, 7]
    num_universes = simulate_universes(positions)
    logger.info(f"{num_universes} universes exist where player 1 / 2 win. ")


if __name__ == '__main__':
    main()
