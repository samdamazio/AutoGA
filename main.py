import pandas as pd

def xls_to_xlsx(xls_file_path, new_xlsx_file_path):
    """Converts a .xls file to .xlsx format."""
    xls_data = pd.read_excel(xls_file_path, engine='xlrd')
    xls_data.to_excel(new_xlsx_file_path, index=False)
    print(f"Arquivo convertido salvo em: {new_xlsx_file_path}")

def load_data(simone_path, renata_path):
    """Loads the data from the given file paths."""
    simone_df = pd.read_excel(simone_path)
    renata_df = pd.read_excel(renata_path)
    return simone_df, renata_df

def clean_simone_data(simone_df):
    """Cleans and transforms the Simone dataframe to match the structure of the Renata dataframe."""
    simone_df_clean = simone_df[['Números de telefone', 'Nome']].rename(columns={'Números de telefone': 'telefone', 'Nome': 'nome'})
    simone_df_clean['nome'] = simone_df_clean['nome'].fillna('sem nome')
    simone_df_clean['etiquetas'] = 'Simone, ' + simone_df_clean['nome']
    simone_df_clean['telefone'] = simone_df_clean['telefone'].str.extract(r'(\d+)', expand=False)
    simone_df_final = simone_df_clean[['telefone', 'nome', 'etiquetas']]
    return simone_df_final

def save_data(simone_df_final, output_path):
    """Saves the cleaned Simone dataframe to an Excel file."""
    simone_df_final.to_excel(output_path, index=False)

def main(simone_xls_path, renata_xls_path, simone_xlsx_path, renata_xlsx_path, output_path):
    """Main function to convert, load, clean, and save the data."""
    xls_to_xlsx(simone_xls_path, simone_xlsx_path)
    xls_to_xlsx(renata_xls_path, renata_xlsx_path)
    
    simone_df, renata_df = load_data(simone_xlsx_path, renata_xlsx_path)
    simone_df_final = clean_simone_data(simone_df)
    save_data(simone_df_final, output_path)
    print(f"Data has been cleaned and saved to {output_path}")

# Paths to the input and output files
simone_xls_path = "/mnt/data/simone.xls"
renata_xls_path = "/mnt/data/renata_maria_bc.xls"
simone_xlsx_path = "/mnt/data/simone_converted.xlsx"
renata_xlsx_path = "/mnt/data/renata_maria_bc_converted.xlsx"
output_path = "/mnt/data/simone_cleaned.xlsx"

# Run the main function
if __name__ == "__main__":
    main(simone_xls_path, renata_xls_path, simone_xlsx_path, renata_xlsx_path, output_path)
