def algorithm(data, solution):

    # convex_points = convex_hull(data.customers)
    exclude_list = []
    while len(exclude_list) < len(data.customers):
        route = [0]
        capacity = 0
        cost = 0

        curr_point = data.furthest_point(0, exclude_list)
        exclude_list.append(curr_point[0])
        route += [int(curr_point[0])]
        capacity += data.nodes[int(curr_point[0])]['rq']

        while capacity < data.capacity:
            if len(exclude_list)-2 == len(data.customers):
                break
            closest = data.closest_point(curr_point[0], exclude_list)
            if closest[0] == -1:
                break
            c = data.nodes[closest[0]]['rq']
            if c + capacity > data.capacity:
                break
            route += [closest[0]]
            cost += closest[1]
            capacity = capacity + data.nodes[closest[0]]['rq']
            exclude_list.append(closest[0])
        route = route + [0]
        solution.routes += [route]
        solution.costVal += cost
    return solution

