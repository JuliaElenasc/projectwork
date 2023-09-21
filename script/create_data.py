import geopandas as gpd
import networkx as nx
import numpy as np
import pandas as pd

if __name__ == '__main__':
    city_to_remove = ['Campione d\'Italia', 'Capraia Isola', 'Isola del Giglio', 'Ponza', 'Ventotene', 'Procida',
                      'Isole Tremiti', 'Favignana', 'Pantelleria', 'Ustica', 'Lipari', 'Lampedusa e Linosa',
                      'La Maddalena', 'Carloforte']
    path_city_shape = '../dati/Limiti01012023/Limiti01012023/Com01012023/Com01012023_WGS84.shp'
    # leggo il file
    city_shape = gpd.read_file(path_city_shape)
    # tolgo le isole e le citta che non ci interessano
    city_shape = city_shape[~city_shape['COMUNE'].isin(city_to_remove)].reset_index(drop=True)
    # mi estrapolo la lista delle citta
    city_list = pd.DataFrame(columns=['COMUNE', 'PRO_COM_T'])
    for i in range(city_shape.shape[0]):
        city_list.loc[i, 'COMUNE'] = city_shape.iloc[i]['COMUNE']
        city_list.loc[i, 'PRO_COM_T'] = city_shape.iloc[i]['PRO_COM_T']
    # calcolo dei vicini
    city_shape['NB'] = None
    for i in range(city_shape.shape[0]):
        nb = list(
            np.argwhere(city_shape['geometry'].touches(city_shape['geometry'][int(i)]).to_numpy() == True).flatten())
        city_shape.at[i, 'NB'] = nb
    # matrice distanze
    g = nx.Graph()
    counter = []
    g.add_nodes_from(range(city_shape.shape[0]))
    for i in range(city_shape.shape[0]):
        nb = list(city_shape.iloc[i]['NB'])
        for arc in nb:
            g.add_edge(i, arc)
    distances = nx.all_pairs_shortest_path_length(g)
    distances = pd.DataFrame(dict(distances))
    distances.to_pickle('../dati/distance_matrix.pkl')
