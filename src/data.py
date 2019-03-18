import sys
import xml.etree.ElementTree as ET
import matplotlib
import matplotlib.pyplot as plt


# Customers are represented as Points, which are a subclass of complex numbers
class Point(complex):
    x = property(lambda p: p.real)
    y = property(lambda p: p.imag)


class Data:
    capacity = 0
    nodes = tuple()
    depots = []
    decimals = 0
    def __init__(self, filename):

        tree = ET.parse(filename)
        root = tree.getroot()

        self.instance_name = root.find('info').find('name').text

        if (root.find('network').find('euclidean') is not None):
            self.decimals = int(root.find('network').find("decimals").text)
        else:
            sys.exit('Distance format not supported.')

        _requests = {node.get("node"): float(node.find("quantity").text) for node in root.find('requests').findall('request')}

        _nodes = [ {
                "id":node.get("id"),
                "pt":Point(float(node.find("cx").text),float(node.find("cy").text)),
                "tp":int(node.get("type")),
                "rq": 0 if node.get("id") not in _requests else _requests[node.get("id")]
                }
                for node in root.find('network').find('nodes').findall('node')
                ]

        self.depots = list(filter(lambda i: _nodes[i]["tp"]==0, range(len(_nodes))))

        customers = [_nodes[i] for i in range(len(_nodes)) if i not in self.depots]

        self.nodes = tuple( [_nodes[x] for x in self.depots] + customers )

        self.capacity = float(root.find('fleet').find('vehicle_profile').find('capacity').text)

        self.compute_distances()

    def short_info(self):
        sys.stdout.write("Number of nodes (incl. depots): {}. ID depot(s): {}, Decimals: {}\n"
                        .format( len(self.nodes), list(map(lambda x: self.nodes[x]["id"],self.depots)), self.decimals )
                        )

    def show(self):
        sys.stdout.write("Instance: {}\n".format(self.instance_name))
        sys.stdout.write("Number of nodes (incl. depots): {}\n".format( len(self.nodes) ) )
        sys.stdout.write("Capacity: {}\n".format(self.capacity))
        #sys.stdout.write("Nodes: {}\n".format(self.nodes))

    def pre_distance(self,i,j):
        if j<i:
            return(self.distances[(j,i)])
        else:
            return(self.distances[(i,j)])

    def compute_distances(self):
        self.distances=dict()
        for i in range(len(self.nodes)-1):
            for j in range(i+1,len(self.nodes)):
                self.distances.update({(i,j):self.distance_idx(i,j)})

    def distance_idx(self, i, j):
        return self.distance(self.nodes[i]["pt"],self.nodes[j]["pt"])

    def distance(self,A, B):
        "The distance between two points."
        return round(abs(A - B),self.decimals)

    def plot_points(self, outputfile_name=None):
        "Plot instance points."
        style='bo'
        plt.plot([node["pt"].x for node in self.nodes], [node["pt"].y for node in self.nodes], style)
        plt.plot([self.nodes[0]["pt"].x], [self.nodes[0]["pt"].y], "rs")
        plt.axis('scaled'); plt.axis('off')
        if outputfile_name is None:
            plt.show()
        else:
            plt.savefig(outputfile_name)