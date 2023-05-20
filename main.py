from graphs_init.graph_read import read_undirected_graph
from tasks.task1_1 import *
from random import sample

def write_output_to_file(output_filename: str, output: List[str]):
    with open(output_filename, "w") as out:
        for s in output:
            out.write(s + "\n")

if __name__ == '__main__':
    output=[]
    filename="small-graph"
    graph=read_undirected_graph(filename, 1)
    output.append("Количество вершин и рёбер графа:"+str(graph.v)+","+str(graph.e))
    dense=(2*graph.e)/((graph.v-1)*graph.v)
    output.append("Плотность графа:"+str(dense))
    mwcc,wcc_count=get_max_weakly_connected_component(graph)
    output.append("Число компонент слабой связности:"+str(wcc_count))
    output.append("Доля вершин:"+str( len(mwcc)/graph.e))
    random_part=sample(mwcc, min(500, len(mwcc)))
    r,d,p=calculate_radius_diameter_percentile(graph,random_part)
    output.append("Радиус, диаметр, 90 процентиль:"+str(r)+","+str(d)+","+str(p))
    acl=average_clustering(graph,random_part)
    output.append("Средний кластерный коэффициент для наибольшей компоненты слабой связности:"+str( acl))
    coef=calculate_coef_pirs(graph,random_part)
    output.append("Коэффициент ассортативности:"+str(coef))
    write_output_to_file("output/"+filename+".txt", output)
