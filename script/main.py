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
    gdf = gpd.read_file(comune, encoding='utf-8')
    print('shapefile:',gdf.shape) # vedere le dimensioni 
    
    #Corregere nomi non aggiornati nel csv
    dati['Comune_residenza'] = dati['Comune_residenza'].replace('Bardello', 'Bardello con Malgesso e Bregano')
    dati['Comune_residenza'] = dati['Comune_residenza'].replace('Bregano', 'Bardello con Malgesso e Bregano')
    dati['Comune_residenza'] = dati['Comune_residenza'].replace('Tonengo', 'Moransengo-Tonengo')
    dati['Comune_residenza'] = dati['Comune_residenza'].replace('Vendrogno', 'Bellano')
    dati['Comune_residenza'] = dati['Comune_residenza'].replace('Riva Valdobbia', 'Alagna Valsesia')
    dati['Comune_residenza'] = dati['Comune_residenza'].replace('Monteciccardo', 'Pesaro')
    dati['Comune_residenza'] = dati['Comune_residenza'].replace('Faedo', "San Michele all'Adige")
    dati['Comune_residenza'] = dati['Comune_residenza'].replace('Valmala', "Busca")
    dati['Comune_residenza'] = dati['Comune_residenza'].replace('Castellar', "Saluzzo")
    dati['Comune_residenza'] = dati['Comune_residenza'].replace('Camo', "Santo Stefano Belbo")
    dati['Comune_residenza'] = dati['Comune_residenza'].replace("Ca' d'Andrea", "Torre de' Picenardi")
    
    # Agregare i dati csv 
    data_group = add_comune(dati, 'Comune_residenza')
    print('csv:',data_group.shape)

    # Fare l'unione tra CSV e Shapefile
    total_data= pd.DataFrame(pd.merge(gdf, data_group, left_on='COMUNE', right_on= 'Comune_residenza', how= 'outer'))
    print('merge:',total_data.shape)
    print('merge types',total_data.dtypes)
    # Vedere tutti i datti che non sono uniti
    #nan_data = total_data[total_data['COMUNE'].isna()]
    #print(nan_data)

    # Cancella tutti i dati che non si trovano nel shapefile
    total_data_cleaned = total_data.dropna(subset=['COMUNE'])
    print(total_data_cleaned.shape)

    print('hasta aqui')

    # Matriz de adyacencia --> PENDIENTE
    # Modelo
    # Definir la credibilidad
    # crea una matriz con las columnas A,n, media_random y errore
    
    
    
