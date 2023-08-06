from typing import Set, Optional, Iterable

from searchalg.state import State


class Node:
    def __init__(self, state: State, prev_node: 'Node' = None, next_nodes: Optional[Set['Node']] = None):
        self.prev_node = prev_node
        self.next_nodes = set() if next_nodes is None else next_nodes
        self.is_expanded = False
        self.state = state

    def get_estimated_cost(self) -> int:
        return self.state.get_cost() + self.state.get_est_target_cost()

    def get_cost(self) -> int:
        return self.state.get_cost()

    def is_terminal(self):
        return self.state.is_terminal()

    def expand(self, ref_prev=False, ref_next=False) -> Iterable['Node']:
        """ Expands next nodes. By default, does not store references to previous / next nodes when expanding. """
        prev_node = None
        if ref_prev:
            prev_node = self

        next_nodes = set()
        if self.is_terminal():
            raise ValueError("Node to be expanded is already final!")
        if not self.is_expanded:
            for state in self.state.next_states():
                next_nodes.add(
                    Node(state=state, prev_node=prev_node)
                )
            self.is_expanded = True
            if ref_next:
                self.next_nodes = next_nodes
        return next_nodes

    def __lt__(self, other):
        return self.get_estimated_cost() < other.get_estimated_cost()

    def __repr__(self):
        return f"Node(state={self.state})"
