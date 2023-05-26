from graphs_init.graph_read import read_undirected_graph
from tasks.task1_1 import *
from tasks.feature_3 import *
from random import sample

def write_output_to_file(output_filename: str, output: List[str]):
    with open(output_filename, "w") as out:
        for s in output:
            out.write(s + "\n")

if __name__ == '__main__':
    output=[]
    filename="sample"
    graph=read_undirected_graph(filename, 1)
    output.append("Количество вершин и рёбер графа:"+str(graph.v)+","+str(graph.e))
    dense=(2*graph.e)/((graph.v-1)*graph.v)
    output.append("Плотность графа:"+str(dense))
    mwcc,wcc_count=get_max_weakly_connected_component(graph)
    output.append("Число компонент слабой связности:"+str(wcc_count))
    output.append("Доля вершин:"+str(len(mwcc)/graph.v))
    random_part=sample(mwcc, min(500, len(mwcc)))
    snowball_part=get_snowball(graph,mwcc,3,500)
    r_rand,d_rand,p_rand=calculate_radius_diameter_percentile(graph,random_part)
    r_snow,d_snow,p_snow=calculate_radius_diameter_percentile(graph,snowball_part)
    output.append("Радиус, диаметр, 90 процентиль (случайно выбранные вершины):"+str(r_rand)+","+str(d_rand)+","+str(p_rand))
    output.append("Радиус, диаметр, 90 процентиль (метод snowball):"+str(r_snow)+","+str(d_snow)+","+str(p_snow))
    acl=average_clustering(graph,mwcc)
    output.append("Средний кластерный коэффициент для наибольшей компоненты слабой связности:"+str(acl))
    coef=calculate_coef_pirs(graph,mwcc)
    output.append("Коэффициент ассортативности:"+str(coef))
    write_output_to_file("output/"+filename+".txt", output)
    node_activities=get_node_activities(graph,10000000)
    random_part=sample(mwcc,1)
    snowball_for_regression=get_snowball(graph,mwcc,1,10000)
    X,Y=get_x_y(graph, node_activities,snowball_for_regression)
    for i in range(len(X)):
       print("--------------------------------")
       print(X[i])
       print(Y[i])
    
