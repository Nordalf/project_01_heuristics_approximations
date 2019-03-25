import signal
from error import TimeOutExeption


class LocalSearch:
    solution = None
    alg = None

    def __init__(self, solution=None, alg=None):
        assert solution is not None
        assert alg is not None
        self.solution = solution
        self.alg = alg

    def timeoutHandler(self, signumb, frame):
        raise TimeOutExeption(self.solution)

    def construct(self, time_left):
        signal.signal(signal.SIGALRM, self.timeoutHandler)
        signal.alarm(int(time_left))
        return self.localsearch()

    def localsearch(self):
        self.solution = self.alg(self.solution)
        return self.solution
