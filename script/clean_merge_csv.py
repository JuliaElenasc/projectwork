import geopandas as gpd
import pandas as pd


def clean_data(path_csv_mercato: str, path_shapefile: str, output_dir: str):
    print('Iniziando pulizia dei dati')
    csv_mercati = pd.read_csv(path_csv_mercato)

    # Lista dei comuni da rimuovere
    comune_del = ["Campione d'Italia", "Capraia Isola", "Isola del Giglio", "Ponza", "Ventotene", "Procida",
                  "Isole Tremiti", "Favignana", "Pantelleria", "Ustica", "Lipari", "Lampedusa e Linosa", "La Maddalena",
                  "Carloforte"]

    # Apertura del file e rimozione dei comuni
    gdf = gpd.read_file(path_shapefile, encoding='utf-8')
    gdf = gdf[~gdf['COMUNE'].isin(comune_del)]

    # Correzione dei dati nel csv
    csv_mercati['Comune_residenza'] = csv_mercati['Comune_residenza'].replace('Bardello',
                                                                              'Bardello con Malgesso e Bregano')
    csv_mercati['Comune_residenza'] = csv_mercati['Comune_residenza'].replace('Bregano',
                                                                              'Bardello con Malgesso e Bregano')
    csv_mercati['Comune_residenza'] = csv_mercati['Comune_residenza'].replace('Tonengo', 'Moransengo-Tonengo')
    csv_mercati['Comune_residenza'] = csv_mercati['Comune_residenza'].replace('Vendrogno', 'Bellano')
    csv_mercati['Comune_residenza'] = csv_mercati['Comune_residenza'].replace('Riva Valdobbia', 'Alagna Valsesia')
    csv_mercati['Comune_residenza'] = csv_mercati['Comune_residenza'].replace('Monteciccardo', 'Pesaro')
    csv_mercati['Comune_residenza'] = csv_mercati['Comune_residenza'].replace('Faedo', "San Michele all'Adige")
    csv_mercati['Comune_residenza'] = csv_mercati['Comune_residenza'].replace('Valmala', "Busca")
    csv_mercati['Comune_residenza'] = csv_mercati['Comune_residenza'].replace('Castellar', "Saluzzo")
    csv_mercati['Comune_residenza'] = csv_mercati['Comune_residenza'].replace('Camo', "Santo Stefano Belbo")
    csv_mercati['Comune_residenza'] = csv_mercati['Comune_residenza'].replace("Ca' d'Andrea", "Torre de' Picenardi")
    # Raggruppamento dei dati del csv
    data_group = csv_mercati.groupby('Comune_residenza').mean(numeric_only=True).reset_index()

    # Unione tra lo shapefile e il csv
    total_data = pd.DataFrame(pd.merge(gdf, data_group, left_on='COMUNE', right_on='Comune_residenza', how='outer'))

    # Rimozione dei dati vuoti o mancanti dello shapefile
    total_data_cleaned = total_data.dropna(subset=['COMUNE'])

    columns_delete = ['COD_RIP', 'COD_REG', 'COD_PROV', 'COD_CM', 'COD_UTS', 'COMUNE', 'COMUNE_A', 'CC_UTS',
                      'SHAPE_LENG', 'Shape_Le_1', 'geometry']
    total_data_cleaned = total_data_cleaned.drop(columns_delete, axis=1)

    # Salvataggio dei dati
    total_data_cleaned.to_csv(output_dir, index=False)
    print('Dati puliti salvati nella cartella output')



