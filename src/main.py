#!/usr/bin/python3

import sys
import os
import argparse
import time
import glob

import data
import solution
import solverCH
import solverLS
import solverNN
import utilities

# @my_logger
# @my_timer

# Used for table creation
instance_times_costs = []
def solve(instance, config):
    global instance_times_costs
    temp_instance_times_costs = []
    # The default algorithm
    t0 = time.process_time() # Changed from clock to process_time due to deprecation
    ch = solverCH.ConstructionHeuristics(instance)
    sol = ch.construct(config.time_limit-t0) # returns an object of type Solution
    sol.cost(ch.total_distance) # Adds the heuristic cost to the solution
    ch.total_distance = round(ch.total_distance,2)
    print("CH COST: ", ch.total_distance)
    temp_instance_times_costs += [0,ch.total_distance, round(t0,2)]
    assert sol.valid_solution()

    # Deleting/resetting the routes to check the next solution and store it in the global array.
    del sol.routes[:]

    # The self-created algorithm inspired with searching for nearest customer
    t0 = time.process_time() # Changed from clock to process_time due to deprecation
    nn = solverNN.NearestNeighbour(instance)
    sol = nn.construct(config.time_limit-t0) # returns an object of type Solution
    sol.cost(nn.total_distance) # Adds the heuristic cost to the solution
    nn.total_distance = round(nn.total_distance,2)
    print("NN COST: ", nn.total_distance)
    temp_instance_times_costs += [nn.total_distance, round(t0,2)]
    assert sol.valid_solution()
    
    # The self-created local search algorithm, which compare routes. The local_search_adj compares with the 
    # route closes to it - from an index perspective. local_search_far compares one route with all other routes
    # and does this for all routes. 
    t0 = time.process_time() # Changed from clock to process_time due to deprecation
    ls = solverLS.LocalSearch(instance)
    sol = ls.local_search3(sol, nn.total_distance, config.time_limit-t0) # returns an object of type Solution
    sol.cost(ls.total_distance) # Adds the heuristic cost to the solution
    print("LS COST: ", ls.total_distance)
    temp_instance_times_costs += [round(ls.total_distance,2), round(t0,2)]
    assert sol.valid_solution()

    # Deleting/resetting the routes to check the next solution and store it in the global array.
    del sol.routes[:]
    #print(instance_times_costs)
    instance_times_costs += [temp_instance_times_costs+[]]
    temp_instance_times_costs = []
    return sol


def main(argv):

    parser = argparse.ArgumentParser()

    parser.add_argument('-o', action='store',
                        dest='output_file',
                        help='The file where to save the solution and, in case, plots')

    parser.add_argument('-t', action='store',
                        dest='time_limit',
                        type=int,
                        required=True,
                        help='The time limit')

    parser.add_argument('-all',action='store',
                        dest='all',
                        type=bool,
                        help='If this flag is on, then every instance file is going to be tested')

    parser.add_argument('-i', 
                        dest='instance_file',
                        action='store',
                        required=False,
                        help='The path to the file of the instance to solve')


    config = parser.parse_args()

    instance_row_labels = []
    if config.all:
        for filename in glob.glob('..\data\*\*\*.xml'):
            print('instance_file    = {!r}'.format(filename))
            print('output_file      = {!r}'.format(config.output_file))
            print('time_limit       = {!r}'.format(config.time_limit))
            instance = data.Data(filename)
            instance_row_labels += [filename]
            instance.short_info()
            sol = solve(instance,config)
            #if config.output_file is not None:
            #    instance.plot_points("../results/"+filename+'.png')
            instance.show()
    else:
        print('instance_file    = {!r}'.format(config.instance_file))
        print('output_file      = {!r}'.format(config.output_file))
        print('time_limit       = {!r}'.format(config.time_limit))
        instance = data.Data(config.instance_file)
        instance.short_info()
        if config.output_file is not None:
            instance.plot_points("../results/"+config.output_file+'.png')
        instance.show()
        sol = solve(instance,config)
    
    if config.output_file is not None:
        #sol.plot_routes("../results/"+config.output_file+'_sol'+'.png')
        #sol.write_to_file("../results/"+config.output_file+'.txt')
        sol.plot_table("../results/"+config.output_file+'_tbl', instance_row_labels, instance_times_costs)
    print("{} routes with total cost {:.1f}"
          .format(len(sol.routes), sol.costVal))

if __name__ == "__main__":
    main(sys.argv[1:])
