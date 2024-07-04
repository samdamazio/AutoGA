import os
import re
import pandas as pd
import tkinter as tk
from tkinter import filedialog, messagebox
from tkinterdnd2 import TkinterDnD, DND_FILES
import sys

# Carregar a lista de nomes comuns dos arquivos CSV
def load_common_names():
    if getattr(sys, 'frozen', False):
        # If the application is run as a bundle, the path is relative to the bundle
        base_path = sys._MEIPASS
    else:
        base_path = os.path.dirname(os.path.abspath(__file__))
    
    fem_names_path = os.path.join(base_path, 'db', 'ibge-fem-10000.csv')
    mas_names_path = os.path.join(base_path, 'db', 'ibge-mas-10000.csv')
    
    fem_names_df = pd.read_csv(fem_names_path, usecols=[0], header=None, names=["name"])
    mas_names_df = pd.read_csv(mas_names_path, usecols=[0], header=None, names=["name"])
    
    common_names = set(fem_names_df['name'].str.capitalize().tolist() + mas_names_df['name'].str.capitalize().tolist())
    return common_names

common_names = load_common_names()

def xls_to_xlsx(xls_file_path, new_xlsx_file_path):
    """Converts a .xls file to .xlsx format."""
    xls_data = pd.read_excel(xls_file_path, engine='xlrd')
    xls_data.to_excel(new_xlsx_file_path, index=False)
    print(f"Arquivo convertido salvo em: {new_xlsx_file_path}")

def load_data(file_path):
    """Loads the data from the given file paths."""
    df = pd.read_excel(file_path)
    return df

def extract_phone_number(phone_str):
    """Extracts and cleans the phone number from various formats."""
    if pd.isna(phone_str):
        return ''
    cleaned_phone = re.sub(r'\D', '', str(phone_str))
    if not cleaned_phone.startswith('55'):
        cleaned_phone = '55' + cleaned_phone  # Add country code if not present
    return cleaned_phone

def get_first_common_name(full_name):
    """Gets the first common name from the full name, otherwise returns 'sem nome'."""
    if pd.isna(full_name):
        return 'sem nome'
    for part in full_name.split():
        cleaned_part = re.sub(r'\W', '', part).capitalize()  # Remove non-alphanumeric characters and capitalize
        if cleaned_part in common_names:
            return cleaned_part
    return 'sem nome'

def clean_data(df, file_name):
    """Cleans and transforms the dataframe."""
    df_clean = df[['Números de telefone', 'Nome']].rename(columns={'Números de telefone': 'telefone', 'Nome': 'nome'})
    df_clean['nome'] = df_clean['nome'].apply(get_first_common_name)
    df_clean['etiquetas'] = file_name
    df_clean['telefone'] = df_clean['telefone'].apply(extract_phone_number)
    
    # Add ", sem nome," to etiquetas if the name is "sem nome"
    df_clean.loc[df_clean['nome'] == 'sem nome', 'etiquetas'] += ', sem nome,'

    # Remove rows where phone number does not have exactly 13 digits
    df_clean = df_clean[df_clean['telefone'].str.len() == 13]

    # Remove duplicate rows
    df_clean = df_clean.drop_duplicates()

    df_final = df_clean[['telefone', 'nome', 'etiquetas']]
    return df_final

def save_data(df_final, output_path):
    """Saves the cleaned dataframe to an Excel file."""
    df_final.to_excel(output_path, index=False)

def main(file_path, output_dir):
    """Main function to convert, load, clean, and save the data."""
    # Create output directory if it doesn't exist
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Generate output paths
    converted_xlsx_path = os.path.join(output_dir, os.path.basename(file_path).replace(".xls", "_converted.xlsx"))
    output_path = os.path.join(output_dir, os.path.basename(file_path).replace(".xls", "_bc.xlsx"))

    # Convert and process the data
    xls_to_xlsx(file_path, converted_xlsx_path)
    
    df = load_data(converted_xlsx_path)
    file_name = os.path.basename(file_path).replace(".xls", "")
    df_final = clean_data(df, file_name)
    save_data(df_final, output_path)
    
    # Delete the converted file
    os.remove(converted_xlsx_path)
    
    print(f"Data has been cleaned and saved to {output_path}")

def select_file():
    return filedialog.askopenfilename()

def run_transformation():
    file_path = select_file()
    output_dir = os.path.join(os.getcwd(), "planilhas_bc")
    
    if file_path:
        main(file_path, output_dir)
        messagebox.showinfo("Success", f"Data has been cleaned and saved to {output_dir}")

def drop(event):
    paths = event.data.split()
    output_dir = os.path.join(os.getcwd(), "planilhas_bc")
    
    if len(paths) == 1:
        file_path = paths[0]
        main(file_path, output_dir)
        messagebox.showinfo("Success", f"Data has been cleaned and saved to {output_dir}")

root = TkinterDnD.Tk()
root.title("Data Transformation Tool")
root.geometry("600x400")

frame = tk.Frame(root)
frame.pack(pady=20)

label = tk.Label(frame, text="Drag and drop the .xls file here or click the button to select it.")
label.pack(pady=10)

button = tk.Button(frame, text="Transform Data", command=run_transformation)
button.pack(pady=10)

root.drop_target_register(DND_FILES)
root.dnd_bind('<<Drop>>', drop)

root.mainloop()

if __name__ == '__main__':
    try:
        root.mainloop()
    except Exception as e:
        messagebox.showerror("Error", str(e))
        print(str(e))
