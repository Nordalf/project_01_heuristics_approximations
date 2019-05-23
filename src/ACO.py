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
import numpy as np

c = 1.0 # Original number of trails
alpha = 1 # controls pheromone importance
beta = 5 # controls the distance priority - should be greater than alpha
evaporation = 0.05 # percentage of how much pheromone is evaporated pr iteration
ant_factor = 0.8 # the amount of ants used pr request

max_iterations = 1000

global_best = 0

def euclideanDistance(coordinate1, coordinate2):
    return pow(pow(coordinate1.x - coordinate2.x, 2) + pow(coordinate1.y - coordinate2.y, 2), .5)

class Trail:
    visited_trail = 0
    def __init__(self, pheromone_level):
        self.pheromone_level = pheromone_level
        visited_trail += 1

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
    pheromone_level = 1.0 / len(data.nodes) # Default level. Set to low. The value goes to 1.0
    
    # Construct Canonical Solution Randomly
    while(len(not_visited_nodes) != 0): # Run as long as there are requests
        # random.seed(len(not_visited_nodes))
        picked_choice = random.choice(list(not_visited_nodes)) # Pick a random request
        # trail =  # Create a new Trail, consisting of the random ID and pheromone level
        # pheromone_map.get(current_request):
        pheromone_map[current_request] = Trail(picked_choice, pheromone_level)

        # distance = euclideanDistance(data.nodes[current_request]["pt"], data.nodes[picked_choice["id"]]["pt"]) # Calculate the distance
        if q+not_visited_nodes[picked_choice]["rq"] <= data.capacity: # Check capacity constraint
            q += not_visited_nodes[picked_choice]["rq"] # Update the current capacity used for the route
            current_request = picked_choice # New current request
            del not_visited_nodes[picked_choice] # Remove request from the list
            print("LEN: ", len(not_visited_nodes))
            route += [current_request-1]
        else:
            solution.routes += [route+[0]]
            route = [0]
            q = data.nodes[current_request]["rq"]

    print("Pheromone Map: ", pheromone_map)
    return solution

def pick_move(pheromone, distance, visited):
    pheromone = 
        
        
def algorithm(data, solution, seed=None):
    random.seed(seed)
    solution = aco(data, solution)

    print("Cost", solution.cost())
    return solution



