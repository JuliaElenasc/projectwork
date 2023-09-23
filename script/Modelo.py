import pandas as pd
import numpy as np

def smoothing_city_MSE(data_analisi, valori_A, valori_n):
    check_media_random = pd.DataFrame(columns=['A', 'n', 'media_random', 'errore'])#,index=range(1,27)) #crea tabela dei risultati da longitudine 26
    for A in valori_A:
        for n in valori_n:
            credibility_parameter = A * data_analisi['veicoli_20182020'].mean()
            Z1 = data_analisi['veicoli_20182020'] / (credibility_parameter + data_analisi['veicoli_20182020'])
                
            Observed_residual_code = data_analisi['frequenza_20182020']
            
            Z2 = 1 - Z1

            D_n = np.identity(len(data_analisi))
            np.fill_diagonal(D_n, 0)

            V = data_analisi['frequenza_20182020'] * data_analisi['veicoli_20182020']
            V2 = data_analisi['veicoli_20182020']

            numeratore = np.dot(D_n, V) 
            denominatore = np.dot(D_n, V2)
            #per chi non confina con niente con esposizione...--> no entiendo
            denominatore[denominatore == 0] = 1
            media_pesata_freq = numeratore / denominatore
                       
            # crea la columna Smoothed_frequenza_cod en el dataframe data_analisi
            data_analisi[f"smoothed_freq_A{A}_n{n}"] = (Z1 * Observed_residual_code) + (Z2 * media_pesata_freq)
            # Se crea la columna errore comune y se calcula el Error medio cuadratico para cada valor en data analisi usando como base los datos de 2021 --> porqué?
            data_analisi['errore_comune'] = ((data_analisi[f"smoothed_freq_A{A}_n{n}"] - data_analisi['Frequenza sinistri 2021']) ** 2) * data_analisi['Veicoli Anno 2021']
            
            # agrega los valores calculados a un diccionario para agregarlo a la matriz vacia creada inicialmente
            row = {
                'A': A,
                'n': n,
                'media_random': data_analisi['Veicoli Anno 2021'].sum() * data_analisi[f"smoothed_freq_A{A}_n{n}"].sum() / data_analisi['Veicoli Anno 2021'].sum(),
                'errore': np.sqrt(data_analisi['errore_comune'].sum() / data_analisi['Veicoli Anno 2021'].sum())
            }
            check_media_random = check_media_random.append(row, ignore_index=True)
            
            data_analisi_scenario = data_analisi.copy()
            
            #print(data_analisi_scenario.columns)
            print(f"calcolando escenario smoothed_freq_A{A}_n{n}")
            print('The best ')
    results_df = pd.concat([check_media_random], axis=0, ignore_index=True)
    return results_df, data_analisi_scenario

#--------------------------------------------------------------------------
# Inputs
data_analisi = pd.read_csv('Mercato_code.csv')
D = np.random.uniform(0.0, 20, size=(7887, 7887))

# Scenarios
valori_A = [0.01, 0.02, 0.03, 0.04, 0.05]
valori_n = [18, 19, 20, 21, 22]

# 2018-2020 calculation (frequency and vehicles)
data_analisi['frequenza_20182020'] = (
    (data_analisi['Frequenza sinistri 2018'] * data_analisi['Veicoli Anno 2018'] +
     data_analisi['Frequenza sinistri 2019'] * data_analisi['Veicoli Anno 2019'] +
     data_analisi['Frequenza sinistri 2020'] * data_analisi['Veicoli Anno 2020']) /
    np.maximum((data_analisi['Veicoli Anno 2020'] + data_analisi['Veicoli Anno 2019'] + data_analisi['Veicoli Anno 2018']), 0.001)
    )
data_analisi['veicoli_20182020'] = data_analisi['Veicoli Anno 2018'] + data_analisi['Veicoli Anno 2019'] + data_analisi['Veicoli Anno 2020']

risultato1, risultato2  = smoothing_city_MSE(data_analisi, valori_A, valori_n)
#risultato_df = pd.DataFrame(risultato)

print('hasta aqui!!!')



# A dataframe is created that saves the results of the scenarios with a control scenario
#check_media_random=results_df=df_check_media



#----------------------------------------------------------------------------------

# Guardar el DataFrame en un archivo CSV
    # en media_random calcula una media ponderada del numero de accidentes de transito
    # con la formula n_vehiculos*frecuencia_accidentes/numero de vehiculos total
    # 
