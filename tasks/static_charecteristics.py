from graphs_init.undirected_graph import UndirectedGraph
from typing import Set, Tuple, List
from math import log

#Функция для нахождения пересечения двух множеств (И)
def conjunction(graph: UndirectedGraph, u: int, v: int) -> List[int]:
    result=[]
    neigbours_1=graph.edge_map[u].keys()
    neigbours_2=graph.edge_map[v].keys()
    for k in neigbours_2:
        if k in neigbours_1:
            result.append(k)
    return result

#Функция для нахождения объединения двух множеств (ИЛИ)
def disjunction(graph: UndirectedGraph, u: int, v: int) -> List[int]:
    neigbours_1=graph.edge_map[u].keys()
    neigbours_2=graph.edge_map[v].keys()
    for k in neigbours_2:
        if k not in neigbours_1:
            neigbours_1.append(k)
    return neigbours_1

#Нахождение статических метрик по формулам
def common_neigbours(graph: UndirectedGraph, u: int, v: int) -> int:
    return len(conjunction(graph, u, v))

def adamic_adar(graph: UndirectedGraph, u: int, v: int) -> float:
    conjunction_set=conjunction(graph,u,v)
    res=0
    for k in conjunction_set:
        res+=(1/log(len(graph.edge_map[k].keys())))
    return res

def jaaccard_coefficient(graph: UndirectedGraph, u: int, v: int) -> float:
    return len(conjunction(graph,u,v))/len(disjunction(graph,u,v))

def preferential_attachment (graph: UndirectedGraph, u: int, v: int) -> int:
    neigbours_1=graph.edge_map[u].keys()
    neigbours_2=graph.edge_map[v].keys()
    return len(neigbours_1)*len(neigbours_2)

