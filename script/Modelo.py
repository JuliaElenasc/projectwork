def plot_mappe (gdf, colona): #funzione che fa il plot da un geodataframe secondo una colonna
    gdf.plot()
    gdf[colona].plot(marker='o', color='red', markersize=5, ax=plt.gca())
    plt.show()

#modelo
  # -----Modelo
    # Calcular ma media 2018-2020 para el calculo de la media 2021 (nueva columna "frequenza_20182020")
    # Calculamos la nueva columna 'frequenza_20182020'

    # Definir la credibilidad
    # crea una matriz con las columnas A,n, media_random y errore
    # en media_random calcula una media ponderada del numero de accidentes de transito
    # con la formula n_vehiculos*frecuencia_accidentes/numero de vehiculos total
    # 
