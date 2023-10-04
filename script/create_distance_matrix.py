import geopandas as gpd
import networkx as nx
import numpy as np
import pandas as pd


def distance_matrix(path_read_shp_file: str, path_save_distance_matrix: str):
    city_to_remove = ['Campione d\'Italia', 'Capraia Isola', 'Isola del Giglio', 'Ponza', 'Ventotene', 'Procida',
                      'Isole Tremiti', 'Favignana', 'Pantelleria', 'Ustica', 'Lipari', 'Lampedusa e Linosa',
                      'La Maddalena', 'Carloforte']
    # leggo il file
    city_shape = gpd.read_file(path_read_shp_file)
    # tolgo le isole e le citta che non ci interessano
    city_shape = city_shape[~city_shape['COMUNE'].isin(city_to_remove)].reset_index(drop=True)
    # mi estrapolo la lista delle citta
    city_list = pd.DataFrame(columns=['COMUNE', 'PRO_COM_T'])
    for i in range(city_shape.shape[0]):
        city_list.loc[i, 'COMUNE'] = city_shape.iloc[i]['COMUNE']
        city_list.loc[i, 'PRO_COM_T'] = city_shape.iloc[i]['PRO_COM_T']
    # CALCOLO DEI VICINI
    city_shape['NB'] = None
    # mi estrapolo i vicini utilizzando la funzione .touches
    for i in range(city_shape.shape[0]):
        nb = list(np.argwhere(city_shape['geometry'].touches(city_shape['geometry'][i]).to_numpy() == True).flatten())
        city_shape.at[i, 'NB'] = nb
    # MATRICE DI DISTANZE
    # creo un grafo
    g = nx.Graph()
    # aggiungo i noi al grafo
    g.add_nodes_from(range(city_shape.shape[0]))
    # aggiungo gli archi connettendo i vicini
    for i in range(city_shape.shape[0]):
        nb = list(city_shape.iloc[i]['NB'])
        for arc in nb:
            g.add_edge(i, arc)
        # calcolo i percorsi minimi tra punto e punto
    distances = nx.all_pairs_shortest_path_length(g)
    distances = pd.DataFrame(dict(distances))
    distances = distances.sort_index()
    distances.to_csv(path_save_distance_matrix)
