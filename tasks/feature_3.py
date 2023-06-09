from graphs_init.undirected_graph import UndirectedGraph
from typing import Set, Tuple, List
import math
from random import sample
import numpy as np
from tasks.static_charecteristics import *



def get_node_activities(graph:UndirectedGraph,t_s:int):

   l=0.2
   t_min=graph.t_min
   t_max=graph.t_max
   # вычислим map весов (лин., эксп.,корн.)
   weight_map={}
      
   for i in graph.edge_map.keys():
      for j in graph.edge_map[i].keys():
         for k in range(len(graph.edge_map[i][j])):
            t=graph.edge_map[i][j][k]
            if t<=t_s and i!=j:
               if i not in weight_map.keys():
                  weight_map[i]={}
               w_l=l+(1-l)*(t-t_min)/(t_max-t_min)
               w_e=l+(1-l)*(math.e**(3*(t-t_min)/(t_max-t_min))-1)/(math.e**3 - 1)
               w_s=l+(1-l)*math.sqrt((t-t_min)/(t_max-t_min))
               list_to_append=[w_l,w_e,w_s]
               weight_map[i][j]=list_to_append

   # вычислим map активности вершин
   node_activity_map={}

   for i in weight_map.keys():
      pre_list_lin=[]
      pre_list_exp=[]
      pre_list_sqrt=[]
      for j in weight_map[i].keys():
         weight_list=weight_map[i][j]
         pre_list_lin.append(weight_list[0])
         pre_list_exp.append(weight_list[1])
         pre_list_sqrt.append(weight_list[2])

      pre_list_lin=np.array(pre_list_lin)
      pre_list_exp=np.array(pre_list_exp)
      pre_list_sqrt=np.array(pre_list_sqrt)
      first=[np.quantile(pre_list_lin,.0),
             np.quantile(pre_list_lin,.25),
             np.quantile(pre_list_lin,0.5),
             np.quantile(pre_list_lin,0.75),
             np.quantile(pre_list_lin,1.),
             np.sum(pre_list_lin),
             np.mean(pre_list_lin)]
      second=[np.quantile(pre_list_exp,.0),
             np.quantile(pre_list_exp,.25),
             np.quantile(pre_list_exp,0.5),
             np.quantile(pre_list_exp,0.75),
             np.quantile(pre_list_exp,1.),
             np.sum(pre_list_exp),
             np.mean(pre_list_exp)]
      third=[np.quantile(pre_list_sqrt,.0),
             np.quantile(pre_list_sqrt,.25),
             np.quantile(pre_list_sqrt,0.5),
             np.quantile(pre_list_sqrt,0.75),
             np.quantile(pre_list_sqrt,1.),
             np.sum(pre_list_sqrt),
             np.mean(pre_list_sqrt)]
      
      node_activity_map[i]=[first,second,third]

   output_list=[k for k in weight_map.keys()]

   return node_activity_map,output_list



def get_x_edges(graph:UndirectedGraph,node_activity_map:dict,nodes_begin:list,t_s:int):

   # для каждой пары вершин найдём характеристики из feature3(3)
   counted_edges=[]
   X=[]

   for i in nodes_begin:

      for j in nodes_begin:

         # Если рассмотренное ребро входит в 2/3 графа-пропускаем его
         flag=False
         if j in graph.edge_map[i].keys() and min(graph.edge_map[i][j])<=t_s:
            flag=False
         else:
            flag=True
            
         if str(i)+"."+str(j) not in counted_edges and str(j)+"."+str(i) not in counted_edges and j!=i and flag:
            
            first_i=node_activity_map[i][0]
            second_i=node_activity_map[i][1]
            third_i=node_activity_map[i][2]
            first_j=node_activity_map[j][0]
            second_j=node_activity_map[j][1]
            third_j=node_activity_map[j][2]
            pre_X=[]

            for k in range(7):
               pre_X.append(first_i[k]+first_j[k])
               pre_X.append(second_i[k]+second_j[k])
               pre_X.append(third_i[k]+third_j[k])
               pre_X.append(abs(first_i[k]-first_j[k]))
               pre_X.append(abs(second_i[k]-second_j[k]))
               pre_X.append(abs(third_i[k]-third_j[k]))
               pre_X.append(min(first_i[k],first_j[k]))
               pre_X.append(min(second_i[k],second_j[k]))
               pre_X.append(min(third_i[k],third_j[k]))
               pre_X.append(max(first_i[k],first_j[k]))
               pre_X.append(max(second_i[k],second_j[k]))
               pre_X.append(max(third_i[k],third_j[k]))

            counted_edges.append(str(i)+"."+str(j))

            pre_X.append(common_neigbours(graph,i,j,t_s))
            pre_X.append(adamic_adar(graph,i,j,t_s))
            pre_X.append(jaaccard_coefficient(graph,i,j,t_s))
            pre_X.append(preferential_attachment(graph,i,j,t_s))

            X.append(pre_X)

   return X,counted_edges



