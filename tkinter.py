import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox

def select_file():
    file_path = filedialog.askopenfilename()
    return file_path

def run_transformation():
    simone_xls_path = select_file()
    renata_xls_path = select_file()
    simone_xlsx_path = filedialog.asksaveasfilename(defaultextension=".xlsx", initialfile="simone_converted.xlsx")
    renata_xlsx_path = filedialog.asksaveasfilename(defaultextension=".xlsx", initialfile="renata_maria_bc_converted.xlsx")
    output_path = filedialog.asksaveasfilename(defaultextension=".xlsx", initialfile="simone_cleaned.xlsx")
    
    if simone_xls_path and renata_xls_path and simone_xlsx_path and renata_xlsx_path and output_path:
        main(simone_xls_path, renata_xls_path, simone_xlsx_path, renata_xlsx_path, output_path)
        messagebox.showinfo("Success", f"Data has been cleaned and saved to {output_path}")

root = tk.Tk()
root.title("Data Transformation Tool")

btn = tk.Button(root, text="Transform Data", command=run_transformation)
btn.pack(pady=20)

root.mainloop()
