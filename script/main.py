#Aprire file proporzionati
import geopandas as gpd
import pandas as pd
import matplotlib.pyplot as plt
def add_comune(df, col):
    group = df.groupby(col).mean().reset_index()
    return group

def plot_centroid (gdf):
    gdf.plot()
    gdf['centroid'].plot(marker='o', color='red', markersize=5, ax=plt.gca())
    plt.show()

if __name__=='__main__':
    #Files
    comune= '.\\dati\Limiti01012023\Limiti01012023\Com01012023\Com01012023_WGS84.shp'
    dati = pd.read_csv('.\\dati\DatidiMercato.csv')
    
    # Delete data -->PENDIENTE
    comune_del= ["Campione d'Italia", "Capraia Isola", "Isola del Giglio", "Ponza", "Ventotene", "Procida", "Isole Tremiti", "Favignana", "Pantelleria", "Ustica", "Lipari", "Lampedusa e Linosa", "La Maddalena", "Carloforte"]
    
    #----------- 1. OPEN DATA---------------
    # Open the shapefile
    gdf = gpd.read_file(comune)
    print(gdf.shape) # vedere le dimensioni 
    
    # Agregare i dati csv 
    data_group = add_comune(dati, 'Comune_residenza')
    print(data_group.shape)

    # Fare l'unione tra CSV e Shapefile
    total_data= pd.DataFrame(pd.merge(gdf, data_group, left_on='COMUNE', right_on= 'Comune_residenza', how= 'outer'))
    print(total_data)

    # Matriz de adyacencia --> PENDIENTE
    
    
