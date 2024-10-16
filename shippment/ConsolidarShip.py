import os
import pandas as pd

# Caminho da pasta principal
folder_path = r"D:\OneD\OneDrive - grupojb.log.br\DATABASE PAINEL\BASE - SHIPMENTS_2_teste"

# Lista para armazenar os DataFrames
dataframes = []

# Colunas que você espera que estejam presentes em todos os arquivos
colunas_necessarias = ['shipment', 'remessa', 'pedido', 'dt', 'vol', 'filial']

# Percorrer todas as subpastas e arquivos CSV dentro da pasta principal
for root, dirs, files in os.walk(folder_path):
    for file in files:
        if file.endswith(".csv"):
            file_path = os.path.join(root, file)
            try:
                # Ler o CSV e adicionar à lista de DataFrames (removendo o BOM)
                df = pd.read_csv(file_path, sep=';', encoding='utf-8-sig')
                df.columns = df.columns.str.strip()  # Remover espaços em branco dos nomes das colunas
                print(f"Nomes das colunas no arquivo {file}: {df.columns.tolist()}")
                
                if all(col in df.columns for col in colunas_necessarias):
                    # Selecionar apenas as colunas necessárias
                    df = df[colunas_necessarias]
                    # Converter as colunas para os tipos de dados apropriados
                    df['shipment'] = pd.to_numeric(df['shipment'], errors='coerce').astype('Int64')
                    df['remessa'] = pd.to_numeric(df['remessa'], errors='coerce').astype('Int64')
                    df['pedido'] = pd.to_numeric(df['pedido'], errors='coerce').astype('Int64')
                    df['dt'] = pd.to_numeric(df['dt'], errors='coerce').astype('Int64')
                    df['vol'] = pd.to_numeric(df['vol'], errors='coerce').astype('Int64')
                    df['filial'] = df['filial'].astype(str)
                    dataframes.append(df)
                else:
                    print(f"Arquivo {file} ignorado: Colunas necessárias não estão presentes")
            
            except Exception as e:
                print(f"Erro ao processar o arquivo {file_path}: {e}")

# Concatenar todos os DataFrames em um único DataFrame
if dataframes:  # Verificar se há DataFrames antes de concatenar
    final_df = pd.concat(dataframes, ignore_index=True)

    # Exportar o DataFrame final para um único arquivo CSV
    output_path = r"D:\Sistema\base_consolidada\consolidado_shipment.csv"
    final_df.to_csv(output_path, index=False, sep=';', encoding='latin1')

    print("CSV consolidado criado com sucesso!")
else:
    print("Nenhum arquivo válido encontrado para processar.")