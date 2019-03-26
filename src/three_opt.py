
def move_three_opt(tour, i, j, k, case):
    def reverse_tour(tour, i, j):
        if i > j:
            i, j = j, i
        tour[i:j] = reversed(tour[i:j])
        return tour

    def case_1(tour, i, j, k):
        return reverse_tour(tour, (k + 1) % len(tour), i)

    def case_2(tour, i, j, k):
        return reverse_tour(tour, (j + 1) % len(tour), k)

    def case_3(tour, i, j, k):
        return reverse_tour(tour, (i + 1) % len(tour), j)

    def case_4(tour, i, j, k):
        tour = reverse_tour(tour, (j + 1) % len(tour), k)
        return reverse_tour(tour, (i + 1) % len(tour), j)

    def case_5(tour, i, j, k):
        tour = reverse_tour(tour, (k + 1) % len(tour), i)
        return reverse_tour(tour, (i + 1) % len(tour), j)

    def case_6(tour, i, j, k):
        tour = reverse_tour(tour, (k + 1) % len(tour), i)
        return reverse_tour(tour, (j + 1) % len(tour), k)

    def case_7(tour, i, j, k):
        tour = reverse_tour(tour, (k + 1) % len(tour), i)
        tour = reverse_tour(tour, (i + 1) % len(tour), j)
        return reverse_tour(tour, (j + 1) % len(tour), k)

    switcher = {
        1: case_1,
        2: case_2,
        3: case_3,
        4: case_4,
        5: case_5,
        6: case_6,
        7: case_7,
    }

    func = switcher[case]
    return func(tour, i, j, k)


def three_opt(x1, x2, y1, y2, z1, z2, dist_func):
    # #  case 1 a'bc;  2-opt (i,k)
    # delete_cost_case_1 = dist_func(x1, x2) + dist_func(z1, z2)
    # add_cost_case_1 = dist_func(x1, z1) + dist_func(x2, z2)

    # #  case 2 abc';  2-opt (j,k)
    # delete_cost_case_2 = dist_func(y1, y2) + dist_func(z1, z2)
    # add_cost_case_2 = dist_func(y1, z1) + dist_func(y2, z2)

    # #  case 3 ab'c;  2-opt (i,j)
    # delete_cost_case_3 = dist_func(x1, x2) + dist_func(y1, y2)
    # add_cost_case_3 = dist_func(x1, y1) + dist_func(x2, y2)

    # # PURE 3-OPT MOVES
    # # NOTE: all 3 edges to be removed, so the same formula for del_Length
    # # A) move equal to two subsequent 2-opt moves, asymmetric
    # # B) move equal to three subsequent 2-opt moves, symmetric

    # case 4 ab'c'
    # add_cost_case_4 = dist_func(x1, y1) + dist_func(x2, z1) + dist_func(y2, z2)

    # case 5 a'b'c
    # add_cost_case_5 = dist_func(x1, z1) + dist_func(y2, x2) + dist_func(y1, z2)

    # case 6 a'bc'
    add_cost_case_6 = dist_func(x1, y2) + dist_func(z1, y1) + dist_func(x2, z2)
    # case 7 a'b'c'
    add_cost_case_7 = dist_func(x1, y2) + dist_func(z1, x2) + dist_func(y1, z2)

    delete_cost_3_opt = dist_func(
        x1, x2) + dist_func(y1, y2) + dist_func(z1, z2)

    result_tuple = (
        # (1, delete_cost_case_1 - add_cost_case_1),
        # (2, delete_cost_case_2 - add_cost_case_2),
        # (3, delete_cost_case_3 - add_cost_case_3),
        # (4, delete_cost_3_opt - add_cost_case_4),
        # (5, delete_cost_3_opt - add_cost_case_5),
        (6, delete_cost_3_opt - add_cost_case_6),
        (7, delete_cost_3_opt - add_cost_case_7),
    )

    best_gain = max(result_tuple, key=lambda gain: gain[1])

    print("i={} j={} k={}".format(x1, y1, z1))
    print("case_6={}\t case_7={} best={}".format(delete_cost_3_opt -
                                                 add_cost_case_6, delete_cost_3_opt - add_cost_case_7, best_gain[0]))

    return best_gain


def three_opt_best_gain(tour, dist_func):
    locally_opt = False
    sum_gain = 0

    last_candidate_node_i, last_candidate_node_j, last_candidate_node_k = None, None, None
    last_opt_case = None

    while not locally_opt:
        locally_opt = True
        best_gain = 0
        opt_case = None
        candidate_node_i, candidate_node_j, candidate_node_k = None, None, None

        i, j, k = 0, 0, 0

        for l_1 in range(len(tour)-1):
            i = l_1
            x1 = tour[i]
            x2 = tour[(i + 1) % len(tour)]
            for l_2 in range(1, len(tour) - 3):
                j = (i + l_2) % len(tour)
                y1 = tour[j]
                y2 = tour[(j + 1) % len(tour)]

                for l_3 in range(l_2 + 1, len(tour) - 1):
                    k = (i + l_3) % len(tour)
                    z1 = tour[k]
                    z2 = tour[(k + 1) % len(tour)]

                    case, gain = three_opt(x1, x2, y1, y2, z1, z2, dist_func)
                    if gain > best_gain:
                        print("found better tour")
                        best_gain = gain
                        opt_case = case
                        candidate_node_i, candidate_node_j, candidate_node_k = i, j, k

                        locally_opt = False

        print(last_candidate_node_i == candidate_node_i,
              last_candidate_node_j == candidate_node_j,
              last_candidate_node_k == candidate_node_k,
              last_candidate_node_k == candidate_node_k, last_opt_case, opt_case, last_opt_case == opt_case)
        if last_candidate_node_i == candidate_node_i and \
            last_candidate_node_j == candidate_node_j and \
            last_candidate_node_k == candidate_node_k and \
           last_opt_case == opt_case:
            locally_opt = True

        if not locally_opt:
            print(tour)
            tour = move_three_opt(tour, candidate_node_i, candidate_node_j,
                                  candidate_node_k, opt_case)
            print(tour)

            last_candidate_node_i, last_candidate_node_j, last_candidate_node_k = candidate_node_i, candidate_node_j, candidate_node_k
            last_opt_case = opt_case

            sum_gain += best_gain

    return tour, sum_gain


def algorithm(solution):

    def distance(i, j):
        return solution.instance.pre_distance(i, j)

    for route_index in range(len(solution.routes)):
        solution.routes[route_index], gain = three_opt_best_gain(
            solution.routes[route_index][:-1], distance)
        solution.costVal -= gain

    return solution
