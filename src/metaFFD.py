import random
import math


def ffd(data, solution):

    max_cap = data.capacity
    sorted_cap = sorted(
        data.customers, key=lambda customer: customer['rq'], reverse=True)
    solution.routes = [[0]]
    for customer in sorted_cap:
        # find bin to fit
        is_fit = False
        for r_index in range(len(solution.routes)):
            route_cap = solution.route_index_capacity(r_index)
            if route_cap + customer['rq'] < max_cap:  # fits
                solution.routes[r_index].append(data.nodes.index(customer))
                is_fit = True
                break
        if not is_fit:  # not fits, add new route
            solution.routes.append([0])
            solution.routes[-1].append(data.nodes.index(customer))
    return solution


def lkh(data, solution):
    # @TODO implementation of lkh
    for route in solution.routes:

        for (route_index, customer1) in enumerate(route):
            around = (route[route_index-1],
                      route[(route_index+1) % len(route)])
            for customer2 in around:
                x1 = (customer1, customer2)
                print(x1)

                # find link such that produce better tour after perform exchange move
                y1_list = data.lkh_y1_candidate(route, x1)
                for ((t2, t3), dist) in y1_list:
                    if t3 in around:
                        continue
                    print((t2, t3), dist)

        break

    return solution


def two_opt_subsegments(N):
    return [(i, i + length)
            for length in reversed(range(2, N))
            for i in reversed(range(N - length + 1))]


def two_opt_if_improvement(tour, i, j, distance):
    A, B, C, D = tour[i-1], tour[i], tour[j-1], tour[j % len(tour)]
    if distance(A, B) + distance(C, D) > distance(A, C) + distance(B, D):
        tour[i:j] = reversed(tour[i:j])
        return True


def two_opt_first_gain(tour, distance):
    while True:
        improvements = {two_opt_if_improvement(tour, i, j, distance)
                        for (i, j) in two_opt_subsegments(len(tour))}
        if improvements == {None}:
            return tour


def routes_two_opt(routes, distance):
    for route_index in range(len(routes)):
        routes[route_index] = two_opt_first_gain(
            routes[route_index], distance)
    return routes


def is_accept(before_length, after_length, temp):
    # using try to avoid OverflowError when math.exp is too low
    try:
        prob = math.exp(-(after_length - before_length) /
                        temp)
        accept = random.random() <= prob
        # print("del", after_length-before_length,
        #       "temp", temp,
        #       "inexp", -(after_length - before_length) / temp,
        #       "prob", prob,
        #       "is better", before_length > after_length,
        #       "is accept", accept
        #       )
        return accept
    except OverflowError:
        return False


def get_exchangable_nodes(data, route, from_point, from_route_curr_cap, to_route_curr_cap):

    max_cap = data.capacity
    incoming_node_cap = data.nodes[from_point]['rq']

    upper_bound = max_cap - (from_route_curr_cap - incoming_node_cap)
    lower_bound = to_route_curr_cap - (max_cap - incoming_node_cap)
    # print(upper_bound, lower_bound)
    possible_nodes = []
    nodes = random.sample(route, 3)

    def all_possible_comb(current_node, current_cap, knapsack):
        if current_node == len(nodes):
            cap_sum = data.route_capacity(knapsack)
            # check if solution is still feasible after move points in knapsack to other route
            if cap_sum > lower_bound:
                possible_nodes.append(knapsack)
            return

        # not take depot
        if nodes[current_node] == 0:
            all_possible_comb(current_node + 1, current_cap, list(knapsack))
        else:
            # not take this node
            all_possible_comb(current_node + 1, current_cap, list(knapsack))

            # take this node
            if (current_cap + data.nodes[nodes[current_node]]['rq'] <= upper_bound):
                knapsack.append(nodes[current_node])
                current_cap += data.nodes[nodes[current_node]]['rq']
                all_possible_comb(current_node + 1,
                                  current_cap, list(knapsack))

    all_possible_comb(0, 0, [])

    return possible_nodes
    # print("poss", possible_nodes, lower_bound, upper_bound)
    # point_cap = []
    # if to_route_curr_cap + incoming_node_cap < max_cap:
    #     point_cap.append("n")

    # for p in route:
    #     if max_cap >= ((from_route_curr_cap - incoming_node_cap) + data.nodes[p]['rq']) and max_cap >= ((to_route_curr_cap - data.nodes[p]['rq']) + incoming_node_cap) and p != 0:
    #         point_cap.append(p)

    # return point_cap


