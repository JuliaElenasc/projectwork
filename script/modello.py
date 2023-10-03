import pandas as pd
import geopandas as gpd
import numpy as np
import calculates_parameters as c_par


def smoothing_city_MSE(path_csv: str, path_distance_matrix: str, path_shapefile: str, path_result: str,
                       value_A: float = 0.03, value_n: int = 20, ceck_best: bool = False):
    dtype_dict = {'PRO_COM': float, 'PRO_COM_T': object}
    data = pd.read_csv(path_csv, dtype=dtype_dict)
    distance_matrix = pd.read_csv(path_distance_matrix, dtype=float, header=0, index_col=0)
    
    # Chiama alla funzione di calcolo dal miglior escenario
    if ceck_best:
        value_A, value_n = c_par.calculate(path_csv, path_distance_matrix)
    
    # Per il periodo di interesse (2018-2021), in una nuova colonna viene calcolata la media ponderata della frequenza
    data['frequenza_20182021'] = (data['Frequenza sinistri 2018'] * data['Veicoli Anno 2018'] +
                                  data['Frequenza sinistri 2019'] * data['Veicoli Anno 2019'] +
                                  data['Frequenza sinistri 2020'] * data['Veicoli Anno 2020'] +
                                  data['Frequenza sinistri 2021'] * data['Veicoli Anno 2021']) / np.maximum(
        (data['Veicoli Anno 2021'] + data['Veicoli Anno 2020'] +
         data['Veicoli Anno 2019'] + data['Veicoli Anno 2018']), 0.001)
    
    # Creazione della colonna: veicoli_20182021
    data['veicoli_20182021'] = (data['Veicoli Anno 2021'] + data['Veicoli Anno 2020'] +
                                data['Veicoli Anno 2019'] + data['Veicoli Anno 2018'])

    # Calcolo del credibility parameter
    credibility_parameter = value_A * data['veicoli_20182021'].mean()
    
    # Calcolo dal Zi e il suo complemento
    Z1 = data['veicoli_20182021'] / (credibility_parameter + data['veicoli_20182021'])
    Z2 = 1 - Z1
    
    # Calcolo della media ponderata delle frequenze 
    d_n = 1 / np.power(distance_matrix, value_n)
    d_n = d_n.fillna(0)
    for i in range(d_n.shape[0]):
        d_n.iloc[i, i] = 0

    V = data['frequenza_20182021'] * data['veicoli_20182021']
    V2 = data['veicoli_20182021']
    
    data['numeratore'] = np.dot(d_n, V)
    data['denominatore'] = np.dot(d_n, V2)
    
    # Per chi non confina con niente con esposizione
    data['denominatore'] = data['denominatore'].replace(0, 1) # To avoid division by zero
    data['media_pesata_freq'] = data['numeratore'] / data['denominatore']

    # Calcola la colonna Smoothed_freq nel dataframe data (modello)
    data[f"smoothed_freq"] = (Z1 * data['frequenza_20182021']) + (Z2 * data['media_pesata_freq'])
    
    # Viene creata la colonna errore comune che si calcola l'errore medio quadratico
    data['errore_comune'] = ((data[f"smoothed_freq"] - data['Frequenza sinistri 2021']) ** 2) * data[
        'Veicoli Anno 2021']
    # Unione del dataframe con lo shapefile
    gdf = gpd.read_file(path_shapefile)
    union_column = 'PRO_COM_T'
    merged_gdf = gdf.merge(data, left_on=union_column, right_on=union_column, how='inner')
    # salvataggio del file in formato .geojson
    merged_gdf.to_file(path_result, driver='GeoJSON')
    print('File geojson risultante salvato')


