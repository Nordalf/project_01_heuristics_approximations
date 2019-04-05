def algorithm(data, solution):

    """
    This heuristic algorithm has following behavior
    1 ) Pick a point furthest from depot which is not in the solution route
    2 ) Grows point to nearest neighbor until the capacity is reached, save those points as cluster
    3 ) Send a vehicle to all point in each cluster
    4 ) Repeat
    """
    # convex_points = convex_hull(data.customers)
    exclude_list = []
    while len(exclude_list) < len(data.customers):
        route = [0]
        capacity = 0
        cost = 0

        curr_point = data.furthest_point(0, excluded=exclude_list)
        exclude_list.append(curr_point[0])
        route += [int(curr_point[0])]
        capacity += data.nodes[int(curr_point[0])]['rq']

        while capacity < data.capacity:
            if len(exclude_list)-2 == len(data.customers):
                break
            closest = data.closest_customer_point(curr_point[0], excluded=exclude_list)
            if closest[0] == -1:
                break
            c = data.nodes[closest[0]]['rq']
            if c + capacity > data.capacity:
                break
            route += [closest[0]]
            cost += closest[1]
            capacity = capacity + data.nodes[closest[0]]['rq']
            exclude_list.append(closest[0])
        if route[-1] != 0:
            route = route + [0]

        solution.routes += [route]
    return solution

