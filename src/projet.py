import sys


#Fonctions pour la méthode avec les arcs arrières

def extract_graph():
    cpt = 0
    graph = {}
    for line in sys.stdin:
        voisins = line.split()
        voisins = [int(i) for i in voisins]
        graph[cpt] = voisins
        cpt+=1

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
                    if neighbor in graph:  
                        if neighbor not in visited:
                            stack.append(neighbor)
                            visited.add(neighbor)
                        else:
                            back_edges.append((current, neighbor))
    return back_edges


def remove_vertex(graph, vertex_to_remove):
    
    del graph[vertex_to_remove]
    
    return graph


def most_common_vertex(edge_list):
    vertex_count = {}
   
    for edge in edge_list:
        for vertex in edge:
            if vertex not in vertex_count:
                vertex_count[vertex] = 0
            vertex_count[vertex] += 1
    
    most_common_vertex = None
    count = 0
    for vertex, vertex_count in vertex_count.items():
        if vertex_count > count:
            count = vertex_count
            most_common_vertex = vertex
    # Supprimer tous les couples contenant ce sommet
    edge_list = [edge for edge in edge_list if most_common_vertex not in edge]
    return most_common_vertex, edge_list


def contains_cycle(graph):
    visited = set()
    recStack = set()

    def dfs(node):
        visited.add(node)
        recStack.add(node)

        for neighbour in graph[node]:
            if neighbour in graph:    
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


def remove_vertices_from_scc(SCC):
    removed = []
    for i in SCC:
        if len(i) > 1:
            for j in range (1,len(i)):
                removed.append(i[j])
    return removed


def simplified_graph(graph,DFVS):

    for i in DFVS:
        graph = remove_vertex(graph, i)

    vertices_degree_out_0 = vertices_out_degree_0(graph)

    for i in vertices_degree_out_0:
        graph = remove_vertex(graph, i)

    vertices_degree_in_0 = vertices_in_degree_0(graph)

    for i in vertices_degree_in_0:
        graph = remove_vertex(graph, i)
    
    return graph


def LVR(back_edges):

    list_of_vertices_to_remove = []

    while back_edges:
        
        vertex_to_remove = most_common_vertex(back_edges)[0]
        list_of_vertices_to_remove.append(vertex_to_remove)
        back_edges = most_common_vertex(back_edges)[1]
    
    return list_of_vertices_to_remove

def optimised_DFVS(graph, DFVS): 
    
    while(contains_cycle(graph)):
            
            I = list_of_vertices_to_remove.pop(0)
            graph = remove_vertex(graph, I)
            DFVS.append(I)

    return DFVS


#Fonctions pour la méthode avec les CFC


def transpose_graph(graph):
    transposed_graph = {}
    for vertex in graph:
        transposed_graph[vertex] = []
    for vertex in graph:
        for neighbour in graph[vertex]:
            transposed_graph[neighbour].append(vertex)
    return transposed_graph


def dfs_iterative(graph):
    visited = set()
    stack = []
    suffix_order = []
    for vertex in graph:
        if vertex not in visited:
            stack.append(vertex)
            while stack:
                current_vertex = stack.pop()
                if current_vertex not in visited:
                    visited.add(current_vertex)
                    suffix_order.append(current_vertex)
                    for neighbour in graph[current_vertex]:
                        if neighbour not in visited:
                            stack.append(neighbour)
    return suffix_order


def find_scc(graph):
    visited = set()
    stack = []
    transposed_graph = transpose_graph(graph)
    suffix_order = dfs_iterative(transposed_graph)
    scc = []
    while suffix_order:
        vertex = suffix_order.pop()
        if vertex not in visited:
            current_scc = []
            stack.append(vertex)
            while stack:
                current_vertex = stack.pop()
                if current_vertex not in visited:
                    visited.add(current_vertex)
                    current_scc.append(current_vertex)
                    for neighbour in graph[current_vertex]:
                        if neighbour not in visited:
                            stack.append(neighbour)
            scc.append(current_scc)
    return scc

#MAIN

#graph = {1:[2],2:[1,5],3:[4],4:[3,5],5:[6],6:[7],7:[8],8:[6,9],9:[]}

graph = extract_graph()
E = graph.pop(0)[1]

#Si le graphe comporte moins de 150000 arêtes 

if E < 150000:

    DFVS = self_pointing_nodes(graph)

    graph = simplified_graph(graph,DFVS)

    back_edges = dfs_iter(graph)

    list_of_vertices_to_remove = LVR(back_edges)

    DFVS = optimised_DFVS(graph, DFVS)
    
    for i in DFVS:
        print(i)

else:
    
    SCC = find_scc (graph)
    result = remove_vertices_from_scc(SCC)

    for i in result:
        print(i)
