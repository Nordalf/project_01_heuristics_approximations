import sys
from convex_hull import ConvexHull
import matplotlib.pyplot as plt
from data import Point


class ClusterOPT:
    """
    implementation of cluster opt for cvrp problem,
    it's compare each convex hull point of each route and move it if it make better route
    """
    solution = None

    route_convexes = None
    ch = None

    def __init__(self, solution):
        self.solution = solution
        self.ch = ConvexHull(self.solution.instance)
        self.route_convexes = [self.ch.convex_hull(route[:-1])
                               for route in self.solution.routes]

    def distance(self, i, j):
        return self.solution.instance.pre_distance(i, j)

    def route_length(self, route):
        return self.solution.instance.route_length(route)

    @staticmethod
    def mid_point(points):
        return Point(sum(points) / len(points))

    @staticmethod
    def cluster_permutation(N):
        "Generate all segments combinations"
        return ((i, j)
                for i in range(N)
                for j in range(i+1, N))

    def closest_point(self, target_point, points):
        return self.solution.instance.closest_point(
            target_point, excluded=[0], included=points)

    def convex_opt_swap_if_improvement(self, tour_i, tour_j, closest_from_j_i, closest_from_i_j):
        A, B, C = tour_i[closest_from_j_i -
                         1], tour_i[closest_from_j_i], tour_i[(closest_from_j_i + 1)]
        D, E, F = tour_j[closest_from_i_j -
                         1], tour_j[closest_from_i_j], tour_j[(closest_from_i_j + 1)]
        # print(A, B, C)
        # print(D, E, F)
        old_distance_i = self.distance(A, B) + self.distance(B, C)
        old_distance_j = self.distance(D, E) + self.distance(E, F)

        new_distance_i = self.distance(A, E) + self.distance(E, C)
        new_distance_j = self.distance(D, B) + self.distance(B, F)
        # true means new distance makes better tour
        # print("i:", old_distance_i > new_distance_i)
        # true means new distance makes better tour
        # print("j:", old_distance_j > new_distance_j)

        # true means new distance makes better tour
        print("all:", (old_distance_i + old_distance_j)
              > new_distance_i + new_distance_j)
        if (old_distance_i + old_distance_j) > (new_distance_i + new_distance_j):
            tour_i[closest_from_j_i], tour_j[closest_from_i_j] = tour_j[closest_from_i_j], tour_i[closest_from_j_i]
            return True

    def convex_opt_move_if_improvement(self, tour_i, tour_j, closest_from_i_j, closest_from_j_i):
        # print(A, B, C)
        # print(tour_i, tour_j, closest_from_i_j,
        #       closest_from_j_i, (closest_from_i_j + 1))
        A, B, C = tour_i[closest_from_j_i -
                         1], tour_i[closest_from_j_i], tour_i[(closest_from_j_i + 1)]

        D, E, F = tour_j[closest_from_i_j -
                         1], tour_j[closest_from_i_j], tour_j[(closest_from_i_j + 1)]

        old_distance_i = self.distance(A, B) + self.distance(B, C)
        old_distance_j = self.distance(D, E) + self.distance(E, F)

        new_distance_before_i = self.distance(
            A, E) + self.distance(E, B) + self.distance(B, C)
        new_distance_after_i = self.distance(
            A, B) + self.distance(B, E) + self.distance(E, C)
        new_distance_j = self.distance(D, F)

        if new_distance_before_i < new_distance_after_i:  # better visit E before B
            if (old_distance_i + old_distance_j) > (new_distance_before_i + new_distance_j):
                # it makes overall tour better
                moved_point_j = tour_j.pop(closest_from_i_j)
                # print("move", moved_point_j, "to",
                #       tour_i, "before", tour_i[closest_from_j_i])
                tour_i.insert(closest_from_j_i, moved_point_j)
                return True
        else:  # better visit B then E
            if (old_distance_i + old_distance_j) > (new_distance_after_i + new_distance_j):
                # it makes overall tour better
                moved_point_j = tour_j.pop(closest_from_i_j)
                # print("move", moved_point_j, "to",
                #       tour_i, "after", tour_i[closest_from_j_i])
                tour_i.insert(closest_from_j_i+1, moved_point_j)
                return True

    def is_capacity_reach_when_swap(self, route_i, route_j, customer_i, customer_j):
        max_capacity = self.solution.instance.capacity
        # print("is_capacity_reach_when_swap", route_i,
        #       route_j, customer_i, customer_j)
        new_capacity_i = self.solution.route_index_capacity(
            route_i) - self.solution.instance.node_capacity(customer_i) + self.solution.instance.node_capacity(customer_j)
        new_capacity_j = self.solution.route_index_capacity(
            route_j) - self.solution.instance.node_capacity(customer_j) + self.solution.instance.node_capacity(customer_i)
        return new_capacity_i >= max_capacity and new_capacity_j >= max_capacity

    def is_capacity_reach_when_move(self, route_i, customer):
        max_capacity = self.solution.instance.capacity
        # print("curr capacity", self.solution.route_index_capacity(
        # route_i))
        new_capacity_i = self.solution.route_index_capacity(
            route_i) + self.solution.instance.node_capacity(customer)

        # print("new capacity", new_capacity_i)
        return new_capacity_i >= max_capacity

    def convex_opt_closest_gain(self, routes):
        improvements = True
        while improvements:
            for (i, j) in self.cluster_permutation(len(routes)):
                if len(routes[i]) == 1 or len(routes[j]) == 1:
                    continue
                # print("before", routes[i], routes[j])
                mid_point_i = self.mid_point(
                    [point[1] for point in self.route_convexes[i]])
                mid_point_j = self.mid_point(
                    [point[1] for point in self.route_convexes[j]])

                convex_indexed_i = [point[0]
                                    for point in self.route_convexes[i]]
                convex_indexed_j = [point[0]
                                    for point in self.route_convexes[j]]
                i_j_index = self.closest_point(
                    mid_point_i, convex_indexed_j)[0]
                j_i_index = self.closest_point(
                    mid_point_j, convex_indexed_i)[0]
                if i_j_index == -1 or j_i_index == -1:
                    continue

                closest_from_i_j = routes[j].index(i_j_index)
                closest_from_j_i = routes[i].index(j_i_index)

                # print(self.is_capacity_reach_when_swap(
                #     i, j, routes[i][closest_from_j_i], routes[j][closest_from_i_j]))
                if not self.is_capacity_reach_when_move(i, routes[j][closest_from_i_j]):
                    improvements = self.convex_opt_move_if_improvement(
                        routes[i], routes[j], closest_from_i_j, closest_from_j_i)
                elif not self.is_capacity_reach_when_move(j, routes[i][closest_from_j_i]):
                    improvements = self.convex_opt_move_if_improvement(
                        routes[j], routes[i], closest_from_j_i, closest_from_i_j)
                elif not self.is_capacity_reach_when_swap(
                        i, j, routes[i][closest_from_j_i], routes[j][closest_from_i_j]):

                    # print("current capacity_{}".format(i), self.solution.route_index_capacity(
                    #     i), "current capacity_{}".format(j), self.solution.route_index_capacity(j))
                    # print("closest_from_{}_{}".format(i, j), closest_from_i_j,
                    #       "closest_from_{}_{}".format(j, i), closest_from_j_i)
                    # print("mid_point_{}".format(i), mid_point_i,
                    #       "mid_point_{}".format(j), mid_point_j)

                    improvements = self.convex_opt_swap_if_improvement(
                        routes[i], routes[j], closest_from_j_i, closest_from_i_j)
                if improvements:
                    print("after", routes[i], routes[j])
                    self.route_convexes = [self.ch.convex_hull(route[:-1])
                                           for route in self.solution.routes]

            if bool(improvements) or improvements is None:
                return routes
            # debugging plot
            # style = 'bo-'
            # plt.plot()
            # plt.text(mid_point.x, mid_point.y, '  ' + "mid")
            # plt.plot(mid_point.x, mid_point.y, style)
            # for (label, p) in route_convexes[route_index]:
            #     plt.text(p.x, p.y, '  ' + str(label))

            # plt.plot([point[1].x for point in route_convexes[route_index]] + [route_convexes[route_index][0][1].x], [
            #         point[1].y for point in route_convexes[route_index]] + [route_convexes[route_index][0][1].y], style)
            # plt.show()

    def run(self):
        self.solution.routes = self.convex_opt_closest_gain(
            self.solution.routes)
        return self.solution
