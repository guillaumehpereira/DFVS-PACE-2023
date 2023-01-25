import sys

def extract_graph():
    cpt = 0
    graph = {}


    for line in sys.stdin:
        voisins = line.split()
        voisins = [int(i) for i in voisins]
        graph[cpt] = voisins
        cpt+=1
    
    return graph



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

def supprsommets(scc):
    suppr = []
    for i in scc:
        if len(i)>1:
            for j in range (1,len(i)):
                suppr.append(i[j])
    return suppr
    
#graph = {1:[2],2:[1,5],3:[4],4:[3,5],5:[6],6:[7],7:[8],8:[6,9],9:[]}
graph = extract_graph()
graph.pop(0)

scc = find_scc (graph)
result = supprsommets(scc)

for i in result:
    print(i)
