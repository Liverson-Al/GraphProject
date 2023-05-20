from graphs_init.undirected_graph import UndirectedGraph

#функция для считывания графа
def read_undirected_graph(filename: str,split: int) -> UndirectedGraph:
    if split==0:
        split_symb="\t"
    else:
        split_symb=" "
    graph = UndirectedGraph(filename)
    with open("datasets/"+filename+".txt") as file:
        for line in file:
            if line.startswith("%"):
                continue
            node_from, node_to, w, t = line.split(split_symb)
            t=t[:-1]
            graph.add_edge(int(node_from), int(node_to), t)
    return graph