def simulated_annealing(data, solution, distance, temp=1000, alpha=0.95, trying=100, output_file=None):
    # simulated_annealing is a metaheuristic method
    # temp = initial temperature
    # alpha = parameter to perform geometric cooling
    # trying = number of trying when better tour is not found
    first_sol = solution.routes.copy()
    first_sol_cost = solution.cost()

    best_cost_found = first_sol_cost
    current_improving_routes_cost = first_sol_cost

    while True:
        # start with frist sol
        improving_routes = first_sol.copy()
        current_iter_best_cost = first_sol_cost
        current_improving_routes_cost = first_sol_cost
        curr_try = 0
        curr_temp = temp

        while True:
            # simulated annealing iteration
            if curr_try > trying:
                break
            # randomly choose customer to exchange
            from_route = random.randint(0, len(improving_routes)-1)
            from_point = random.choice(
                [p for p in improving_routes[from_route] if p != 0])
            from_point_index = improving_routes[from_route].index(
                from_point)

            # randomly choose route to exchange to
            to_route = random.randint(0, len(improving_routes) - 2)
            if to_route >= from_route:
                to_route = (to_route + 1) % len(improving_routes)

            to_cand_list = get_exchangable_nodes(
                data, improving_routes[to_route], from_point, data.route_capacity(improving_routes[from_route]), data.route_capacity(improving_routes[to_route]))
            # randomly select candidate from to exchange
            if len(to_cand_list) == 0:
                # no candidate to swap
                # print("no candidate")
                continue

            to_points = random.choice(to_cand_list)
            from_temp_tour = improving_routes[from_route].copy()
            to_temp_tour = improving_routes[to_route].copy()

            if not to_points:
                # check is array is empty
                # just move point from route "from" to route "to"
                to_temp_tour.append(from_temp_tour[from_point_index])
                del from_temp_tour[from_point_index]
            else:
                from_temp_tour += to_points
                to_temp_tour.append(from_temp_tour[from_point_index])

                del from_temp_tour[from_point_index]
                to_temp_tour = [n for n in to_temp_tour if n not in to_points]

            from_temp_tour = two_opt_first_gain(from_temp_tour, distance)
            to_temp_tour = two_opt_first_gain(to_temp_tour, distance)

            before_tours_cost = data.route_length(
                improving_routes[from_route]) + data.route_length(improving_routes[to_route])
            after_tours_cost = data.route_length(
                from_temp_tour) + data.route_length(to_temp_tour)

            after_cost = current_improving_routes_cost - \
                before_tours_cost + after_tours_cost
            # print('[before]f : {}, t:{} cost:{}'.format(
            #     improving_routes[from_route], improving_routes[to_route], before_cost))
            # print('[after]f : {}, t:{} cost:{}'.format(
            #     from_temp_tour, to_temp_tour, after_cost))

            if is_accept(current_iter_best_cost, after_cost, curr_temp):
                improving_routes[from_route] = from_temp_tour
                improving_routes[to_route] = to_temp_tour

                current_improving_routes_cost = after_cost
                # print(current_improving_routes_cost, current_iter_best_cost, best_cost_found)
                curr_temp *= alpha
                curr_try = 0

                if current_improving_routes_cost < current_iter_best_cost:
                    current_iter_best_cost = current_improving_routes_cost
                    if current_improving_routes_cost < best_cost_found:
                        best_cost_found = current_improving_routes_cost
                        solution.routes = improving_routes.copy()
                        if output_file is not None:
                            assert solution.valid_solution()
                            solution.write_to_file(output_file+'.sol')
            else:
                curr_try += 1

        # update temp
    return solution


def algorithm(data, solution, seed=4, output_file=None):
    random.seed(seed)
    solution = ffd(data, solution)
    solution.routes = solution.routes
    first_sol = solution

    first_sol.routes = routes_two_opt(first_sol.routes, data.pre_distance)
    if output_file is not None:
        assert solution.valid_solution()
        solution.write_to_file(output_file+'.sol')
    solution = simulated_annealing(
        data, solution, data.pre_distance, output_file=output_file)
    return solution
