import matplotlib.pyplot as plt
from data import Point


class ConvexHull():

    instance = None

    def __init__(self, instance):
        assert instance
        self.instance = instance

    @staticmethod
    def is_turn_right(pt1, pt2, pt3):
        """
        is_turn_right returns True if pt3 makes vector from pt1 to pt2 turn right
        :param pt1:
        :param pt2:
        :param pt3:
        :return:
        """

        pt2x = pt2.x - pt1.x
        pt2y = pt2.y - pt1.y
        pt3x = pt3.x - pt1.x
        pt3y = pt3.y - pt1.y

        cross_product = (pt2x * pt3y) - (pt2y * pt3x)

        if cross_product < 0:
            return True

        return False

    def convex_hull(self, points):
        """
            points is an array of instance's customer index
        """
        # print("points", points)
        points = [(customer_index, self.instance.nodes[customer_index]['pt'])
                  for customer_index in points]

        if len(points) <= 2:
            return points
            
        # 1. Sort the points by x-coordinate, resulting in a sequence p1,..., pn.
        sorted_points = sorted(points, key=lambda point: point[1])
        l_upper = [sorted_points[0], sorted_points[1]]

        for i in range(2, len(sorted_points)):
            l_upper.append(sorted_points[i])
            while len(l_upper) > 3 and not self.is_turn_right(l_upper[-3][1], l_upper[-2][1], l_upper[-1][1]):
                del l_upper[-2]

        l_lower = [sorted_points[-1], sorted_points[-2]]

        for i in range(len(sorted_points)-2, -1, -1):
            l_lower.append(sorted_points[i])
            while len(l_lower) > 3 and not self.is_turn_right(l_lower[-3][1], l_lower[-2][1], l_lower[-1][1]):
                del l_lower[-2]
        l_lower = l_lower[1:-1]
        
        return l_upper + l_lower
        # return list(dict.fromkeys(l_upper + l_lower))
