
class TimeOutExeption(Exception):
    solution = None

    def __init__(self, solution):
        super(TimeOutExeption, self).__init__(
            "construction heuristics timeout")

        self.solution = solution