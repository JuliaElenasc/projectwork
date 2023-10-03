import pandas as pd
import numpy as np
from itertools import product


def calculate(path_mercato_code, path_distance_matrix):
    A = [0.01, 0.02, 0.03, 0.04, 0.05]
    n = [18, 19, 20, 21, 22]
    dtype_dict = {'PRO_COM': float, 'PRO_COM_T': object}
    data = pd.read_csv(path_mercato_code, dtype=dtype_dict)
    distance_matrix = pd.read_csv(path_distance_matrix, dtype=float, header=0, index_col=0)

    # Per il periodo di interesse (2018-2020), in una nuova colonna viene calcolata la media ponderata della frequenza

    data['frequenza_20182020'] = (data['Frequenza sinistri 2018'] * data['Veicoli Anno 2018'] +
                                  data['Frequenza sinistri 2019'] * data['Veicoli Anno 2019'] +
                                  data['Frequenza sinistri 2020'] * data['Veicoli Anno 2020']) / \
                                 np.maximum((data['Veicoli Anno 2020'] + data['Veicoli Anno 2019'] + data[
                                     'Veicoli Anno 2018']), 0.001)

    # Per il periodo di interesse (2018-2020), crea una nuova colonna: vehicoli_20182020
    data['veicoli_20182020'] = (data['Veicoli Anno 2020'] + data['Veicoli Anno 2019'] + data['Veicoli Anno 2018'])
    check_media_random = pd.DataFrame(columns=['A', 'n', 'media_random', 'errore'])
    combinations = list(product(A, n))
    for A, n in combinations:
        # 1. Zi
        # Il valore di credibilità viene regolato in base a una costante A
        credibility_parameter = A * data['veicoli_20182020'].mean()

        # Calcolo di Zi (Proporzione di veicoli in relazione al parametro di credibilità e al numero di veicoli)
        Zi = data['veicoli_20182020'] / (credibility_parameter + data['veicoli_20182020'])
        
        # 2. Il valore di la frequenza rilevata dei sinistri è la colonna ['frequenza_20182020']
        # 3. Calcolo complementario di Zi
        Z2 = 1 - Zi
        # 4. Calcolo della media ponderata delle frequenze
        d_n = 1 / np.power(distance_matrix, n)
        d_n = d_n.fillna(0)
        for i in range(d_n.shape[0]):
            d_n.iloc[i, i] = 0
        V = data['frequenza_20182020'] * data['veicoli_20182020']  # r*e (in formula)
        V2 = data['veicoli_20182020']  # e ( in formula)
        
        data['numeratore'] = np.dot(d_n, V)
        data['denominatore'] = np.dot(d_n, V2)
        # Per chi non confina con niente con esposizione
        data['denominatore'] = data['denominatore'].replace(0, 1)
        data['media_pesata_freq'] = data['numeratore'] / data['denominatore']
        # Crea la colonna 'Smoothed_frequenza_cod' nel dataframe 'data'
        data[f"smoothed_freq"] = (Zi * data['frequenza_20182020']) + (Z2 * data['media_pesata_freq'])
        # Viene creata la colonna 'errore_comune', e l'errore quadratico medio viene calcolato utilizzando i dati del 2021 come riferimento
        data['errore_comune'] = ((data[f"smoothed_freq"] - data['Frequenza sinistri 2021']) ** 2) * data[
            'Veicoli Anno 2021']
        # Aggiungi i valori calcolati dallo scenario a un dizionario per aggiungerli alla matrice vuota inizialmente creata
        row = {
            'A': A,
            'n': n,
            'media_random': sum(data['Veicoli Anno 2021'] * data[f"smoothed_freq"]) /
                            data['Veicoli Anno 2021'].sum(),
            'errore': np.sqrt(data['errore_comune'].sum() / data['Veicoli Anno 2021'].sum())
        }
        check_media_random.loc[len(check_media_random)] = row
    
    # Miglior scenario
    index_min_errore = check_media_random['errore'].idxmin()
    loc = check_media_random.loc[index_min_errore]
    best = {
        'A': loc['A'],
        'n': loc['n'],
        'media_random': loc['media_random'],
        'errore': loc['errore']
    }
    print('Miglior scenario')
    for columna, valor in best.items():
        print(f"{columna}: {valor}")
    return (best['A'], best['n'])