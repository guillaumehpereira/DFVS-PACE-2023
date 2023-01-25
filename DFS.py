import sys
import random

def extract_graph():
    cpt = 0
    graph = {}


    for line in sys.stdin:
        voisins = line.split()
        voisins = [int(i) for i in voisins]
        graph[cpt] = voisins
        cpt+=1
    
    graph.pop(0)
    return graph

def vertices_out_degree_0(graph):
    vertices_out_0 = []
    for vertex in graph:
        if len(graph[vertex]) == 0:
            vertices_out_0.append(vertex)
    return vertices_out_0

def vertices_in_degree_0(graph):
    to_remove = [node for node in graph if not any(node in values for values in graph.values())]
    return to_remove

def self_pointing_nodes(graph):
    self_pointing = []
    for node, edges in graph.items():
        if node in edges:
            self_pointing.append(node)
    return self_pointing

def merge_nodes(graph, node1, node2):
    new_graph = dict(graph)
    new_graph[node1].extend(new_graph[node2])
    new_graph.pop(node2)
    for key, value in new_graph.items():
        new_graph[key] = list(set([node1 if x == node2 else x for x in value]))
    return new_graph

def vertices_out_degree_1(graph):
    for vertex in graph:
        if len(graph[vertex]) == 1:
            new_graph = merge_nodes(graph,graph[vertex],vertex)
    return new_graph

def dfs_iter(graph):
    stack = []
    visited = set()
    back_edges = []
    for vertex in graph:
        if vertex not in visited:
            stack.append(vertex)
            visited.add(vertex)
            while stack:
                current = stack.pop()
                for neighbor in graph[current]:
                    if neighbor not in visited:
                        stack.append(neighbor)
                        visited.add(neighbor)
                    else:
                        back_edges.append((current, neighbor))
    return back_edges

def remove_vertex(graph, vertex_to_remove):
    # Supprimer le sommet du graphe
    del graph[vertex_to_remove]
    # Supprimer les arcs qui pointent vers le sommet ￃﾠ supprimer
    for vertex in graph:
        if vertex_to_remove in graph[vertex]:
            graph[vertex].remove(vertex_to_remove)
    return graph

def most_common_vertex(edge_list):
    vertex_count = {}
    # Compter les occurrences de chaque sommet
    for edge in edge_list:
        for vertex in edge:
            if vertex not in vertex_count:
                vertex_count[vertex] = 0
            vertex_count[vertex] += 1
    # Trouver le sommet le plus frￃﾩquent
    most_common_vertex = None
    count = 0
    for vertex, vertex_count in vertex_count.items():
        if vertex_count > count:
            count = vertex_count
            most_common_vertex = vertex
    # Supprimer tous les couples contenant ce sommet
    edge_list = [edge for edge in edge_list if most_common_vertex not in edge]
    return most_common_vertex, edge_list

def detect_cycle(graph):
    visited = set()
    recStack = set()

    def dfs(node):
        visited.add(node)
        recStack.add(node)

        for neighbour in graph[node]:
            if neighbour not in visited:
                if dfs(neighbour):
                    return True
            elif neighbour in recStack:
                return True

        recStack.remove(node)
        return False

    for node in graph:
        if node not in visited:
            if dfs(node):
                return True

    return False




#graph = {1:[2],2:[1,5],3:[4],4:[3,5],5:[6],6:[7],7:[8],8:[6,9],9:[]}
graph = extract_graph()

DFVS = self_pointing_nodes(graph)

for i in DFVS:
    graph = remove_vertex(graph, i)

vertices_degree_out_0 = vertices_out_degree_0(graph)

for i in vertices_degree_out_0:
    graph = remove_vertex(graph, i)

vertices_degree_in_0 = vertices_in_degree_0(graph)

for i in vertices_degree_in_0:
    graph = remove_vertex(graph, i)

list_of_vertices_to_remove = []
back_edges = dfs_iter(graph)
while back_edges:
    
    vertex_to_remove = most_common_vertex(back_edges)[0]
    list_of_vertices_to_remove.append(vertex_to_remove)
    #graph = remove_vertex(graph, vertex_to_remove)
    back_edges = most_common_vertex(back_edges)[1]

#print(len(list_of_vertices_to_remove))

while(detect_cycle(graph)):
    
    I = random.choice(list_of_vertices_to_remove)
    #print(I)
    list_of_vertices_to_remove.remove(I)
    graph = remove_vertex(graph, I)
    DFVS.append(I)
    

for i in DFVS:
    print(i)