def get_y(graph:UndirectedGraph, edges:list,t_s:int):

   Y=[]

   for i in range (len(edges)):
      edge=edges[i]
      index=edge.find(".")
      a=int(edge[:index])
      b=int(edge[index+1:])
      if b in graph.edge_map[a].keys():
         Y.append(1)
      else:
         Y.append(0)

   return Y



def get_y(graph:UndirectedGraph, edges:list, t_s:int):

   Y=[]

   for i in range (len(edges)):
      edge=edges[i]
      index=edge.find(".")
      a=int(edge[:index])
      b=int(edge[index+1:])
      if b in graph.edge_map[a].keys() and max(graph.edge_map[a][b])>t_s:
         Y.append(1)
      else:
         Y.append(0)

   return Y

# def get_x_big_graph(graph:UndirectedGraph,node_activity_map:dict,nodes_begin:list,t_s:int):
#    # для каждой пары вершин найдём характеристики из feature3(3) 
#    counted_edges=[]
#    X=[]
#    for k in range (len(nodes_begin)):
#       edge=nodes_begin[k]
#       index=edge.find(".")
#       i=int(edge[:index])
#       j=int(edge[index+1:])
#       # Если рассмотренное ребро входит в 2/3 графа-пропускаем его
#       flag=False
#       if j in graph.edge_map[i].keys() and min(graph.edge_map[i][j])<=t_s:
#          flag=False
#       else:
#          flag=True 
#       if j!=i and flag and j in node_activity_map.keys() and i in node_activity_map.keys():
#          first_i=node_activity_map[i][0]
#          second_i=node_activity_map[i][1]
#          third_i=node_activity_map[i][2]
#          first_j=node_activity_map[j][0]
#          second_j=node_activity_map[j][1]
#          third_j=node_activity_map[j][2]
#          pre_X=[]
#          for k in range(7):
#             pre_X.append(first_i[k]+first_j[k])
#             pre_X.append(second_i[k]+second_j[k])
#             pre_X.append(third_i[k]+third_j[k])
#             pre_X.append(abs(first_i[k]-first_j[k]))
#             pre_X.append(abs(second_i[k]-second_j[k]))
#             pre_X.append(abs(third_i[k]-third_j[k]))
#             pre_X.append(min(first_i[k],first_j[k]))
#             pre_X.append(min(second_i[k],second_j[k]))
#             pre_X.append(min(third_i[k],third_j[k]))
#             pre_X.append(max(first_i[k],first_j[k]))
#             pre_X.append(max(second_i[k],second_j[k]))
#             pre_X.append(max(third_i[k],third_j[k]))
#          counted_edges.append(str(i)+"."+str(j))
#          pre_X.append(common_neigbours(graph,i,j,t_s))
#          pre_X.append(adamic_adar(graph,i,j,t_s))
#          pre_X.append(jaaccard_coefficient(graph,i,j,t_s))
#          pre_X.append(preferential_attachment(graph,i,j,t_s))
#          X.append(pre_X)
#    return X,counted_edges
