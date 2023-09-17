#Aprire file proporzionati
import geopandas as gpd
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

def add_comune(df, col): #funzione che agruppa le datti duplicati da un csv
    group = df.groupby(col).mean().reset_index()
    return group


if __name__=='__main__':
    #Files
    comune= '.\\dati\Limiti01012023\Limiti01012023\Com01012023\Com01012023_WGS84.shp'
    dati = pd.read_csv('.\\dati\DatidiMercato.csv')
    
    # Delete data
    comune_del= ["Campione d'Italia", "Capraia Isola", "Isola del Giglio", "Ponza", "Ventotene", "Procida", "Isole Tremiti", "Favignana", "Pantelleria", "Ustica", "Lipari", "Lampedusa e Linosa", "La Maddalena", "Carloforte"]
    # Open the shapefile
    gdf = gpd.read_file(comune, encoding='utf-8')
    gdf = gdf[~gdf['COMUNE'].isin(comune_del)]

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
    
    columns_delete= ['COD_RIP','COD_REG', 'COD_PROV','COD_CM','COD_UTS', 'PRO_COM_T','COMUNE','COMUNE_A','CC_UTS','SHAPE_LENG','Shape_Le_1', 'geometry']
    total_data_cleaned = total_data_cleaned.drop(columns_delete, axis=1)
    print('merge types',total_data_cleaned.dtypes)

    # esporta dataframe a csv
    nome_file = 'Mercato_code.csv'
    total_data_cleaned.to_csv(nome_file, index=False)
    print('file saved')


    
    