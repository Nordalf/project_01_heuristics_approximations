

def euclideanDistance(coordinate1, coordinate2):
    return pow(pow(coordinate1.x - coordinate2.x, 2) + pow(coordinate1.y - coordinate2.y, 2), .5)


def algorithm(data, solution):
    # To implement
    "This heuristic algorithm runs through the destinations like a two dimensional array"
    "The first loop is more a less to ensure every node is visited"
    "The second loop starts at node 0 and finds its nearest neightbor. The nearest neightbor is then set to the current node"
    "to continue the path from that node. This continues until no more capacity is available in the truck."
    "This continues until all nodes have been visited."
    route = [0]
    q = 0
    # Just to have a ******** number
    shortestDistance = 10000000
    current = 0
    visited = []
    for i in range(len(data.nodes)-1):
        for j in range(1, len(data.nodes)):
            temp = euclideanDistance(
                data.nodes[current]["pt"], data.nodes[j]["pt"])
            if j not in visited:
                if temp <= shortestDistance:
                    shortestDistance = temp
                    current = j
                    visited += [j]
                    if q+data.nodes[current]["rq"] <= data.capacity:
                        q += data.nodes[current]["rq"]
                        # if len(route) > 0:
                        #     solution.costVal += shortestDistance
                        route += [current]
                    else:
                        # solution.costVal += shortestDistance
                        solution.routes += [route+[0]]
                        route = [0, current]
                        q = data.nodes[current]["rq"]
        shortestDistance = 10000000

    solution.routes += [route+[0]]
    solution.routes = solution.routes
    return solution
