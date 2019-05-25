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

# TODO
# Create a map of pheromone between two points
# Append pheromone on a trail already visited
# Decay pheromone at every iteration. Decay with small amounts 

# 23/05/2019 - NOT WORKING. 

import random
import numpy as np


def euclideanDistance(coordinate1, coordinate2):
    return pow(pow(coordinate1.x - coordinate2.x, 2) + pow(coordinate1.y - coordinate2.y, 2), .5)

class Ant:
    """
        Ants build solutions probabilistically without updating pheromone trails
    """
    c = 1.0 # Original number of trails
    alpha = 1 # controls pheromone importance
    beta = 5 # controls the distance priority - should be greater than alpha
    evaporation = 0.05 # percentage of how much pheromone is evaporated / decayed pr iteration
    ant_factor = 0.8 # the amount of ants used pr request

    no_of_ants = 5 # The number of ants needed to try and find a solution
    max_iterations = 1000 # The maximum number of iterations one ant is going to try

    pheromone_map = {} # A dictionary of the pheromone level from one request to another
    probability_of_going_to_request = {} # The Pheromone Map

    global_best = 0
    global_best_route = []

    def aco(self, data, solution, max_iterations=5):
        route = [0]
        Q = data.capacity # Max Capacity
        # pheromone_trails = [] # Default level. Set to low. The value goes to 1.0
        q = 0 # Collected capacity
        distance = 0
        not_visited_nodes = {}
        
        local_best = 0
        local_best_route = []
        
        sum_of_all_available_requests_score = 0

        # Start by initializing all the pheromone level
        for first_entry in range(len(data.nodes)):
            self.pheromone_map[data.nodes[first_entry]['id']] = {}
            for second_entry in range(1, len(data.nodes)):
                if first_entry != second_entry:
                    distance = euclideanDistance(data.nodes[first_entry]['pt'], data.nodes[second_entry]['pt']) # Calculate the distance
                    init_pheromone = 1 / distance
                    self.pheromone_map[data.nodes[first_entry]['id']][data.nodes[second_entry]['id']] = {"pheromone": init_pheromone }
                    sum_of_all_available_requests_score += self.pheromone_map[data.nodes[first_entry]['id']][data.nodes[second_entry]['id']]["pheromone"] # Summation of all scores
        
        for i in range(1, len(data.nodes)):
            not_visited_nodes[data.nodes[i]["id"]-1] = {
                    "id": data.nodes[i]["id"]-1,
                    "rq": data.nodes[i]["rq"],
                }
            # Cop   y the problem instance to play with
            
        current_request = random.choice(list(not_visited_nodes)) # The first choice is random chosen
        q += not_visited_nodes[current_request]["rq"] # Update the current capacity used for the route
        route += [current_request] # Add it to the route

        del not_visited_nodes[current_request] # Remove the randomly picked, since it has been "marked" as visited now
        # print("First Random Picked: ", current_request)
            
        counter = 0
        while counter <= max_iterations:
            if counter != 0:
                for i in range(len(data.nodes)):
                    not_visited_nodes[data.nodes[i]['id']] = {
                            'id': data.nodes[i]['id'],
                            'pt': data.nodes[i]['pt'],
                            'rq': data.nodes[i]['rq'],
                        }
                    # Copy the problem instance to play with
                print(not_visited_nodes)
                current_request = 1
                previous_score = 0
                picked_request = 0
                
                while len(not_visited_nodes) != 0:
                    for key, value in self.pheromone_map[current_request].items():
                        if len(not_visited_nodes) == 1:
                            if key in not_visited_nodes.keys():
                                picked_request = key
                                print(picked_request)
                                break
                        request_to_request_score = self.pheromone_map[current_request][key]["pheromone"] ** self.alpha * ((1.0 / distance) ** self.beta) # Calculate the probabiltity
                        prob_go_to_request = request_to_request_score / sum_of_all_available_requests_score
                        if previous_score == 0: # one time
                            if key in not_visited_nodes.keys():
                                previous_score = prob_go_to_request
                                picked_request = key
                        if prob_go_to_request > previous_score: # If the probability is higher, choose this point
                            # print(not_visited_nodes.keys())
                            if key in not_visited_nodes.keys():
                                picked_request = key # The highest probability request is chosen
                                

                        previous_score = prob_go_to_request
                    
                    # Since we have found the next address to visit, we can append the pheromone level
                    # if len(not_visited_nodes) > 1:
                    print("Current: ", current_request, " - Picked: ", picked_request, " - Len NV: ", len(not_visited_nodes))
                    selected_next_address_distance = euclideanDistance(data.nodes[current_request-1]['pt'], data.nodes[picked_request-1]['pt'])
                    self.pheromone_map[current_request][picked_request]["pheromone"] += 1 / selected_next_address_distance
                
                    if q+not_visited_nodes[picked_request]['rq'] <= Q: # Check capacity constraint
                        q += not_visited_nodes[picked_request]["rq"] # Update the current capacity used for the route
                        current_request = picked_request # New current request
                        del not_visited_nodes[current_request] # Remove request from the list
                        if len(not_visited_nodes) == 0: # Since the while loop is going to end after this, we are adding the route to all the routes
                            route += [current_request]
                            solution.routes += [route+[0]]
                            route = [0]
                        route += [current_request]
                        previous_score = 0
                    else:
                        current_request = picked_request # Starting point for next
                        solution.routes += [route+[0]]
                        route = [0]
                        route += [current_request]
                        del not_visited_nodes[current_request] # Remove request from the list
                        q = data.nodes[current_request]["rq"]
                        previous_score = 0

                cost = solution.cost()
                if local_best == 0:
                    local_best = cost
                    self.global_best = cost
                if cost < local_best:
                    local_best = cost
                    local_best_route = solution.routes
                    print("New Local Best Route")
                    if local_best < self.global_best:
                        self.global_best = local_best
                        self.global_best_route = solution.routes
                        print("New Global Best Route")
                # Reset the route
                route = []
                # Reset the solution routes
                solution.routes = []
                # Evaporate by .05 % for every pheromone trail
                for i in range(1, len(self.pheromone_map)):
                    for j in range(1, len(self.pheromone_map[i])):
                        if i != j:
                            self.pheromone_map[i][j]["pheromone"] = self.pheromone_map[i][j]["pheromone"] * (1 - self.evaporation)
            counter += 1
                # print("Pheromone Map: ", self.pheromone_map)
        print(self.global_best_route)
        solution.routes = self.global_best_route
        
        return solution
        
        
    def algorithm(self, data, solution, seed=None, output_file=None):
        random.seed(seed)
        solution = self.aco(data, solution, 5000 )
        # local_best = solution.cost()
        
        print("Cost", self.global_best)
        return solution



