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
    # print("temp", temp, "cond", math.exp(-(after_length-before_length)/temp))
    return random.random() <= math.exp(-(after_length-before_length)/temp)


def simulated_annealing(data, solution, distance, temp=1000, iteration=1000000, alpha=0.95):

    improving_routes = solution.routes.copy()
    best_cost_found = solution.cost()

    for i in range(iteration):
        temp = iteration/(i+1)
        # randomly choose customer to exchange
        from_route = random.randint(0, len(improving_routes)-1)
        from_point = random.choice(
            [p for p in improving_routes[from_route] if p != 0])
        from_point_index = improving_routes[from_route].index(
            from_point)

        from_point_cap = data.nodes[from_point]['rq']
        from_route_remaining_cap = data.capacity - (data.route_capacity(improving_routes[from_route]) -
                                                    from_point_cap)

        # randomly choose route to exchange to
        to_route = random.randint(0, len(improving_routes) - 2)
        if to_route >= from_route:
            to_route += 1
        # to_route_remaining_cap = data.capacity - \
        #     solution.route_index_capacity(to_route)
        to_cand_list = [p for p in improving_routes[to_route]
                        if data.nodes[p]['rq'] <= from_route_remaining_cap and p != 0]
        # randomly select candidate from to exchange
        if len(to_cand_list) == 0:
            # no candidate to swap
            continue
        else:
            to_point = random.choice(to_cand_list)
            to_point_index = improving_routes[to_route].index(
                to_point)

        # print("from: ", improving_routes[from_route], from_point,
        #       from_point_cap, from_route_remaining_cap)
        # print("to: ", improving_routes[to_route],
        #       to_cand_list, to_point)

        # do exchange and 2 opt, look at the improvement
        # from_temp_tour = improving_routes[from_route][:from_point_index-1] + \
        #     [to_point] + \
        #     improving_routes[from_route][from_point_index:]
        # to_temp_tour = improving_routes[to_route][:to_point_index-1] + \
        #     [from_point] + \
        #     improving_routes[to_route][to_point_index:]
        from_temp_tour = improving_routes[from_route].copy()
        to_temp_tour = improving_routes[to_route].copy()
        from_temp_tour[from_point_index], to_temp_tour[to_point_index] = to_temp_tour[to_point_index], from_temp_tour[from_point_index]
        # print(from_point, to_point,from_temp_tour,to_temp_tour)
        from_temp_tour = two_opt_first_gain(from_temp_tour, distance)
        to_temp_tour = two_opt_first_gain(to_temp_tour, distance)

        before_cost = data.route_length(
            improving_routes[from_route]) + data.route_length(improving_routes[to_route])
        
        after_cost = data.route_length(
            from_temp_tour) + data.route_length(to_temp_tour)
        # print('[before]f : {}, t:{} cost:{}'.format(
        #     improving_routes[from_route], improving_routes[to_route], before_cost))
        # print('[after]f : {}, t:{} cost:{}'.format(
        #     from_temp_tour, to_temp_tour, after_cost))

        if is_accept(before_cost, after_cost, temp):
            improving_routes[from_route] = from_temp_tour
            improving_routes[to_route] = to_temp_tour
            
            new_cost = sum([data.route_length(r) for r in improving_routes])
            print(new_cost)
            if new_cost < best_cost_found:
                best_cost_found = new_cost
                solution.routes = improving_routes.copy()

        # update temp
    return solution


def algorithm(data, solution, seed=4):
    random.seed(seed)
    solution = ffd(data, solution)
    old_cost = solution.cost()

    solution.routes = routes_two_opt(solution.routes, data.pre_distance)
    solution = simulated_annealing(data, solution, data.pre_distance)
    print("improvement", old_cost - solution.cost())
    return solution
