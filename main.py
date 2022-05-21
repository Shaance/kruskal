#!/usr/bin/env python3
from typing import List


class UnionFind:
    def __init__(self, vertices_nb: int):
        self.parents = [vertex for vertex in range(vertices_nb)]
        self.ranks = [1 for _ in range(vertices_nb)]

    def find(self, vertex: int) -> int:
        parent = vertex
        while self.parents[parent] != parent:
            parent = self.parents[parent]

        # path compression
        while vertex != parent:
            vertex, self.parents[vertex] = self.parents[vertex], parent

        return parent

    def union(self, vertex1: int, vertex2: int) -> bool:
        """":returns True if union could be made between the 2 vertices"""
        parent1 = self.find(vertex1)
        parent2 = self.find(vertex2)

        if parent1 == parent2:
            return False

        # attach lower to higher rank will maintain a lower tree height
        if self.ranks[parent1] > self.ranks[parent2]:
            self.parents[vertex2] = parent1
        elif self.ranks[parent1] < self.ranks[parent2]:
            self.parents[vertex1] = parent2
        else:
            self.parents[vertex2] = parent1
            self.ranks[parent1] += 1

        return True


class Edge:
    def __init__(self, from_: int, to: int, weight: int):
        self.from_ = from_
        self.to = to
        self.weight = weight

    def __repr__(self) -> str:
        return f"[from:{self.from_}, to:{self.to}, weight:{self.weight}]"


class Graph:
    def __init__(self):
        self.vertices = set()
        self.edges = []

    def add_edge(self, edge: Edge):
        self.edges.append(edge)
        self.vertices.add(edge.from_)
        self.vertices.add(edge.to)

    def get_vertices_nb(self):
        return len(self.vertices)


class MinimumSpanningTree:
    def __init__(self, edges: List[Edge], weight: int):
        self.edges = edges
        self.weight = weight

    def __repr__(self) -> str:
        return f"Minimum spanning tree has total weight of {self.weight} and has the following edges {self.edges} "


def kruskal(graph: Graph) -> MinimumSpanningTree:
    """
    The returned MST will look like this with the graph created by create_graph function

             weight
    vertex1 -------> vertex2

       4     2     3     3
    0 --> 1 --> 2 --> 3 --> 4
                |
                |  1
                | --> 5

    """
    min_path_edges = []
    nb_of_vertices = len(graph.vertices)
    edges_idx = 0
    total_weight = 0
    sorted_edges = sorted(graph.edges, key=lambda e: e.weight)
    u_find = UnionFind(nb_of_vertices)

    # A tree is a fully connected graph without cycle. It can only be possible when
    # number of edges - 1 == number of vertices. More edges -> a cycle exists, less -> a vertex is not connected
    while len(min_path_edges) < graph.get_vertices_nb() - 1:
        edge = sorted_edges[edges_idx]
        edges_idx += 1
        parent_f = u_find.find(edge.from_)
        parent_t = u_find.find(edge.to)

        # if parents are the same, vertices are already connected, adding an edge will cause a cycle
        # we should not use the edge to build the MST
        if parent_f != parent_t:
            min_path_edges.append(edge)
            u_find.union(edge.from_, edge.to)
            total_weight += edge.weight

    return MinimumSpanningTree(min_path_edges, total_weight)


def create_graph() -> Graph:
    graph = Graph()
    graph.add_edge(Edge(0, 1, 4))
    graph.add_edge(Edge(0, 2, 4))
    graph.add_edge(Edge(1, 2, 2))
    graph.add_edge(Edge(1, 0, 4))
    graph.add_edge(Edge(2, 0, 4))
    graph.add_edge(Edge(2, 1, 2))
    graph.add_edge(Edge(2, 3, 3))
    graph.add_edge(Edge(2, 5, 2))
    graph.add_edge(Edge(2, 4, 4))
    graph.add_edge(Edge(3, 2, 3))
    graph.add_edge(Edge(3, 4, 3))
    graph.add_edge(Edge(4, 2, 4))
    graph.add_edge(Edge(4, 3, 3))
    graph.add_edge(Edge(5, 2, 2))
    graph.add_edge(Edge(5, 4, 3))
    return graph


def main():
    print(kruskal(create_graph()))


if __name__ == "__main__":
    main()
