import matplotlib.pyplot as plt


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
            points is an array of Point
        """
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
        convex = l_upper + l_lower
        style = 'bo-'
        plt.plot()

        for (label, p) in points:
            plt.text(p.x, p.y, '  ' + str(label))
        plt.plot([point[1].x for point in convex] + [convex[0][1].x], [
                point[1].y for point in convex] + [convex[0][1].y], style)
        plt.show()

        return l_upper + l_lower
