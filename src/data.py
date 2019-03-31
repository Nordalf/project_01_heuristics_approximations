import sys
import xml.etree.ElementTree as ET
import matplotlib.pyplot as plt
import kd_tree
import re


# Customers are represented as Points, which are a subclass of complex numbers
class Point(complex):
    x = property(lambda p: p.real)
    y = property(lambda p: p.imag)

    def __cmp__(self, other):
        if self.x == other.x:
            return self.y > other.y

        return self.x < other.x

    def __lt__(self, other):
        if self.x == other.x:
            return self.y > other.y

        return self.x < other.x


class Data:
    capacity = 0
    nodes = tuple()
    depots = []
    customers = []
    decimals = 0
    tree = None
    distances = dict()

    def __init__(self, filename):

        tree = ET.parse(filename)
        root = tree.getroot()

        self.instance_name = root.find('info').find('name').text

        if root.find('network').find('euclidean') is not None:
            self.decimals = int(root.find('network').find("decimals").text)
        else:
            sys.exit('Distance format not supported.')

        _requests = {node.get("node"): float(node.find("quantity").text) for node in
                     root.find('requests').findall('request')}

        _nodes = [{
            "id": int(node.get("id")),
            "pt": Point(float(node.find("cx").text), float(node.find("cy").text)),
            "tp": int(node.get("type")),
            "rq": 0 if node.get("id") not in _requests else _requests[node.get("id")]
        }
            for node in root.find('network').find('nodes').findall('node')
        ]

        self.depots = list(
            filter(lambda i: _nodes[i]["tp"] == 0, range(len(_nodes))))

        self.customers = [_nodes[i]
                          for i in range(len(_nodes)) if i not in self.depots]

        self.nodes = tuple([_nodes[x] for x in self.depots] + self.customers)
        # self.tree = kd_tree.KdTree(self.nodes)

        self.capacity = float(root.find('fleet').find(
            'vehicle_profile').find('capacity').text)

        self.compute_distances()

    def __repr__(self):
        return str(self.__class__) + ": " + str(self.__dict__)

    def short_info(self):
        sys.stdout.write("Number of nodes (incl. depots): {}. ID depot(s): {}, Decimals: {}\n"
                         .format(len(self.nodes), list(map(lambda x: self.nodes[x]["id"], self.depots)), self.decimals)
                         )

    def show(self):
        sys.stdout.write("Instance: {}\n".format(self.instance_name))
        sys.stdout.write(
            "Number of nodes (incl. depots): {}\n".format(len(self.nodes)))
        sys.stdout.write("Capacity: {}\n".format(self.capacity))
        # sys.stdout.write("Nodes: {}\n".format(self.nodes))

    def pre_distance(self, i, j):
        if i == j:
            return (0)
        if j < i:
            return (self.distances[(j, i)])
        return (self.distances[(i, j)])

    def compute_distances(self):
        for i in range(len(self.nodes) - 1):
            for j in range(i + 1, len(self.nodes)):
                self.distances.update({(i, j): self.distance_idx(i, j)})

    def distance_idx(self, i, j):
        return self.distance(self.nodes[i]["pt"], self.nodes[j]["pt"])

    def distance(self, A, B):
        "The distance between two points."
        return round(abs(A - B), self.decimals)

    def node_capacity(self, node_index):
        return self.nodes[node_index]["rq"]

    def furthest_point(self, i, excluded=[], included=[]):
        max_index = -1
        max_dist = -sys.maxsize-1
        i = int(i)
        if len(included) == 0:
            included = range(len(self.nodes))
        for index in included:
            if index == i or index in excluded:
                continue
            else:
                distance = self.pre_distance(i, index)
                if distance > max_dist:
                    max_index = index
                    max_dist = distance
        return (max_index, max_dist)

    def closest_point(self, i, excluded=[], included=[]):
        min_index = -1
        min_dist = sys.maxsize
        if type(i) == Point:
            if len(included) == 0:
                included = range(len(self.nodes))
            for index in included:
                if index in excluded:
                    continue
                else:
                    distance = self.distance(i, self.nodes[index]['pt'])
                    if distance < min_dist:
                        min_index = index
                        min_dist = distance
            return (min_index, min_dist)
        else:
            i = int(i)
            if len(included) == 0:
                included = range(len(self.nodes))
            for index in included:
                if index == i or index in excluded:
                    continue
                else:
                    distance = self.pre_distance(i, index)
                    if distance < min_dist:
                        min_index = index
                        min_dist = distance
            return (min_index, min_dist)

    def route_capacity(self, route):
        return sum(self.node_capacity(point_index) for point_index in route)

    def route_length(self, route):
        return sum(self.pre_distance(route[i], route[i-1]) for i in range(len(route)))

    def plot_points(self, show=True, outputfile_name=None):
        "Plot instance points."
        style = 'bo'

        for (label, p) in enumerate(self.nodes):
            plt.text(p["pt"].x, p["pt"].y, '  ' + str(label))

        plt.plot([node["pt"].x for node in self.nodes], [
                 node["pt"].y for node in self.nodes], style)
        plt.plot([self.nodes[0]["pt"].x], [self.nodes[0]["pt"].y], "rs")
        plt.axis('scaled')
        plt.axis('off')
        if outputfile_name is None:
            if show:
                plt.show()
        else:
            plt.savefig(outputfile_name)
