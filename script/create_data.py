import geopandas as gpd
import libpysal
import igraph
import networkx as nx
import numpy as np
import pandas as pd
from matplotlib import pyplot as plt

if __name__ == '__main__':
    city_to_remove = ['Campione d\'Italia', 'Capraia Isola', 'Isola del Giglio', 'Ponza', 'Ventotene', 'Procida',
                      'Isole Tremiti', 'Favignana', 'Pantelleria', 'Ustica', 'Lipari', 'Lampedusa e Linosa',
                      'La Maddalena', 'Carloforte', 'Gorgona Scalo', 'Marettimo', 'Levanzo']
    path_city_shape = '../dati/Limiti01012023/Limiti01012023/Com01012023/Com01012023_WGS84.shp'
    # leggo il file
    print('leggo il file')
    city_shape = gpd.read_file(path_city_shape)
    # tolgo le isole e le citta che non ci interessano
    print('tolgo le isole e le citta che non ci interessano')
    city_shape = city_shape[~city_shape['COMUNE'].isin(city_to_remove)]
    # mi estrapolo la lista delle citta
    print('mi estrapolo la lista delle citta')
    city_list = list(city_shape['COMUNE'])
    num_cities = len(city_list)
    # calcolo dei vicini
    print('calcolo dei vicini')
    city_weights = libpysal.weights.Queen.from_dataframe(city_shape)
    # calcolo centroidi
    print('calcolo centroidi')
    city_centroid = city_shape.centroid
    # matrice di adiacenza
    print('matrice di adiacenza')
    cities_matrix = libpysal.weights.full(city_weights)[0]
    # matrice distanze
    print('matrice distanze')
    graph_city = nx.Graph(cities_matrix)
    print('errore passato')
    distance_matrix = nx.all_pairs_shortest_path_length(graph_city)
    output = pd.DataFrame(distance_matrix)
    print('fine')
    output.to_pickle('../dati/distance_matrix.pkl')
    print('vittoria')
