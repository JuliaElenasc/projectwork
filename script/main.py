# librerie per la GUI
import tkinter as tk
from tkinter import ttk

# librerie per i grafici
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.cm import get_cmap, ScalarMappable
from matplotlib.colors import Normalize

# librerie varie
import os
import geopandas as gpd

# funzioni nostre
import clean_merge_csv as cmc
import create_distance_matrix as cdmx
import modello as mdl


def update_map():
    selected_region = int(regioni[region_var.get()])
    if selected_region == 0:
        data_filtered = data_map
    else:
        data_filtered = data_map[data_map['COD_REG'] == selected_region]

    ax.clear()
    data_filtered.plot(column='smoothed_freq', cmap=cmap, ax=ax, legend=True, cax=cax)
    plt.title('Smoothing')
    canvas.draw()


def exit_app():
    root.destroy()


if __name__ == '__main__':
    # Dichiarazione percorso file e nomi dei file
    path_data=r'../dati'
    path_read_shp_file = r'../dati/Limiti01012023/Limiti01012023/Com01012023/Com01012023_WGS84.shp'
    path_read_csv_file = r'../dati/DatidiMercato.csv'
    path_save_distance_matrix = r'../output/distance_matrix.csv'
    path_save_clean_csv = r'../output/Mercato_code.csv'
    path_geojson = r'../output/city_list.geojson'
    # creazione delle cartelle in caso mancassero
    if not os.path.exists(path_data):
        print('Cartella dei dati non trovata')
        try:
            # Se non esiste, crea la cartella
            os.makedirs(path_data)
            print(f'Cartella per i dati creata, inserire i dati in questa cartella:\n{os.path.abspath(path_data)}')
        except OSError as e:
            print('Errore nella creazione della cartella per i dati')
        quit()
    if not os.path.exists(r'../output'):
        try:
            # Se non esiste, crea la cartella
            os.makedirs(r'../output')
        except OSError as e:
            print('Errore, impossibile creare la cartella per i dati in output')
            quit()
    # lavorazione dei dati
    # pulizia del csv
    cmc.clean_data(path_read_csv_file, path_read_shp_file, path_save_clean_csv)
    # creazione della matrice delle distanze
    cdmx.distance_matrix(path_read_shp_file, path_save_distance_matrix)

    # Calcolo dello smoothing
    mdl.smoothing_city_MSE(path_save_clean_csv, path_save_distance_matrix, path_read_shp_file, path_geojson, ceck_best=True)

    # Grafici
    # lettura dei dati prodotti dal modello
    data = gpd.read_file(path_geojson)
    selected_columns = ['PRO_COM_T', 'COD_REG', 'smoothed_freq', 'COMUNE', 'geometry']
    data_map = data[selected_columns]
    data_map['COD_REG'] = data_map['COD_REG'].astype(int)
    regioni = {'Italia': 0, 'Piemonte': 1, 'Valle d\'Aosta': 2, 'Lombardia': 3, 'Trentino-Alto Adige': 4, 'Veneto': 5,
               'Friuli-Venezia Giulia': 6, 'Liguria': 7, 'Emilia-Romagna': 8, 'Toscana': 9, 'Umbria': 10, 'Marche': 11,
               'Lazio': 12, 'Abruzzo': 13, 'Molise': 14, 'Campania': 15, 'Puglia': 16, 'Basilicata': 17, 'Calabria': 18,
               'Sicilia': 19, 'Sardegna': 20}
    norm = Normalize(vmin=data_map['smoothed_freq'].min(),
                     vmax=data_map['smoothed_freq'].max())
    cmap = get_cmap('turbo')
    sm = ScalarMappable(cmap=cmap, norm=norm)
    # creazione della GUI
    root = tk.Tk()
    root.title("Frequenza sinistri smoothed")
    region_label = ttk.Label(root, text="Seleziona regioni:", )
    region_label.pack()
    region_var = tk.StringVar()
    region_combo = ttk.Combobox(root, textvariable=region_var, values=list(regioni.keys()))
    region_combo.pack()
    update_button = ttk.Button(root, text="Aggiorna Mappa", command=update_map)
    update_button.pack()
    exit_button = ttk.Button(root, text="Esci", command=exit_app)
    exit_button.pack()
    # creazione del grafico
    fig, ax = plt.subplots(1, 1, figsize=(10, 8))
    cax = fig.add_axes([0.89, 0.1, 0.03, 0.8])
    data_map.plot(column='smoothed_freq', cmap=cmap, ax=ax, legend=True, cax=cax)
    fig.colorbar(sm, cax=cax, label='Frequenza sinistri %')
    plt.title('Smoothing')
    canvas = FigureCanvasTkAgg(fig, master=root)
    canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
    root.mainloop()
