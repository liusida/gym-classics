from abc import ABCMeta, abstractmethod

import gym
from gym.spaces import Discrete
import numpy as np


class BaseEnv(gym.Env, metaclass=ABCMeta):
    """Abstract base class for shared functionality between all environments."""

    def __init__(self, n_actions):
        self._transition_cache = {}

        # Make look-up tables for quick state-to-integer conversion and vice-versa
        all_states = list(self._decoded_states())
        self._encoder = {}
        self._decoder = {}
        i = 0
        for state in all_states:
            self._encoder[state] = i
            self._decoder[i] = state
            i += 1

        self.observation_space = Discrete(len(all_states))
        self.action_space = Discrete(n_actions)

    def seed(self, seed=None):
        self.action_space.seed(seed)
        return [seed]

    def states(self):
        """Returns a generator over all possible environment states."""
        return range(self.observation_space.n)

    @abstractmethod
    def _decoded_states(self):
        """Returns a generator over all possible underlying (non-encoded) states in the
        environment. Used internally to initialize the encoder/decoder."""
        raise NotImplementedError

    def _encode(self, state):
        """Converts a raw state into a unique integer."""
        return self._encoder[state]

    def _decode(self, i):
        """Reverts an encoded integer back to its raw state."""
        return self._decoder[i]

    def actions(self):
        """Returns a generator over all possible agent actions."""
        return range(self.action_space.n)

    def transitions(self, state, action):
        """Returns the transitions from the given state-action pair."""
        sa_pair = (state, action)
        if sa_pair in self._transition_cache:
            return self._transition_cache[sa_pair]

        n = self.observation_space.n
        next_states = np.arange(n)
        dones = np.zeros(n)
        rewards = np.zeros(n)
        probabilities = np.zeros(n)

        for s, r, p, d in self._generate_transitions(state, action):
            dones[s] = float(d)
            rewards[s] = r
            probabilities[s] += p

        i = np.nonzero(probabilities)

        assert np.allclose(probabilities.sum(), 1.0)
        transition = (next_states[i], dones[i], rewards[i], probabilities[i])
        self._transition_cache[sa_pair] = transition
        return transition

    @abstractmethod
    def _generate_transitions(self, state, action):
        """Returns a generator over all transitions from this state-action pair.

        Should be overridden in the subclass.
        """
        raise NotImplementedError
