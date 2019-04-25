import math

from data import Data
import solution
import sys
import signal
from error import TimeOutExeption


class ConstructionHeuristics:

    instance = None
    alg = None
    solution = None

    def __init__(self, instance=None, alg=None):
        assert instance is not None
        assert alg is not None
        self.instance = instance
        self.alg = alg
        self.solution = solution.Solution(self.instance)

    def timeoutHandler(self, signum, frame):
        raise TimeOutExeption(self.solution)

    def construct(self, time_left):
        signal.signal(signal.SIGALRM, self.timeoutHandler)
        signal.alarm(math.ceil(time_left))
        return self.canonical_solution()

    def canonical_solution(self):
        self.solution = solution.Solution(self.instance)
        self.solution = self.alg(self.instance, self.solution)
        return self.solution


class MetaHeuristic:

    instance = None
    alg = None
    solution = None

    def __init__(self, instance=None, alg=None):
        assert instance is not None
        assert alg is not None
        self.instance = instance
        self.alg = alg
        self.solution = solution.Solution(self.instance)

    def timeoutHandler(self, signum, frame):
        raise TimeOutExeption(self.solution)

    def construct(self, time_left):
        signal.signal(signal.SIGALRM, self.timeoutHandler)
        signal.alarm(math.ceil(time_left))
        return self.canonical_solution()

    def canonical_solution(self):
        self.solution = solution.Solution(self.instance)
        self.solution = self.alg(self.instance, self.solution)
        return self.solution
