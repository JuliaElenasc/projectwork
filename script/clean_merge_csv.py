#Aprire file proporzionati
import geopandas as gpd
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import config
import os


def clean_data (path_csv_mercato, path_shapefile, output_dir):
    
    shapefile_comune = path_shapefile
    csv_mercati = pd.read_csv(path_csv_mercato)
    
    print("Reading input files, please wait...")
        
    # Delete data
    print("Cleaning data and obtaining the city code...")
    comune_del= ["Campione d'Italia", "Capraia Isola", "Isola del Giglio", "Ponza", "Ventotene", "Procida", "Isole Tremiti", "Favignana", "Pantelleria", "Ustica", "Lipari", "Lampedusa e Linosa", "La Maddalena", "Carloforte"]
    
    # Open the shapefile
    gdf = gpd.read_file(shapefile_comune, encoding='utf-8')
    gdf = gdf[~gdf['COMUNE'].isin(comune_del)]
      
    # Correct outdated names in the CSV
    csv_mercati['Comune_residenza'] = csv_mercati['Comune_residenza'].replace('Bardello', 'Bardello con Malgesso e Bregano')
    csv_mercati['Comune_residenza'] = csv_mercati['Comune_residenza'].replace('Bregano', 'Bardello con Malgesso e Bregano')
    csv_mercati['Comune_residenza'] = csv_mercati['Comune_residenza'].replace('Tonengo', 'Moransengo-Tonengo')
    csv_mercati['Comune_residenza'] = csv_mercati['Comune_residenza'].replace('Vendrogno', 'Bellano')
    csv_mercati['Comune_residenza'] = csv_mercati['Comune_residenza'].replace('Riva Valdobbia', 'Alagna Valsesia')
    csv_mercati['Comune_residenza'] = csv_mercati['Comune_residenza'].replace('Monteciccardo', 'Pesaro')
    csv_mercati['Comune_residenza'] = csv_mercati['Comune_residenza'].replace('Faedo', "San Michele all'Adige")
    csv_mercati['Comune_residenza'] = csv_mercati['Comune_residenza'].replace('Valmala', "Busca")
    csv_mercati['Comune_residenza'] = csv_mercati['Comune_residenza'].replace('Castellar', "Saluzzo")
    csv_mercati['Comune_residenza'] = csv_mercati['Comune_residenza'].replace('Camo', "Santo Stefano Belbo")
    csv_mercati['Comune_residenza'] = csv_mercati['Comune_residenza'].replace("Ca' d'Andrea", "Torre de' Picenardi")
    
    # Group i dati csv 
    data_group = group = csv_mercati.groupby('Comune_residenza').mean().reset_index()
 
    # Merge CSV e Shapefile
    total_data= pd.DataFrame(pd.merge(gdf, data_group, left_on='COMUNE', right_on= 'Comune_residenza', how= 'outer'))
   
    # Delete empty data and data not found in the shapefile
    total_data_cleaned = total_data.dropna(subset=['COMUNE'])
    
    columns_delete= ['COD_RIP','COD_REG', 'COD_PROV','COD_CM','COD_UTS','COMUNE','COMUNE_A','CC_UTS','SHAPE_LENG','Shape_Le_1', 'geometry']
    total_data_cleaned = total_data_cleaned.drop(columns_delete, axis=1)
  
    # Export data to a new CSV
    name_output_file= 'Mercato_code.csv'
    result = os.path.join(output_dir,name_output_file)
    
    total_data_cleaned.to_csv(result, index=False)
    print (f'File saved in {result}')



