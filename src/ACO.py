# Ant Colony Optimization applied on the Capacitated Vehicle Routing Problem
# We are using ants to simulate vehicles and its complete set of routes 
# is constructed by successively choosing customers to visit 
# until all the customers have been visited.
#
# A new route is started, when the constraint on the capacity has been breached. 
# each ant is assigned to a randomly chosen
# customer as its first city to visit from the depot. Then, at
# each construction step, an ant k at current city i will
# select the next city j to visit from a feasible neighborhood
# Variables needed:
#   - distance - d(i,j)
#   - heuristic value (eta) - 1/d(i,j) - the attractiveness
#   - pheromone concentration on the edges - t = tau(i, j)
#   - savings of combining two cities - m = mu(i,j)=d(i,0) + d(j,0) - d(i,j)

import random

def euclideanDistance(coordinate1, coordinate2):
    return pow(pow(coordinate1.x - coordinate2.x, 2) + pow(coordinate1.y - coordinate2.y, 2), .5)

class Trail:
    def __init__(self, id, pheromone_level):
        self.id = id
        self.pheromone_level = pheromone_level

def aco(data, solution):
    route = [0]
    Q = data.capacity # Max Capacity
    q = 0 # Collected capacity
    distance = 0
    heuristic_value = 0 # Default Value
    not_visited_nodes = {}

    for i in range(len(data.nodes)):
        not_visited_nodes[data.nodes[i]["id"]] = {
                "id": data.nodes[i]["id"],
                "pt": data.nodes[i]["pt"],
                "tp": data.nodes[i]["tp"],
                "rq": data.nodes[i]["rq"],
            }
        # Copy the problem instance to play with
    
    current_request = 1 # The depot as default
    pheromone_map = {} # A dictionary of the pheromone level from one request to another
    pheromone_level = 0.1 # Default level. Set to low. The value goes to 1.0
    while(len(not_visited_nodes) != 0): # Run as long as there are requests
        random.seed(len(not_visited_nodes))
        picked_choice = random.choice(list(not_visited_nodes)) # Pick a random request
        
        # distance = euclideanDistance(data.nodes[current_request]["pt"], data.nodes[picked_choice["id"]]["pt"]) # Calculate the distance
        if q+not_visited_nodes[picked_choice]["rq"] <= data.capacity: # Check capacity constraint
            q += not_visited_nodes[picked_choice]["rq"] # Update the current capacity used for the route
            current_request = picked_choice # New current request
            del not_visited_nodes[picked_choice] # Remove request from the list
            print("LEN: ", len(not_visited_nodes))
            trail = Trail(picked_choice, pheromone_level) # Create a new Trail, consisting of the random ID and pheromone level
            # if pheromone_map.get(current_request):
            route += [current_request]
        else:
            print("Once")
            solution.routes += [route+[0]]
            route = [0, current_request]
            q = data.nodes[current_request]["rq"]
            # pheromone_map.update({current_request: trail}) # Update the map with the ID -> trail
    return solution
        
        
def algorithm(data, solution, seed=None):
    random.seed(seed)
    solution = aco(data, solution)
    old_cost = solution.cost()

    print("improvement", old_cost - solution.cost())
    return solution



