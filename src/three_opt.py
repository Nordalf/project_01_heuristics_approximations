import sys
from collections import deque


class ThreeOpt:
    """
    implementation of three opt for travelling salesman problem
    """
    solution = None

    def __init__(self, solution):
        self.solution = solution

    def distance(self, i, j):
        return self.solution.instance.pre_distance(i, j)

    def route_length(self, route):
        return self.solution.instance.route_length(route)

    @staticmethod
    def three_opt_subsegments(N):
        "Generate all segments combinations"
        return ((i, j, k)
                for i in range(N)
                for j in range(i+2, N)
                for k in range(j + 2, N + (i > 0)))

    @staticmethod
    def rotate_til_depot_first(tour):
        dq = deque(tour)
        while dq[0] != 0:
            dq.rotate()
        return list(dq)

    def three_opt_if_improvement(self, tour, i, j, k):
        A, B, C, D, E, F = tour[i-1], tour[i], tour[j -
                                                    1], tour[j], tour[k-1], tour[k % len(tour)]
        d0 = self.distance(A, B) + self.distance(C, D) + self.distance(E, F)
        d1 = self.distance(A, C) + self.distance(B, D) + self.distance(E, F)
        d2 = self.distance(A, B) + self.distance(C, E) + self.distance(D, F)
        d3 = self.distance(A, D) + self.distance(E, B) + self.distance(C, F)
        d4 = self.distance(F, B) + self.distance(C, D) + self.distance(E, A)

        if d0 > d1:
            tour[i:j] = reversed(tour[i:j])
            return True
        elif d0 > d2:
            tour[j:k] = reversed(tour[j:k])
            return True
        elif d0 > d4:
            tour[i:k] = reversed(tour[i:k])
            return True
        elif d0 > d3:
            tmp = tour[j:k] + tour[i:j]
            tour[i:k] = tmp
            return True

    def three_opt_first_gain(self, tour):
        while True:
            improvements = True
            for (i, j, k) in self.three_opt_subsegments(len(tour)):
                improvements = self.three_opt_if_improvement(tour, i, j, k)
                if improvements and tour[0] != 0:
                    tour = self.rotate_til_depot_first(tour)
            if bool(improvements) or improvements is None:
                return tour

    def run(self):
        for route_index in range(len(self.solution.routes)):
            self.solution.routes[route_index][:-1] = self.three_opt_first_gain(
                self.solution.routes[route_index][:-1])
        return self.solution
