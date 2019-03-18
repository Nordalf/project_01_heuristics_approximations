#!/usr/bin/python3

import sys
import os
import argparse
import time

import data
import solution
import solverCH
import solverLS
import solverNN
import utilities

# @my_logger
# @my_timer

ch_instance_times = []
ch_instance_costs = []
def solve(instance, config):
    t0 = time.process_time() # Changed from clock to process_time due to deprecation
    ch = solverCH.ConstructionHeuristics(instance)
    sol = ch.construct(config.time_limit-t0) # returns an object of type Solution
    sol.cost(ch.total_distance) # Adds the heuristic cost to the solution
    print("CH COST: ", ch.total_distance)
    ch_instance_times = [t0]
    ch_instance_costs = [ch.total_distance]
    assert sol.valid_solution()

    t0 = time.process_time() # Changed from clock to process_time due to deprecation
    nn = solverNN.NearestNeighbour(instance)
    sol = nn.construct(config.time_limit-t0) # returns an object of type Solution
    sol.cost(nn.total_distance) # Adds the heuristic cost to the solution
    print("NN COST: ", round(nn.total_distance,2))
    ch_instance_times = [t0]
    ch_instance_costs = [nn.total_distance]
    assert sol.valid_solution()

    #t0 = time.process_time() # Changed from clock to process_time due to deprecation
    #ls = solverLS.LocalSearch(instance)
    #sol = ls.local_search(sol, config.time_limit-t0) # returns an object of type Solution
    #print("LS COST: ", ls.total_distance)
    #assert sol.valid_solution()
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

    parser.add_argument('instance_file',action='store',
                        help='The path to the file of the instance to solve')


    config = parser.parse_args()

    print('instance_file    = {!r}'.format(config.instance_file))
    print('output_file      = {!r}'.format(config.output_file))
    print('time_limit       = {!r}'.format(config.time_limit))


    instance = data.Data(config.instance_file)
    instance.short_info()
    if config.output_file is not None:
        instance.plot_points(config.output_file+'.png')
    instance.show()

    sol = solve(instance,config)

    if config.output_file is not None:
        sol.plot_routes(config.output_file+'_sol'+'.png')
        sol.write_to_file(config.output_file+'.sol')
        sol.plot_table(config.output_file+'_tbl'+'.png', )
    print("{} routes with total cost {:.1f}"
          .format(len(sol.routes), sol.costVal))




if __name__ == "__main__":
    main(sys.argv[1:])
