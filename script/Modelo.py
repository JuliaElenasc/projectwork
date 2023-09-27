import pandas as pd
import geopandas as gpd
import pickle
import numpy as np
import json



def smoothing_city_MSE(data_analysis, path_distance_matrix, path_result, values_A, values_n):
    # Data reading
    path_Mercato_code = pd.read_csv(data_analysis)
    data_analysis=path_Mercato_code
    with open(path_distance_matrix, 'r') as file:
        D = pd.read_json(file)
    
    # Preprocesing: For the time period of interest (2018-2021), in a new column the weighted average of frequency is calculated.

    data_analysis['frequenza_20182021'] = (data_analysis['Frequenza sinistri 2018'] * data_analysis['Veicoli Anno 2018'] +
                                      data_analysis['Frequenza sinistri 2019'] * data_analysis['Veicoli Anno 2019'] +
                                      data_analysis['Frequenza sinistri 2020'] * data_analysis['Veicoli Anno 2020'] +
                                      data_analysis['Frequenza sinistri 2021'] * data_analysis['Veicoli Anno 2021']) / \
                                     np.maximum((data_analysis['Veicoli Anno 2021'] + data_analysis['Veicoli Anno 2020'] +
                                                 data_analysis['Veicoli Anno 2019'] + data_analysis['Veicoli Anno 2018']), 0.001)

    # Preprocesing: For the time period of interest (2018-2021), create a new column: vehicoli_20182021
    data_analysis['veicoli_20182021'] = (data_analysis['Veicoli Anno 2021'] + data_analysis['Veicoli Anno 2020'] +
                                    data_analysis['Veicoli Anno 2019'] + data_analysis['Veicoli Anno 2018'])

    # To save the resulting metadata from the scenario processing, a data frame is created     
    check_media_random = pd.DataFrame(columns=['A', 'n', 'media_random', 'errore'])

    
    for A in values_A:
        
        credibility_parameter = A * data_analysis['veicoli_20182021'].mean()
        
        Z1 = data_analysis['veicoli_20182021'] / (credibility_parameter + data_analysis['veicoli_20182021'])
                
        Observed_residual_code = data_analysis['frequenza_20182021']
            
        Z2 = 1 - Z1
            
        D_n = 1/np.power(D,values_n)
            
        D_n_sorted = D_n.sort_index()
                        
        for i in range(data_analysis.shape[0]):
            D_n_sorted.iat[i, i] = 0
                   
        V = data_analysis['frequenza_20182021'] * data_analysis['veicoli_20182021']
        V2 = data_analysis['veicoli_20182021']

        numeratore = D_n_sorted.dot(V) 
           
        denominatore = D_n_sorted.dot(V2)
           
        #per chi non confina con niente con esposizione
        denominatore[denominatore == 0] = 1
        media_pesata_freq = numeratore / denominatore
                       
        # crea la columna Smoothed_frequenza_cod en el dataframe data_analysis
        data_analysis[f"smoothed_freq_A{A}_n{value_n}"] = (Z1 * Observed_residual_code) + (Z2 * media_pesata_freq)
        # Se crea la columna errore comune y se calcula el Error medio cuadratico para cada valor en data analisi usando como base los datos de 2021 --> porqué?
        data_analysis['errore_comune'] = ((data_analysis[f"smoothed_freq_A{A}_n{value_n}"] - data_analysis['Frequenza sinistri 2021']) ** 2) * data_analysis['Veicoli Anno 2021']
        # Une el data frame con un shapefile
        gdf = gpd.read_file(path_shapefile)
        union_column = 'PRO_COM_T'
        gdf[union_column] = gdf[union_column].astype(str)
        data_analysis[union_column] = data_analysis[union_column].astype(str)
        merged_gdf = gdf.merge(data_analysis, left_on=union_column, right_on=union_column, how='inner')
            
        # Guardar el resultado en un nuevo archivo Shapefile o GeoJSON
        result_geojson = path_result
        merged_gdf.to_file(result_geojson, driver='GeoJSON')
        # agrega los valores calculados a un diccionario para agregarlo a la matriz vacia creada inicialmente
        row = {
            'A': A,
            'n': value_n,
            'media_random': sum(data_analysis['Veicoli Anno 2021'] * data_analysis[f"smoothed_freq_A{A}_n{value_n}"]) /data_analysis['Veicoli Anno 2021'].sum(),
            'errore': np.sqrt(data_analysis['errore_comune'].sum() / data_analysis['Veicoli Anno 2021'].sum())
            }
        check_media_random = check_media_random.append(row, ignore_index=True)
            
        data_analysis_scenario = data_analysis.copy()
            
    results_df = pd.concat([check_media_random], axis=0, ignore_index=True)
    return results_df, data_analysis_scenario
#-------------------------------------------------------------------------------------------------
#Files
#pickl = r"C:\Users\JuliaElenaSilloCondo\OneDrive - ITS Angelo Rizzoli\Documenti\projectwork\dati\distance_matrix.pkl"
pickl= r'C:\Users\JuliaElenaSilloCondo\Downloads\D.json'
path_Mercato_code = r"C:\Users\JuliaElenaSilloCondo\OneDrive - ITS Angelo Rizzoli\Documenti\projectwork\output\Mercato_code.csv"
path_shapefile=r'C:\Users\JuliaElenaSilloCondo\OneDrive - ITS Angelo Rizzoli\Documenti\projectwork\dati\Limiti01012023\Limiti01012023\Com01012023\Com01012023_WGS84.shp'
path_result= r'C:\Users\JuliaElenaSilloCondo\OneDrive - ITS Angelo Rizzoli\Documenti\projectwork\output\resultado.geojson'

    # Modelo
value_A = [0.03]
value_n = 20
   
smoothing  = smoothing_city_MSE(path_Mercato_code, pickl,path_result, value_A, value_n)
