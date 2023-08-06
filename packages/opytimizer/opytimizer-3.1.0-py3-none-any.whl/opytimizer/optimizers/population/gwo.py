"""Grey Wolf Optimizer.
"""

import copy

import numpy as np

import opytimizer.math.random as r
import opytimizer.utils.logging as l
from opytimizer.core import Optimizer

logger = l.get_logger(__name__)


class GWO(Optimizer):
    """A GWO class, inherited from Optimizer.

    This is the designed class to define GWO-related
    variables and methods.

    References:
        S. Mirjalili, S. Mirjalili and A. Lewis. Grey Wolf Optimizer.
        Advances in Engineering Software (2014).

    """

    def __init__(self, params=None):
        """Initialization method.

        Args:
            params (dict): Contains key-value parameters to the meta-heuristics.

        """

        logger.info('Overriding class: Optimizer -> GWO.')

        # Overrides its parent class with the receiving params
        super(GWO, self).__init__()

        # Builds the class
        self.build(params)

        logger.info('Class overrided.')

    def _calculate_coefficients(self, a):
        """Calculates the mathematical coefficients.

        Args:
            a (float): Linear constant.

        Returns:
            Both `A` and `C` coefficients.

        """

        # Generates two uniform random numbers
        r1 = r.generate_uniform_random_number()
        r2 = r.generate_uniform_random_number()

        # Calculates the `A` coefficient (eq. 3.3)
        A = 2 * a * r1 - a

        # Calculates the `C` coefficient (eq. 3.4)
        C = 2 * r2

        return A, C

    def update(self, space, function, iteration, n_iterations):
        """Wraps Grey Wolf Optimization over all agents and variables.

        Args:
            space (Space): Space containing agents and update-related information.
            function (Function): A Function object that will be used as the objective function.
            iteration (int): Current iteration.
            n_iterations (int): Maximum number of iterations.

        """

        # Sorts agents
        space.agents.sort(key=lambda x: x.fit)

        # Gathers the best three wolves
        alpha, beta, delta = copy.deepcopy(space.agents[:3])

        # Defines the linear constant
        a = 2 - 2 * iteration / (n_iterations - 1)

        # Iterates through all agents
        for agent in space.agents:
            # Makes a deep copy of current agent
            X = copy.deepcopy(agent)

            # Calculates all coefficients
            A_1, C_1 = self._calculate_coefficients(a)
            A_2, C_2 = self._calculate_coefficients(a)
            A_3, C_3 = self._calculate_coefficients(a)

            # Simulates hunting behavior (Eqs. 3.5 and 3.6)
            X_1 = alpha.position - A_1 * np.fabs(C_1 * alpha.position - agent.position)
            X_2 = beta.position - A_2 * np.fabs(C_2 * beta.position - agent.position)
            X_3 = delta.position - A_3 * np.fabs(C_3 * delta.position - agent.position)

            # Calculates the temporary agent (eq. 3.7)
            X.position = (X_1 + X_2 + X_3) / 3

            # Clips temporary agent's limits
            X.clip_by_bound()

            # Evaluates temporary agent's new position
            X.fit = function(X.position)

            # Checks if new fitness is better than current agent's fitness
            if X.fit < agent.fit:
                # Updates the corresponding agent's position and fitness
                agent.position = copy.deepcopy(X.position)
                agent.fit = copy.deepcopy(X.fit)
