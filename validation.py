import networkx as nx
import random
import numpy as np
import time
from statistics import mean
import pandas as pd
import random
import matplotlib.pyplot as plt
from prettytable import PrettyTable
import time

import graph_algos
import network

def print_frame(nodes, custom_dict, nx_dict, title):
    nx_filter = [nx_dict[i] for i in nodes if i in nx_dict]
    custom_filter = [custom_dict[i] for i in nodes if i in custom_dict]
    
    myTable = PrettyTable()
    myTable.title = title

    # Add Columns
    myTable.add_column("Node", nodes)
    myTable.add_column('Custom', custom_filter)
    myTable.add_column('NetworkX', nx_filter)

    print(myTable)

def main():    
    
    property_list = []
    my_time_list = []
    nx_time_list = []
    
    n = 100
    nodes = random.sample(range(0, n-1),10) #[0,1,2,3,4,5,6,7,8,9]
    G = nx.erdos_renyi_graph(n, 0.3)
    
    print('============== closness centrality ==========')
    time0 = time.process_time()
    r = network.closeness_centrality(G)
    time1 = time.process_time()
    nx_r = nx.algorithms.closeness_centrality(G)
    time2 = time.process_time()
    print_frame(nodes, r, nx_r, 'Closness Centrality')
    property_list.append('Closness Centrality')
    my_time_list.append(time1-time0)
    nx_time_list.append(time2-time1)
    
    #myTable.clear_rows()
    
    

    print('============== clustering coefficient ==========')
    time0 = time.process_time()
    r = network.network_clustering(G)
    time1 = time.process_time()
    nx_r = nx.algorithms.clustering(G)
    time2 = time.process_time()
    print_frame(nodes, r, nx_r, 'Clustering Coefficient')
    property_list.append('Clustering Coefficient')
    my_time_list.append(time1-time0)
    nx_time_list.append(time2-time1)

    
    print('============== avg clustering coefficient ==========\n')
    myTable = PrettyTable()
    myTable.title = 'Average Clustering Coefficient'

    # Add Columns
    time0 = time.process_time()
    myTable.add_column('Custom', [network.average_clustering(G)])
    time1 = time.process_time()    
    myTable.add_column('NetworkX', [nx.algorithms.average_clustering(G)])
    time2 = time.process_time()
    
    print(myTable)
    print()
    property_list.append('Average Clustering Coefficient')
    my_time_list.append(time1-time0)
    nx_time_list.append(time2-time1)



    print('============== diameter ==========\n')
    myTable.clear()
    myTable.title = 'Diameter'
    # Add Columns
    time0 = time.process_time()
    myTable.add_column('Custom', [network.network_diameter(G)])
    time1 = time.process_time()
    myTable.add_column('NetworkX', [nx.algorithms.diameter(G)])
    time2 = time.process_time()
    print(myTable)
    print()

    property_list.append('Diameter')
    my_time_list.append(time1-time0)
    nx_time_list.append(time2-time1)


    print('============== k-core ==========\n')
    time0 = time.process_time()
    _, core = graph_algos.matula_beck_degen_order(G)
    time1 = time.process_time()
    #print('our result: {}'.format(core))
    nx_core_dict = nx.core_number(G)
    nx_core = 0
    for _, v in nx_core_dict.items():
        if v > nx_core:
            nx_core = v
    time2 = time.process_time()
    print('networkx result: {}'.format(nx_core))
    print()
    
    myTable.clear()
    myTable.title = 'k-core'
    # Add Columns
    myTable.add_column('Custom', [core])
    myTable.add_column('NetworkX', [nx_core])
    print(myTable)
    print()

    property_list.append('k-core')
    my_time_list.append(time1-time0)
    nx_time_list.append(time2-time1)


    print('============== avg shortest path wrt node ==========')
      
    my_dist = []
    nx_dist = []
    t_my = []
    t_nx = []
    
    
    for node in nodes:
        print('\ncomputing avg shortest path for node {}...'.format(node))
        time0 = time.process_time()
        my_sp = graph_algos.avg_shortest_path_node(G, node)
        elapsed_time = time.process_time() - time0
        t_my.append(elapsed_time)
        print('our result: {}'.format(my_sp))
        my_dist.append(my_sp)
        
        time0 = time.process_time()
        nx_dict = nx.shortest_path(G, node)
        nx_lengths = []
        for _, v in nx_dict.items():
            nx_lengths.append(len(v)-1)
        elapsed_time = time.process_time() - time0
        t_nx.append(elapsed_time)
        print('networkx result: {}'.format(mean(nx_lengths)))
        nx_dist.append(mean(nx_lengths))
    
    myTable.clear()
    myTable.title = 'avg shortest path wrt node'
    # Add Columns
    myTable.add_column('Node', nodes)
    myTable.add_column('Custom', my_dist)
    myTable.add_column('NetworkX', nx_dist)
    print(myTable)
    print()

    property_list.append('avg shortest path wrt node')
    my_time_list.append((sum(t_my)/len(t_my)))
    nx_time_list.append((sum(t_nx)/len(t_nx)))
       

    print('============== pagerank ==========')   
    DiG = G.to_directed()
    time0 = time.process_time()
    r = graph_algos.my_pagerank(DiG, 15)
    time1 = time.process_time()
    nx_r = nx.pagerank(DiG) 
    time2 = time.process_time()
    my_pagerank = []
    nx_pagerank = []
    for node in nodes:
        print('\ncomputing pagerank for node {}...'.format(node))
        print('our result: {}'.format(r[node]))
        print('networkx result: {}'.format(nx_r[node]))
        my_pagerank.append(r[node])
        nx_pagerank.append(nx_r[node])

    myTable.clear()
    myTable.title = 'Pagerank'
    # Add Columns
    myTable.add_column('Node', nodes)
    myTable.add_column('Custom', my_pagerank)
    myTable.add_column('NetworkX', nx_pagerank)
    print(myTable)
    print()

    property_list.append('pagerank')
    my_time_list.append(time1-time0)
    nx_time_list.append(time2-time1)
    
    myTable.clear()
    myTable.title = 'Execution Runtime'
    # Add Columns
    myTable.add_column('Property', property_list)
    myTable.add_column('Custom', my_time_list)
    myTable.add_column('NetworkX', nx_time_list)
    improvement = [(b-a)/b for a, b in zip(my_time_list, nx_time_list)]
    myTable.add_column('Improvement %', improvement)
    print(myTable)
    print()


if __name__ == '__main__':
    main()