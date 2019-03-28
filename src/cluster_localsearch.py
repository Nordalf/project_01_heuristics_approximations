import sys
from convex_hull import ConvexHull


class ClusterOPT:
    """
    implementation of cluster opt for cvrp problem,
    it's compare each convex hull point of each route and move it if it make better route
    """
    solution = None

    def __init__(self, solution):
        self.solution = solution

    def distance(self, i, j):
        return self.solution.instance.pre_distance(i, j)

    def route_length(self, route):
        return self.solution.instance.route_length(route)

    @staticmethod
    def two_opt_subsegments(N):
        return [(i, i + length)
                for length in reversed(range(2, N))
                for i in reversed(range(N - length + 1))]

    def two_opt_if_improvement(self, tour, i, j):
        A, B, C, D = tour[i-1], tour[i], tour[j-1], tour[j % len(tour)]
        if self.distance(A, B) + self.distance(C, D) > self.distance(A, C) + self.distance(B, D):
            tour[i:j] = reversed(tour[i:j])
            return True

    def two_opt_first_gain(self, tour):
        while True:
            improvements = {self.two_opt_if_improvement(tour, i, j)
                            for (i, j) in self.two_opt_subsegments(len(tour))}
            if improvements == {None}:
                return tour

    def run(self):
        ch = ConvexHull(self.solution.instance)
        for route in self.solution.routes:
            routes_points = [(customer_index, self.solution.instance.nodes[customer_index]['pt'])
                             for customer_index in route]
            convex = ch.convex_hull(routes_points[:-1])
            print(convex[:-1])
        # for route_index in range(len(self.solution.routes)):
        #     self.solution.routes[route_index] = self.two_opt_first_gain(
        #         self.solution.routes[route_index])
        return self.solution
