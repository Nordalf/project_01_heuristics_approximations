import sys
import matplotlib
import matplotlib.pyplot as plt

import data


class Solution:
    total_distance = 0
    routes = []

    def __init__(self, instance):
        self.instance = instance
        # the initialization for the containers for your solutions representation here
        pass

    def __repr__(self):
        return str(self.__class__) + ": " + str(self.__dict__)

    def valid_solution(self):
        "To check whether a solution is valid, we are going to ensure the arcs enters"
        "and leaves each vertex exactly once. We also need to check the number of vehicles leaving and entering a depot"
        " are equal. Lastly then we ensure the capacity for each vehicle does not exceed their maximum capacity."
        "The capacity is handled in the solverCH.py, when the solution is being created"
        # To complete

        isValid = True
        # Lets start of by checking the arcs of the solution.
        leavingVehicles = 0
        enteringVehicles = 0
        for firstRoute in self.routes:
            if firstRoute[0] == 0:
                leavingVehicles += 1
            if firstRoute[-1] == 0:
                enteringVehicles += 1
            for secondRoute in self.routes:
                if firstRoute != secondRoute:
                    # Constraint #1
                    # If there are any points greater than 0, then two routes intersect
                    for i in self.intersection(firstRoute, secondRoute):
                        if i > 0:
                            isValid = False

        # Constraint #2
        if leavingVehicles == enteringVehicles:
            print("Leaving Vehicles: \t", leavingVehicles,
                  "\nEntering Vehicles: \t", enteringVehicles)
        else:
            isValid = False
        print("The validity of the solution  is: ", isValid)
        return (isValid)

    def cost(self):

        return sum([self.instance.route_length(r) for r in self.routes])

    def write_to_file(self, filename):
        with open(filename, "w") as filehandle:
            for route in self.routes:
                filehandle.write(
                    ",".join(map(lambda x: str(self.instance.nodes[x]["id"]), route)) + "\n")

    def plot_lines(self, points, color=None, style='bo-'):
        "Plot lines to connect a series of points."
        plt.plot([self.instance.nodes[p]["pt"].x for p in points], [self.instance.nodes[p]["pt"].y for p in points],
                 style, color=color)
        plt.axis('scaled')
        plt.axis('off')

    def plot_instance_points(self):
        self.instance.plot_points(show=False)

    def plot_routes(self, split=False, output_filename=None):
        "routes is a list of routes (alternatively it can be a grand route).  The depot is red square."
        colormap = plt.cm.get_cmap('hsv', len(self.routes))

        if split:
            ax1 = plt.subplot(1, len(self.routes), 1)
            for (index, route) in enumerate(self.routes):
                start = route[0]
                plt.subplot(1, len(self.routes), index +
                            1, sharex=ax1, sharey=ax1)
                self.plot_instance_points()
                self.plot_lines(
                    list(route) + [start], color=colormap(index), style="o-")
                # Mark the start city with a red square
                self.plot_lines([start], style='rs')
        else:
            c = 0
            for route in self.routes:
                start = route[0]
                self.plot_instance_points()
                self.plot_lines(
                    list(route) + [start], color=colormap(c), style="o-")
                # Mark the start city with a red square
                self.plot_lines([start], style='rs')
                c += 1
        if output_filename is None:
            plt.show()
        else:
            plt.savefig(output_filename)

    @staticmethod
    def intersection(array1, array2):
        "This method compares two arrays whether they have any elements in common."
        "It is done to uphold the first constraint of no routes are overlapping"
        return [value for value in array1 if value in array2]

    @staticmethod
    def plot_table(outputfile_name=None, inserted_row_labels=None, table_vals=None):
        "Filling a table with results"
        fig = plt.figure()
        col_labels = ['Instance', 'KLB', 'Cost',
                      'Time (sec)', 'Cost', 'Time (sec)']
        row_labels = [inserted_row_labels]
        # Draw table
        the_table = plt.table(cellText=[table_vals],
                              rowLabels=row_labels,
                              colLabels=col_labels,
                              loc='center')
        the_table.auto_set_font_size(False)
        the_table.set_fontsize(24)
        the_table.scale(4, 4)

        # Removing ticks and spines enables you to get the figure only with table
        plt.tick_params(axis='x', which='both', bottom=False,
                        top=False, labelbottom=False)
        plt.tick_params(axis='y', which='both', right=False,
                        left=False, labelleft=False)
        for pos in ['right', 'top', 'bottom', 'left']:
            plt.gca().spines[pos].set_visible(False)

        plt.savefig(outputfile_name + '.png',
                    bbox_inches='tight', pad_inches=0.05)
