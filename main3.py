import tkinter as tk
from tkinter import messagebox
import src.common as common
import src.customers as customers
import src.categories as categories
import src.products as products
import src.orders as orders
import src.sellers as sellers
import src.orders_products as orders_products
import subprocess
from tkinter import filedialog
from PIL import Image, ImageTk
import pyfiglet


# ASCII Art all'avvio
ascii_art = pyfiglet.figlet_format("Project Work", font="slant")
print(ascii_art)

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

# Funzione per chiudere il programma
def exit_program():
    root.destroy()

# Creazione della finestra principale
root = tk.Tk()
root.title("Project Work - Data Engineer tools set")
root.geometry("450x600")  # Dimensioni finestra
root.configure(bg="#3498DB")  # Sfondo azzurro

# Caricamento dell'immagine di sfondo
background_path = r"C:\Users\edoce\Desktop\Studio\generation_italy_programmi_e_doc\ProgettiPython\olistit_pw\images\sfondo_display.png"  # Percorso dell'immagine di sfondo
bg_image = Image.open(background_path)
bg_image = bg_image.resize((450, 600))  # Ridimensiona l'immagine per adattarla alla finestra
bg_photo = ImageTk.PhotoImage(bg_image)

# Creazione del Canvas
canvas = tk.Canvas(root, width=450, height=550)
canvas.pack(fill="both", expand=True)

# Inserimento dell'immagine nel Canvas (lo sfondo)
canvas.create_image(0, 0, image=bg_photo, anchor="nw")

canvas.create_text(227, 52, text="Select an operation:", font=("Arial", 12, "bold"), fill="black")
canvas.create_text(225, 50, text="Select an operation:", font=("Arial", 12, "bold"), fill="white")


# Pulsanti ETL
y_start = 100
button_width = 250
button_height = 30

etl_buttons = [
    ("Loading Customers", etl_customers),
    ("Loading Categories", etl_categories),
    ("Loading Products", etl_products),
    ("Loading Orders", etl_orders),
    ("Loading Sellers", etl_sellers),
    ("Loading Order Products", etl_order_products),
    ("Format Regions", format_regions),
    ("Integrate City-Region", integrate_city_region)
]

for text, command in etl_buttons:
    canvas.create_window(225, y_start, window=tk.Button(root, text=text, command=command, width=30, fg="white", bg="#2980B9"), width=button_width, height=button_height)
    y_start += 40

y_start += 20

# Pulsanti con immagini
image_path = r"C:\Users\edoce\Desktop\Studio\generation_italy_programmi_e_doc\ProgettiPython\olistit_pw\images\previewdatainjupyter.png"  # Percorso del tuo logo
logo = Image.open(image_path)
logo_tk = ImageTk.PhotoImage(logo)
jupyter_button = tk.Button(root, image=logo_tk, command=open_jupyter_notebook)
canvas.create_window(225, y_start, window=jupyter_button)
y_start += 60

image_path2 = r"C:\Users\edoce\Desktop\Studio\generation_italy_programmi_e_doc\ProgettiPython\olistit_pw\images\openprjct_powerbi.png"  # Percorso del tuo logo
logo2 = Image.open(image_path2)
logo2_tk = ImageTk.PhotoImage(logo2)
powerbi_button = tk.Button(root, image=logo2_tk, command=open_powerbi_project)
canvas.create_window(225, y_start, window=powerbi_button)
y_start += 60

# Pulsante Exit
exit_button = tk.Button(root, text="Exit", command=exit_program, width=30, fg="white", bg="#C0392B")
canvas.create_window(225, y_start, window=exit_button, width=button_width, height=button_height)

# Assicurati di mantenere un riferimento alle immagini
root.logo_tk = logo_tk
root.logo2_tk = logo2_tk


# Avvio della GUI
root.mainloop()