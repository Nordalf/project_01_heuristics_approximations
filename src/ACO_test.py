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
no_of_requests = 0
max_iterations = 1000

global_best = 0

pheromone_map = {} # A dictionary of the pheromone level from one request to another

def euclideanDistance(coordinate1, coordinate2):
    return pow(pow(coordinate1.x - coordinate2.x, 2) + pow(coordinate1.y - coordinate2.y, 2), .5)


class Ant:
    """
        Ants build solutions probabilistically without updating pheromone trails
    """
    local_best = 0
    visit_memory = [] # Memory of visited nodes
    class Trail:
        visited_trail = 0
        def __init__(self, pheromone_level):
            self.pheromone_level = pheromone_level
            visited_trail += 1

    def aco(self, data, solution):
        route = [0]
        Q = data.capacity # Max Capacity
        no_of_requests = len(data.nodes)
        pheromone_level = 1 / no_of_requests # Default level. Set to low. The value goes to 1.0
        q = 0 # Collected capacity
        distance = 0
        not_visited_nodes = {}
        
        
        for i in range(1, len(data.nodes)):
            not_visited_nodes[data.nodes[i]["id"]-1] = {
                    "id": data.nodes[i]["id"],
                    "pt": data.nodes[i]["pt"],
                    "tp": data.nodes[i]["tp"],
                    "rq": data.nodes[i]["rq"],
                }
            # Copy the problem instance to play with
                
        current_request = random.choice(list(not_visited_nodes)) # The first choice is random chosen
        q += not_visited_nodes[current_request]["rq"] # Update the current capacity used for the route
        route += [current_request] # Add it to the route

        del not_visited_nodes[current_request] # Remove the randomly picked, since it has been "marked" as visited now
        print("First Random Picked: ", current_request)
        
        # picked_choice = random.choice(list(not_visited_nodes)) # Pick a random request
        previous_score = 0
        picked_request = 0
        probability_of_going_to_request = {}
        sum_of_all_available_requests_score = 0
        while len(not_visited_nodes) != 0:
            for key, _ in not_visited_nodes.items():
                distance = euclideanDistance(data.nodes[current_request]['pt'], data.nodes[key]['pt']) # Calculate the distance
                request_to_request_score = pheromone_level ** alpha * (1.0 / distance) ** beta # Calculate the probabiltity
                
                sum_of_all_available_requests_score += request_to_request_score # Summation of all scores
                probability_of_going_to_request[key] = request_to_request_score # Probability pr request
            
            # print(probability_of_going_to_request)
            for key, value in probability_of_going_to_request.items():
                prob_go_to_request = value / sum_of_all_available_requests_score
                if prob_go_to_request > previous_score: # If the probability is higher, choose the new point
                    picked_request = key
                    
                previous_score = prob_go_to_request
            
            probability_of_going_to_request.clear() # Clear the probability map for next check
            sum_of_all_available_requests_score = 0 # Reset SUM

            # pheromone_map[current_request] = Trail(picked_choice, pheromone_level)

            if q+not_visited_nodes[picked_request]['rq'] <= data.capacity: # Check capacity constraint
                q += not_visited_nodes[picked_request]["rq"] # Update the current capacity used for the route
                current_request = picked_request # New current request
                del not_visited_nodes[current_request] # Remove request from the list
                if len(not_visited_nodes) == 0: # Since the while loop is going to end after this, we are adding the route to all the routes
                    solution.routes += [route+[0]]
                    route = [0]
                route += [current_request]
            else:
                solution.routes += [route+[0]]
                route = [0]
                q = data.nodes[current_request]["rq"]
        print("Pheromone Map: ", pheromone_map)
        return solution
        
        
    def algorithm(self, data, solution, seed=None):
        random.seed(seed)
        solution = self.aco(data, solution)
        local_best = solution.cost()
        if global_best == 0:
            global_best = local_best
        if local_best < global_best:
            global_best = local_best
        print("Cost", local_best)
        return solution



