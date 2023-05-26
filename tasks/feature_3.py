from graphs_init.undirected_graph import UndirectedGraph
from typing import Set, Tuple, List
import math
from random import sample
import numpy as np

def get_node_activities(graph:UndirectedGraph,t_s:int):
   l=0.2
   t_min=math.inf
   t_max=-1
   weight_map={}
   # найдём максимальное и минимальное значение
   for i in graph.edge_map.keys():
      for j in graph.edge_map[i].keys():
         t_max=max(t_max,max(graph.edge_map[i][j]))
         t_min=min(t_min,min(graph.edge_map[i][j]))
   # вычислим map весов (лин., эксп.,корн.)
   weight_map={}
      
   for i in graph.edge_map.keys():
      if i not in weight_map.keys():
         weight_map[i]={}
      for j in graph.edge_map[i].keys():
         for k in range(len(graph.edge_map[i][j])):
            t=graph.edge_map[i][j][k]
            if t<t_s:
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
   return node_activity_map

def get_x_y(graph:UndirectedGraph,node_activity_map:dict,nodes_begin:list):
   # для каждой пары вершин найдём характеристики из feature3(3)
   nodes_begin=[key for key in graph.edge_map.keys()]
   counted_edges=[]
   X=[]
   Y=[]
   node_activity_adjacent_nodes={}
   for i in nodes_begin:
      if i not in node_activity_adjacent_nodes.keys():
         node_activity_adjacent_nodes[i]={}
      for j in nodes_begin:
         first_out=[[],[],[]] # массив для хранения суммы для каждого из весов
         second_out=[[],[],[]] # массив для хранения модуля разности для каждого из весов
         third_out=[[],[],[]] # массив для хранения минимума для каждого из весов
         fourth_out=[[],[],[]] # массив для хранения максимума для каждого из весов
         if i+j not in counted_edges and j+i not in counted_edges and j!=i:
            first_i=node_activity_map[i][0]
            second_i=node_activity_map[i][1]
            third_i=node_activity_map[i][2]
            first_j=node_activity_map[j][0]
            second_j=node_activity_map[j][1]
            third_j=node_activity_map[j][2]
            for k in range(7):
               first_out[0].append(first_i[k]+first_j[k])
               first_out[1].append(second_i[k]+second_j[k])
               first_out[2].append(third_i[k]+third_j[k])
               second_out[0].append(abs(first_i[k]-first_j[k]))
               second_out[1].append(abs(second_i[k]-second_j[k]))
               second_out[2].append(abs(third_i[k]-third_j[k]))
               third_out[0].append(min(first_i[k],first_j[k]))
               third_out[1].append(min(second_i[k],second_j[k]))
               third_out[2].append(min(third_i[k],third_j[k]))
               fourth_out[0].append(max(first_i[k],first_j[k]))
               fourth_out[1].append(max(second_i[k],second_j[k]))
               fourth_out[2].append(max(third_i[k],third_j[k]))
            counted_edges.append(i+j)
            X.append([first_out,second_out,third_out,fourth_out])
            if j in graph.edge_map[i].keys():
               Y.append(1)
            else:
               Y.append(0)
            counted_edges.append(i+j)
   return X,Y
