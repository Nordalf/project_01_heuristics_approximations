from collections import namedtuple
from pprint import pformat
from sys import maxsize
import matplotlib.pyplot as plt


class KdTreeNode(namedtuple('Node', 'pt axis left_child right_child')):

    def __repr__(self):
        return pformat(tuple(self))


class KdTree:

    root = None

    def __init__(self, nodes):
        self.root = self._construct(nodes)

    def __repr__(self):
        return repr(self.root)


    def _construct(self, nodes, depth=0):
        if len(nodes) == 0:
            return None

        if depth % 2 == 0:
            axis = 'x'
            nodes_sorted = sorted(nodes, key=lambda node: node['pt'].x)
        else:
            axis = 'y'
            nodes_sorted = sorted(nodes, key=lambda node: node['pt'].y)

        median = len(nodes_sorted) // 2

        return KdTreeNode(
            pt=nodes_sorted[median],
            axis=axis,
            left_child=self._construct(nodes_sorted[:median], depth + 1),
            right_child=self._construct(nodes_sorted[median + 1:], depth + 1),
        )
