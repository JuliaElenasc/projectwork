#Aprire file proporzionati
import geopandas as gpd
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
def add_comune(df, col):
    group = df.groupby(col).mean()
    return group


if __name__=='__main__':

    comune= '.\\dati\Limiti01012023\Limiti01012023\Com01012023\Com01012023_WGS84.shp'
    
    #----------- 1. OPEN DATA---------------
    # Open the shapefile
    gdf = gpd.read_file(comune)
    # Info GeoDataFrame
    print(gdf.head()) 
    #print(gdf.crs)     # (CRS)
    #print(gdf.geometry)  # geometries 
    # Calcular el centroide de cada polígono y agregarlo como una nueva columna
    gdf['centroid'] = gdf['geometry'].centroid
    # Mostrar los primeros 10 registros del GeoDataFrame con los centroides
    print(gdf.head(10))
    #gdf.plot()
    #gdf['centroid'].plot(marker='o', color='red', markersize=5, ax=plt.gca())
    #plt.show()

    # Open csv 
    dati = pd.read_csv('.\\dati\DatidiMercato.csv')
    
    # Agregare i dati 
    data_group = add_comune(dati, 'Comune_residenza')
    data_group.rename(columns={'Comune_residenza': 'COMUNE'},inplace= True)
    print(data_group.dtypes)
    print(data_group)
    
    #---------- 2. Unire le tabelle------------------------------
    # Fare l'unione tra CSV e Shapefile
    #total_data= pd.merge(gdf, data_group, on='COMUNE')





    
    # Matriz de adyacencia --> PENDIENTE
    
    # Delete data iland --> PENDIENTE
    #comune_poly= ["Campione d'Italia", "Capraia Isola", "Isola del Giglio", "Ponza", "Ventotene", "Procida", "Isole Tremiti", "Favignana", "Pantelleria", "Ustica", "Lipari", "Lampedusa e Linosa", "La Maddalena", "Carloforte"]

    # Open dati csv
    dataframe = pd.read_csv(dati)
    







    # Realiza operaciones o visualizaciones con los datos geoespaciales, por ejemplo:
    gdf.plot()  # Crea una visualización simple del GeoDataFrame
