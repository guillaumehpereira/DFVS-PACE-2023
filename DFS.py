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
    # Supprimer les arcs qui pointent vers le sommet à supprimer
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
    # Trouver le sommet le plus fréquent
    most_common_vertex = None
    count = 0
    for vertex, vertex_count in vertex_count.items():
        if vertex_count > count:
            count = vertex_count
            most_common_vertex = vertex
    # Supprimer tous les couples contenant ce sommet
    edge_list = [edge for edge in edge_list if most_common_vertex not in edge]
    return most_common_vertex, edge_list

graph = {1:[2],2:[1,5],3:[4],4:[3,5],5:[6],6:[7],7:[8],8:[6,9],9:[]}

list_of_vertices_to_remove = []
back_edges = dfs_iter(graph)
while back_edges:
    
    vertex_to_remove = most_common_vertex(back_edges)[0]
    list_of_vertices_to_remove.append(vertex_to_remove)
    graph = remove_vertex(graph, vertex_to_remove)
    back_edges = most_common_vertex(back_edges)[1]

print(graph,list_of_vertices_to_remove)
