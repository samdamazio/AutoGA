import os
import re
import pandas as pd
import tkinter as tk
from tkinter import filedialog, messagebox
from tkinterdnd2 import TkinterDnD, DND_FILES

def xls_to_xlsx(xls_file_path, new_xlsx_file_path):
    """Converts a .xls file to .xlsx format."""
    xls_data = pd.read_excel(xls_file_path, engine='xlrd')
    xls_data.to_excel(new_xlsx_file_path, index=False)
    print(f"Arquivo convertido salvo em: {new_xlsx_file_path}")

def load_data(simone_path):
    """Loads the data from the given file paths."""
    simone_df = pd.read_excel(simone_path)
    return simone_df

def extract_phone_number(phone_str):
    """Extracts and cleans the phone number from various formats."""
    if pd.isna(phone_str):
        return ''
    cleaned_phone = re.sub(r'\D', '', str(phone_str))
    if not cleaned_phone.startswith('55'):
        cleaned_phone = '55' + cleaned_phone  # Add country code if not present
    return cleaned_phone

def clean_simone_data(simone_df, file_name):
    """Cleans and transforms the Simone dataframe."""
    simone_df_clean = simone_df[['Números de telefone', 'Nome']].rename(columns={'Números de telefone': 'telefone', 'Nome': 'nome'})
    simone_df_clean['nome'] = simone_df_clean['nome'].fillna('sem nome')
    simone_df_clean['etiquetas'] = file_name
    simone_df_clean['telefone'] = simone_df_clean['telefone'].apply(extract_phone_number)
    simone_df_final = simone_df_clean[['telefone', 'nome', 'etiquetas']]
    return simone_df_final

def save_data(simone_df_final, output_path):
    """Saves the cleaned Simone dataframe to an Excel file."""
    # Ensure the file is not open
    if os.path.exists(output_path):
        os.remove(output_path)
    simone_df_final.to_excel(output_path, index=False)

def main(simone_xls_path, output_dir):
    """Main function to convert, load, clean, and save the data."""
    # Create output directory if it doesn't exist
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Generate output paths
    simone_xlsx_path = os.path.join(output_dir, os.path.basename(simone_xls_path).replace(".xls", "_converted.xlsx"))
    output_path = os.path.join(output_dir, os.path.basename(simone_xls_path).replace(".xls", "_bc.xlsx"))

    # Convert and process the data
    xls_to_xlsx(simone_xls_path, simone_xlsx_path)
    
    simone_df = load_data(simone_xlsx_path)
    file_name = os.path.basename(simone_xls_path).replace(".xls", "")
    simone_df_final = clean_simone_data(simone_df, file_name)
    save_data(simone_df_final, output_path)
    print(f"Data has been cleaned and saved to {output_path}")

def select_file():
    return filedialog.askopenfilename()

def run_transformation():
    simone_xls_path = select_file()
    output_dir = os.path.join(os.getcwd(), "planilhas_bc")
    
    if simone_xls_path:
        main(simone_xls_path, output_dir)
        messagebox.showinfo("Success", f"Data has been cleaned and saved to {output_dir}")

def drop(event):
    paths = event.data.split()
    output_dir = os.path.join(os.getcwd(), "planilhas_bc")
    
    if len(paths) == 1:
        simone_xls_path = paths[0]
        main(simone_xls_path, output_dir)
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
