from graphs_init.undirected_graph import UndirectedGraph
from typing import Set, Tuple, List
from math import inf

#Функция для нахождения максимальной по мощности компоненты слабой связности и числа компонент слабой связности
def get_max_weakly_connected_component(graph: UndirectedGraph) -> Tuple[List[int], int]:
    max_component = []
    wcc_count=0
    # Проходися BFS'ом от вершины, которую ещё не посетили
    visited = {k: False for k in graph.edge_map.keys()}
    for k in graph.edge_map.keys():
        if not visited[k]:
            component = []
            queue = set()
            queue.add(k)
            while queue:
                v = queue.pop()
                visited[v] = True
                component.append(v)
                for i in graph.edge_map[v].keys():
                    if not visited[i]:
                        queue.add(i)
            if len(component)>len(max_component):
                max_component=list(component)
            wcc_count+=1
    return max_component, wcc_count

#Функция для нахождения экцентриситета вершины и количества вершин, находящихся на расстоянии i от неё
def calculate_eccentricity_and_ranges(graph: UndirectedGraph, start: int, random_part: List[int]) -> Tuple[int, List[int]]:
    ranges = [0]
    eccentricity = 0
    #Проходися BFS'ом и если натыкаемся на -1, значит обработка всех соседних вершин на расстоянии distance закончена
    queue = [start, -1]
    visited = set()
    visited.add(start)
    distance = 1
    while queue:
        next = queue.pop(0)
        if next == -1:
            if not queue:
                break
            distance += 1
            ranges.append(0)
            queue.append(-1)
            continue
        for neighbour in graph.edge_map[next].keys():
            if neighbour not in visited:
                if neighbour in random_part:
                    eccentricity = max(eccentricity, distance)
                    ranges[-1] += 1
                visited.add(neighbour)
                queue.append(neighbour)
    return eccentricity, ranges

#Функция для вычисления радиуса, диаметра, 90 процентиля расстояний (работает только для графов с большим количеством связных вершин)
def calculate_radius_diameter_percentile(graph: UndirectedGraph, nodes: List[int]) -> Tuple[int, int, int]:
    ranges = [] #Массив для хранения количества вершин на i позиции, до которых можно дойти за i+1 шаг из любой другой вершины
    radius = inf
    diameter = 0
    for i in range(len(nodes)):
        eccentricity, node_ranges = calculate_eccentricity_and_ranges(graph, nodes[i], nodes)
        #Объединим два массива для дальнешего вычисления процентиля
        for j in range(min(len(ranges), len(node_ranges))):
            ranges[j] += node_ranges[j]
        if len(node_ranges) > len(ranges):
            ranges += node_ranges[len(ranges):]
        radius = min(eccentricity, radius) #Радиус-минимальное из эксцентриситетов вершин
        diameter = max(eccentricity, diameter) #Диаметр-максимальное из эксцентриситетов вершин
    percentile = calculate_percentile(ranges)
    return radius, diameter, percentile

#Функция для вычисления 90 процентиля расстояний (можно ещё посчитать, закинув)
def calculate_percentile(ranges: List[int]) -> int:
    p=90
    n = sum(ranges)
    #Вычисляем индекс по формуле
    index = round(p * n / 100) - 1 
    #Ищем расстояние для 90% перцентиля по индексу
    part_sum_ranges = 0
    for j in range(len(ranges)):
        if part_sum_ranges <= index < part_sum_ranges + ranges[j]:
            return j + 1
        part_sum_ranges += ranges[j]
    return -1

#Функция для вычисления среднего кластерного коэффициента в компоненте слабой связности (всё по формуле)
def average_clustering(graph: UndirectedGraph, nodes: List[int]) -> float:
    Cl=0
    for node in nodes:
        neigbours=graph.edge_map[node].keys()
        gamma=len(neigbours)
        if gamma>=2:
            visited = []
            visited.append(node)
            Lu=0
            for neigbour in neigbours:
                for nn in graph.edge_map[neigbour].keys():
                    if nn in neigbours and nn not in visited:
                        Lu+=1
                visited.append(neigbour)
            Cl+=2*Lu/(gamma*(gamma-1))
    return Cl/graph.v

#Функция для вычисления коэффициента корреляции Пирсона (всё по формуле)
def calculate_coef_pirs(graph: UndirectedGraph, nodes: List[int]) -> float:
    R1=0
    R2=0
    R3=0
    Re=0
    for node_1 in nodes:
        neigbours=graph.edge_map[node_1].keys()
        k_i=len(neigbours)
        R1+=k_i
        R2+=(k_i**2)
        R3+=(k_i**3)
        for node_2 in nodes:
            if node_2==node_1:
                continue
            else:
                if node_2 in neigbours: 
                    k_j=len(graph.edge_map[node_2].keys())
                    Re+=(k_i*k_j)
    return (Re*R1-R2**2)/(R3*R1-R2**2)

