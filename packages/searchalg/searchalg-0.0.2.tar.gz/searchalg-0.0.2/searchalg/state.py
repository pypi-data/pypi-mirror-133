from typing import Iterable


class State:
    def get_cost(self):
        """ Returns the cost from initial to current state. """
        raise NotImplemented

    def get_est_target_cost(self):
        """ Returns the estimated cost from current to target state. """
        raise NotImplemented

    def is_terminal(self) -> bool:
        """ Returns true when this is a final state. """
        raise NotImplemented

    def next_states(self) -> Iterable['State']:
        raise NotImplemented

    def __repr__(self):
        raise NotImplemented("Please override __repr__ for nicer debugging :)")
