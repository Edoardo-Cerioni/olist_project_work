import shutil
import tkinter as tk
from tkinter import messagebox
import src.common as common
import src.etl.customers as customers
import src.etl.categories as categories
import src.etl.products as products
import src.etl.orders as orders
import src.etl.sellers as sellers
import src.etl.orders_products as orders_products
import subprocess
from tkinter import filedialog
from PIL import Image, ImageTk
import pyfiglet
import platform



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
    orders_products.delete_invalid_orders()
    show_message("Loading Orders Products completed!")

def format_regions():
    common.format_region()
    show_message("Region formatting completed!")

def integrate_city_region():
    customers.complete_city_region()
    show_message("City-region integration completed!")


def open_jupyter_notebook():
    # Crea una finestra root temporanea che viene immediatamente nascosta
    root = tk.Tk()
    root.withdraw()

    # Determina il sistema operativo
    current_os = platform.system()

    # Seleziona il notebook
    notebook_file_path = filedialog.askopenfilename(
        title="Select Jupyter Notebook file (.ipynb)",
        filetypes=(
            ("Jupyter Notebook Files", "*.ipynb"),
            ("All Files", "*.*")
        )
    )

    if not notebook_file_path:
        print("No file selected.")
        return

    # Trova l'eseguibile di Jupyter
    try:
        # Cerca l'eseguibile Jupyter
        jupyter_path = shutil.which('jupyter-notebook') or shutil.which('jupyter')

        if not jupyter_path:
            # Se non trova l'eseguibile, chiedi all'utente di selezionarlo
            jupyter_path = filedialog.askopenfilename(
                title="Select Jupyter Executable",
                filetypes=(
                    ("Executable Files", "*"),
                    ("All Files", "*.*")
                )
            )

        if not jupyter_path:
            print("No Jupyter executable found.")
            return

        # Preparazione del comando per aprire il notebook
        if current_os == "Windows":
            # Su Windows

            subprocess.run([jupyter_path, notebook_file_path], check=True)
        elif current_os == "Darwin":  # macOS
            # Su macOS
            subprocess.run([jupyter_path, notebook_file_path], check=True)
        else:
            print("Unsupported operating system")

    except Exception as e:
        print(f"Error launching Jupyter Notebook: {e}")

def open_powerbi_project():
    # Crea una finestra root temporanea che viene immediatamente nascosta
    root = tk.Tk()
    root.withdraw()
    # Determina il sistema operativo
    current_os = platform.system()
    # Seleziona l'eseguibile di PowerBI

    print("""the PDF version is here: olistit_pw > powerBI_files > 
    project_work_generation_pbi.pdf""")

    pbix_file_path = filedialog.askopenfilename(
        title="Select PowerBI file (.pbix)",
        filetypes=(("Power BI Files", "*.pbix"), ("All Files", "*.*"))
    )

    if not pbix_file_path:
        print("No file selected.")
        return

    try:
        if current_os == "Windows":
            powerbi_path = filedialog.askopenfilename(
                title="Select PBIDesktopstore.exe or PBIDesktop.exe",
                filetypes=(
                    ("Executable Files", ".exe"),
                    ("All Files", "*.*")
                )
            )
            print(f"Starting Power BI with executable: {powerbi_path}")
            print(f"Opening Power BI file: {pbix_file_path}")
            subprocess.run([powerbi_path, pbix_file_path], check=True)

        else:
            print("""the PDF version is here: olistit_pw > powerBI_files > 
            project_work_generation_pbi.pdf""")

    except Exception as e:
        print(f"Error launching PowerBI: {e}")
    except FileNotFoundError:
        print("Error: Unable to find the specified PowerBI executable.")
    except subprocess.CalledProcessError:
        print("Error opening the Power BI file.")


# Funzione per chiudere il programma
def exit_program():
    root.destroy()

# Creazione della finestra principale
root = tk.Tk()
root.title("Project Work - Data Engineer tools set")
root.geometry("450x600")  # Dimensioni finestra
root.configure(bg="#3498DB")  # Sfondo azzurro

# Caricamento dell'immagine di sfondo
background_path = "images_pw/sfondo_display.png"  # Percorso dell'immagine di sfondo
bg_image = Image.open(background_path)
bg_image = bg_image.resize((450, 600))  # Ridimensiona l'immagine per adattarla alla finestra
bg_photo = ImageTk.PhotoImage(bg_image)

# Creazione del Canvas
canvas = tk.Canvas(root, width=450, height=550)
canvas.pack(fill="both", expand=True)

# Inserimento dell'immagine nel Canvas (lo sfondo)
canvas.create_image(0, 0, image=bg_photo, anchor="nw")

canvas.create_text(227, 52, text="Select an operation:", font=("Arial", 12, "bold"), fill="black")
#aggiunto per migliorare visibilità
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
    ("Loading Orders Products", etl_order_products),
    ("Format Regions (Customers e Sellers)", format_regions),
    ("Integrate City-Region (Customers)", integrate_city_region)
]

for text, command in etl_buttons:
    canvas.create_window(225, y_start, window=tk.Button(root, text=text, command=command, width=30, fg="white", bg="#2980B9"), width=button_width, height=button_height)
    y_start += 40

y_start += 20

# Pulsanti con immagini
image_path = "images_pw/previewdatainjupyter.png"  # Percorso del tuo logo
logo = Image.open(image_path)
logo_tk = ImageTk.PhotoImage(logo)
jupyter_button = tk.Button(root, image=logo_tk, command=open_jupyter_notebook)
canvas.create_window(225, y_start, window=jupyter_button)
y_start += 60

image_path2 = "images_pw/openprjct_powerbi.png"  # Percorso del tuo logo
logo2 = Image.open(image_path2)
logo2_tk = ImageTk.PhotoImage(logo2)
power_bi_button = tk.Button(root, image=logo2_tk, command=open_powerbi_project)
canvas.create_window(225, y_start, window=power_bi_button)
y_start += 60

# Pulsante Exit
exit_button = tk.Button(root, text="Exit", command=exit_program, width=30, fg="white", bg="#C0392B")
canvas.create_window(225, y_start, window=exit_button, width=button_width, height=button_height)

# Assicurati di mantenere un riferimento alle immagini
root.logo_tk = logo_tk
root.logo2_tk = logo2_tk


# Avvio della GUI
root.mainloop()