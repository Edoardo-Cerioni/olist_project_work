import os
import tkinter as tk
from tkinter import messagebox
import pyfiglet
import src.common as common
import src.customers as customers
import src.categories_byAda as categories
import src.products_byGabri as products
import src.orders_byGabri as orders
import src.sellers as sellers
import src.orders_productsbyGio as orders_products
import matplotlib.pyplot as plt
import pandas as pd
import subprocess
from tkinter import filedialog
from PIL import Image, ImageTk



# Funzione per mostrare messaggi
def show_message(msg):
    messagebox.showinfo("Info", msg)

# Funzioni per eseguire i vari processi ETL
def etl_customers():
    df = customers.extract()
    df = customers.transform(df)
    customers.load(df)
    show_message("Loading Customers completed!")

def etl_categories():
    df = categories.extract()
    df = categories.transform(df)
    categories.load(df)
    show_message("Loading Categories completed!")

def etl_products():
    df = products.extract()
    df = products.transform(df)
    products.load(df)
    show_message("Loading Products completed!")

def etl_orders():
    df = orders.extract()
    df = orders.transform(df)
    orders.load(df)
    show_message("Loading Orders completed!")

def etl_sellers():
    df = sellers.extract()
    df = sellers.transform(df)
    sellers.load(df)
    show_message("Loading Sellers completed!")

def etl_order_products():
    df = orders_products.extract()
    df = orders_products.transform(df)
    orders_products.load(df)
    show_message("Loading Order Products completed!")

def format_regions():
    common.format_region()
    show_message("Region formatting completed!")

def integrate_city_region():
    customers.complete_city_region()
    show_message("City-region integration completed!")

def open_jupyter_notebook():
    # Apre una finestra di dialogo per selezionare un file .ipynb (Jupyter Notebook)
    notebook_file_path = filedialog.askopenfilename(
        title="Select Jupyter Notebook file (.ipynb)",
        filetypes=(("Jupyter Notebook Files", "*.ipynb"), ("All Files", "*.*"))
    )

    if notebook_file_path:  # Se è stato selezionato un file
        print(f"Starting Jupyter Notebook with: {notebook_file_path}")

        # Percorso dell'eseguibile di Jupyter Notebook
        jupyter_path = r"C:\Users\edoce\AppData\Local\Programs\Python\Python313\Scripts\jupyter-notebook.exe"  # Modifica il percorso in base alla tua installazione

        try:
            # Esegui Jupyter Notebook con il file selezionato
            subprocess.run([jupyter_path, notebook_file_path], check=True)
        except FileNotFoundError:
            print("Error: Unable to find Jupyter Notebook. Check the path.")
        except subprocess.CalledProcessError:
            print("Error opening the Jupyter Notebook file.")
    else:
        print("No file selected.")

def open_powerbi_project():
    # Apre una finestra di dialogo per selezionare un file .pbix
    pbix_file_path = filedialog.askopenfilename(
        title="Select PowerBI file (.pbix)",
        filetypes=(("Power BI Files", "*.pbix"), ("All Files", "*.*"))
    )

    if pbix_file_path:  # Se è stato selezionato un file
        print(f"Starting Power BI with: {pbix_file_path}")

        # Percorso dell'eseguibile di Power BI Desktop
        powerbi_path = r"C:\Users\edoce\AppData\Local\Microsoft\WindowsApps\PBIDesktopStore.exe"

        try:
            # Esegui Power BI con il file selezionato
            subprocess.run([powerbi_path, pbix_file_path], check=True)
        except FileNotFoundError:
            print("Error: Unable to find Power BI. Check the path.")
        except subprocess.CalledProcessError:
            print("Error opening the Power BI file.")
    else:
        print("No file selected.")

def exit_program():
    root.destroy()

# ASCII Art all'avvio
ascii_art = pyfiglet.figlet_format("Project Work", font="slant")
print(ascii_art)

# Creazione della finestra principale
root = tk.Tk()
root.title("Project Work - Data Engineer tools set")
root.geometry("400x500")  # Dimensioni finestra
root.configure(bg="#3498DB") #sfondo azzurro

# Creazione dei pulsanti e delle etichette con colori personalizzati
tk.Label(root, text="Select an operation:", font=("Arial", 12, "bold"), fg="white", bg="#3498DB").pack(pady=10)
tk.Button(root, text="Loading Customers", command=etl_customers, width=30, fg="white", bg="#2980B9").pack(pady=5)
tk.Button(root, text="Loading Categories", command=etl_categories, width=30, fg="white", bg="#2980B9").pack(pady=5)
tk.Button(root, text="Loading Products", command=etl_products, width=30, fg="white", bg="#2980B9").pack(pady=5)
tk.Button(root, text="Loading Orders", command=etl_orders, width=30, fg="white", bg="#2980B9").pack(pady=5)
tk.Button(root, text="Loading Sellers", command=etl_sellers, width=30, fg="white", bg="#2980B9").pack(pady=5)
tk.Button(root, text="Loading Order Products", command=etl_order_products, width=30, fg="white", bg="#2980B9").pack(pady=5)
tk.Button(root, text="Format Regions", command=format_regions, width=30, fg="white", bg="#27AE60").pack(pady=5)
tk.Button(root, text="Integrate City-Region", command=integrate_city_region, width=30, fg="white", bg="#27AE60").pack(pady=5)
#tk.Button(root, text="Open data preview on Jupyter", command=open_jupyter_notebook, width=30, fg="black", bg="#F1C40F").pack(pady=10)

image_path = r"C:\Users\edoce\Desktop\Studio\generation_italy_programmi_e_doc\ProgettiPython\olistit_pw\images\previewdatainjupyter.png"  # Percorso del tuo logo
logo = Image.open(image_path)
logo_tk = ImageTk.PhotoImage(logo)
powerbi_button = tk.Button(root, image=logo_tk, command=open_jupyter_notebook)
powerbi_button.pack(pady=10)

#tk.Button(root, text="Open Power BI project", command=open_powerbi_project, width=30, bg="orange").pack(pady=10)

image_path2 = r"C:\Users\edoce\Desktop\Studio\generation_italy_programmi_e_doc\ProgettiPython\olistit_pw\images\openprjct_powerbi.png"  # Percorso del tuo logo
logo2 = Image.open(image_path2)
logo2_tk = ImageTk.PhotoImage(logo2)
powerbi_button = tk.Button(root, image=logo2_tk, command=open_powerbi_project)
powerbi_button.pack(pady=10)
tk.Button(root, text="Exit", command=exit_program, width=30, fg="white", bg="#C0392B").pack(pady=10)


# Avvio della GUI
root.mainloop()