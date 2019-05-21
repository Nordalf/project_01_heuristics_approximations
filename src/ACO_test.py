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

    


    class Trail:
        visited_trail = 0
        def __init__(self, pheromone):
            self.pheromone = pheromone
            visited_trail += 1

    def aco(self, data, solution, max_iterations=5):
        route = [0]
        Q = data.capacity # Max Capacity
        no_of_requests = len(data.nodes)
        pheromone = 1 / no_of_requests # Default level. Set to low. The value goes to 1.0
        q = 0 # Collected capacity
        distance = 0
        not_visited_nodes = {}
        
        local_best = 0
        local_best_route = []

        counter = 0
        while counter <= max_iterations:
            print("Counter: ", counter)
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
            
            sum_of_all_available_requests_score = 0
            
            while len(not_visited_nodes) != 0:
                for key, _ in not_visited_nodes.items():
                    distance = euclideanDistance(data.nodes[current_request]['pt'], data.nodes[key]['pt']) # Calculate the distance
                    request_to_request_score = pheromone ** self.alpha * ((1.0 / distance) ** self.beta) # Calculate the probabiltity
                    
                    sum_of_all_available_requests_score += request_to_request_score # Summation of all scores
                    self.probability_of_going_to_request[key] = request_to_request_score

                for key, value in self.probability_of_going_to_request.items():
                    prob_go_to_request = value / sum_of_all_available_requests_score
                    if current_request in self.pheromone_map:
                        if key in self.pheromone_map[current_request]:
                            
                            if self.pheromone_map[current_request][key]["pheromone"] > prob_go_to_request:
                                # print("Pheromone entry better: ", self.pheromone_map[current_request][key]["pheromone"])
                                picked_request = key # Take route with most pheromone
                    if prob_go_to_request > previous_score: # If the probability is higher, choose this point
                        picked_request = key # The highest probability request is chosen
                        
                    previous_score = prob_go_to_request
                
                # Since we have found the next address to visit, we can append the pheromone level
                selected_next_address_distance = euclideanDistance(data.nodes[current_request]['pt'], data.nodes[picked_request]['pt'])
                pheromone_level_for_chosen_address = 1 / selected_next_address_distance
                
                if current_request in self.pheromone_map.keys():
                    if picked_request in self.pheromone_map[current_request].keys():
                        new_pheromone = self.pheromone_map[current_request][picked_request]["pheromone"] + pheromone_level_for_chosen_address
                        self.pheromone_map[current_request][picked_request]["pheromone"] = new_pheromone
                else:
                    
                    self.pheromone_map[current_request] = {
                    picked_request : {
                            "pheromone": pheromone_level_for_chosen_address # 1 / (distance between two cities)
                        }
                    }
                # print(self.pheromone_map)
                self.probability_of_going_to_request.clear() # Clear the probability map for next check
                sum_of_all_available_requests_score = 0 # Reset SUM for the next iteration


                if q+not_visited_nodes[picked_request]['rq'] <= Q: # Check capacity constraint
                    q += not_visited_nodes[picked_request]["rq"] # Update the current capacity used for the route
                    current_request = picked_request # New current request
                    del not_visited_nodes[current_request] # Remove request from the list
                    # print("LENGTH: ", len(not_visited_nodes))
                    if len(not_visited_nodes) == 0: # Since the while loop is going to end after this, we are adding the route to all the routes
                        solution.routes += [route+[0]]
                        route = [0]
                    route += [current_request]
                else:
                    solution.routes += [route+[0]]
                    route = [0]
                    q = data.nodes[current_request]["rq"]
            cost = solution.cost()
            print("N Cost: ", cost)
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
            for i in range(2, len(self.pheromone_map)):
                for j in range(2, len(self.pheromone_map[i])):
                    self.pheromone_map[i][j]["pheromone"] = self.pheromone_map[i][j]["pheromone"] * (1 - self.evaporation)
            counter += 1
            # print("Pheromone Map: ", self.pheromone_map)
        print(self.global_best_route)
        solution.routes = self.global_best_route
        
        return solution
        
        
    def algorithm(self, data, solution, seed=None):
        random.seed(seed)
        solution = self.aco(data, solution, 10000 )
        # local_best = solution.cost()
        
        print("Cost", self.global_best)
        return solution



