import pandas as pd
import geopandas as gpd
import pickle
import numpy as np
import json



def smoothing_city_MSE(path_mercato_code, path_distance_matrix, path_shapefile, path_result, values_A, values_n):
    # Data reading
    print("Data reading...")
    dtype_dict = {'PRO_COM': float, 'PRO_COM_T': object}
    path_mercato_code = pd.read_csv(path_mercato_code,dtype=dtype_dict)
    
    data_analysis=path_mercato_code
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

    
    # 1. Zi
    print("Calculating Zi...") 
    # The credibility value is adjusted based on a constant A
    credibility_parameter = values_A * data_analysis['veicoli_20182021'].mean()
        
    # Calculation of Zi (Proportion of vehicles in relation to the credibility parameter and the number of vehicles).
    Zi = data_analysis['veicoli_20182021'] / (credibility_parameter + data_analysis['veicoli_20182021'])
    
    # 2. Detected accident frequency
    print("Calculating Detected accident frequency...")
    Observed_residual_code = data_analysis['frequenza_20182021'] 

    # 3. Complementary proportion of Zi
    print("Calculating 1-Zi...")   
    Z2 = 1 - Zi 
            
    # 4. Calculation of the weighted average of frequencies
    print("Calculating weighted average of frequencies...")
    D_n = 1/np.power(D,values_n) # Normalization: For each element in the distance matrix, apply the formula 1/D^n
            
    D_n_sorted = D_n.sort_index() 
                        
    for i in range(data_analysis.shape[0]): # Based on the number of rows in data_analysis, the same number of rows from D_n is taken, and the diagonal values are assigned 0
            D_n_sorted.iat[i, i] = 0
        
    V = data_analysis['frequenza_20182021'] * data_analysis['veicoli_20182021'] # r*e (In the formula)
    V2 = data_analysis['veicoli_20182021'] # e (In the formula)

    numerator = D_n_sorted.dot(V) 
    
    denominator = D_n_sorted.dot(V2)
           
    # For those who do not border anything
    denominator[denominator == 0] = 1 # To avoid division by zero
    
    weighted_average = numerator / denominator

    # 5. Estimated frequency i --> smoothed 
    print("Calculanting Estimated frequency i (smoothed)")               
    # Creates the 'Smoothed_frequenza_cod' column in the 'data_analysis' dataframe.
    data_analysis[f"smoothed_freq_A{values_A}_n{values_n}"] = (Zi * Observed_residual_code) + (Z2 * weighted_average)
    
    # The 'errore_comune' column is created, and the Mean Squared Error is calculated for each value in 'data analisi' using 2021 data as the reference
    data_analysis['errore_comune'] = ((data_analysis[f"smoothed_freq_A{values_A}_n{values_n}"] - data_analysis['Frequenza sinistri 2021']) ** 2) * data_analysis['Veicoli Anno 2021']
    
    gdf = gpd.read_file(path_shapefile) # Merges the data frame with a shapefile
    
    union_column = 'PRO_COM_T' # Common column for the union
    
    merged_gdf = gdf.merge(data_analysis, left_on=union_column, right_on=union_column, how='inner')
            
    # Save the result in the GeoJSON
    print("Saving geojson...")
    name_geojson= "\data_result.geojson"
    result_geojson = path_result+name_geojson
    merged_gdf.to_file(result_geojson, driver='GeoJSON')
    
    # Add the calculated values resulting from the scenario to a dictionary to append it to the initially created empty matrix
    row = {
            'A': values_A,
            'n': values_n,
            'media_random': sum(data_analysis['Veicoli Anno 2021'] * data_analysis[f"smoothed_freq_A{values_A}_n{values_n}"]) /data_analysis['Veicoli Anno 2021'].sum(),
            'errore': np.sqrt(data_analysis['errore_comune'].sum() / data_analysis['Veicoli Anno 2021'].sum())
            }
    row_df = pd.DataFrame([row])

    check_media_random = pd.concat([check_media_random, row_df], ignore_index=True)

    print((f'File saved in {result_geojson}'))
    return 


