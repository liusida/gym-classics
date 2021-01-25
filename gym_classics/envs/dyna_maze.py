from gym_classics.envs.abstract.gridworld import Gridworld


class DynaMaze(Gridworld):
    """A 9x6 deterministic gridworld with barriers to make navigation more challenging.
    The agent starts on the left side at coordinates (0, 3); the goal is the top-right cell.
    Reference: cite{3} (page 192).

    **states**: Agent cell location.

    **actions**: Move up/right/down/left.

    **rewards**: +1 for reaching the goal.

    **termination**: Reaching the goal.
    """

    def __init__(self):
        blocks = frozenset({(2, 2), (2, 3), (2, 4), (5, 1), (7, 3), (7, 4), (7, 5)})
        self._goal = (8, 5)
        super().__init__(dims=(9, 6), starts={(0, 3)}, blocks=blocks)

    def _reward(self, state, action, next_state):
        return 1.0 if next_state == self._goal else 0.0

    def _done(self, state, action, next_state):
        return next_state == self._goal
