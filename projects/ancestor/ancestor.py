from util import Graph, Stack, Queue

def earliest_ancestor(ancestors, starting_node):
    graph = Graph()

    # Add vertices
    for i in ancestors:
        if i[0] not in graph.vertices:
            graph.add_vertex(i[0])
        if i[1] not in graph.vertices:
            graph.add_vertex(i[1])

    # Add edges
    for i in ancestors:
        graph.add_edge(i[1], i[0])

    path = graph.bft(starting_node)
    oldest = path[-1]

    if starting_node == oldest:
        return -1
    else:
        return oldest
