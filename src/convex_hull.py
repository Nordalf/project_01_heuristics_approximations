import matplotlib.pyplot as plt


def is_turn_right(pt1, pt2, pt3):
    """
    is_turn_right returns True if pt3 makes vecter from pt1 to pt2 turn right
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

    if cross_product >= 0:
        return True

    return False


def convex_hull(points):
    # 1. Sort the points by x-coordinate, resulting in a sequence p1,..., pn.
    sorted_points = sorted(points, key=lambda node: node['pt'])
    l_upper = [sorted_points[0], sorted_points[1]]

    for i in range(3, len(sorted_points)):

        l_upper.append(sorted_points[i])
        while len(l_upper) > 3 and not is_turn_right(l_upper[-3]['pt'], l_upper[-2]['pt'], l_upper[-1]['pt']):
            del l_upper[-2]

    l_lower = [sorted_points[-1], sorted_points[-2]]

    for i in range(len(sorted_points)-2, -1, -1):
        l_lower.append(sorted_points[i])
        while len(l_lower) > 3 and not is_turn_right(l_lower[-3]['pt'], l_lower[-2]['pt'], l_lower[-1]['pt']):
            del l_lower[-2]
    l_lower = l_lower[1:]
    # convex = l_upper + l_lower
    # style = 'bo-'
    # plt.plot()
    # plt.plot([node["pt"].x for node in convex], [
    #          node["pt"].y for node in convex], style)
    # plt.show()

    return l_upper + l_lower[1:]
