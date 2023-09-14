import geopandas as gpd
import libpysal
import networkx as nx
import pandas as pd
from matplotlib import pyplot as plt

if __name__ == '__main__':
    city_to_remove = ['Campione d\'Italia', 'Capraia Isola', 'Isola del Giglio', 'Ponza', 'Ventotene', 'Procida',
                      'Isole Tremiti', 'Favignana', 'Pantelleria', 'Ustica', 'Lipari', 'Lampedusa e Linosa',
                      'La Maddalena', 'Carloforte']
    path_city_shape = '../../dati/Com01012023_WGS84.shp'
    city_shape = gpd.read_file(path_city_shape)
    city_shape = city_shape[~city_shape['COMUNE'].isin(city_to_remove)]
    city_shape['centroid'] = city_shape['geometry'].centroid
    city_nb = libpysal.weights.Queen.from_dataframe(city_shape)
    distances = city_shape['centroid'].apply(lambda x: city_shape['centroid'].distance(x))
    Graph_distance = nx.Graph()
    for i in range(len(distances.index)):
        for j in range(i + 1, len(distances.columns)):
            distance = distances.iloc[i, j]
            Graph_distance.add_edge(distances.index[i], distances.columns[j], weight=distance)
    Graph_df = pd.DataFrame(nx.to_pandas_edgelist(Graph_distance), columns=['source', 'target', 'weight'])
    Graph_df.to_pickle('../dati/distances.pkl')
    fig, ax = plt.subplots(figsize=(12, 12))
    city_shape.plot(ax=ax, alpha=0.7)

    pos = {node: (city_shape['centroid'].loc[node].x, city_shape['centroid'].loc[node].y) for node in
           Graph_distance.nodes()}
    labels = {node: node for node in Graph_distance.nodes()}
    weights = [Graph_distance[edge[0]][edge[1]]['weight'] for edge in Graph_distance.edges()]

    nx.draw(Graph_distance, pos, labels=labels, width=weights, edge_color='b', ax=ax)

    plt.axis('off')
    plt.title("Grafo delle Distanze tra Comuni")
    plt.show()