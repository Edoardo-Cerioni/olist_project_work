# Project work - Data Engineer


## Description
This project provides an ETL (Extract, Transform, Load) toolkit for managing and processing data related to customers, categories, products, orders, and sellers. It also includes a graphical interface to facilitate the execution of operations.

## Features
- **ETL for various datasets**: customers, categories, products, orders, sellers, and order-product relationships.
- **Data formatting and integration**: management of regions and city-region associations.
- **Integration with Jupyter Notebook**: allows opening `.ipynb` files directly from the interface.
- **Support for Power BI**: facilitates opening Power BI projects for data analysis.

## Requirements
- **Python 3.x**
- Required libraries can be installed with:
  ```bash
  pip install -r requirements.txt
  ```
- **Jupyter Notebook** (if you want to open `.ipynb` files from the GUI)
- **Power BI Desktop** (if you intend to open `.pbix` files)

## Installation
1. Clone the repository or download the files.
   ```bash
   git clone <repository-url>
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Start the application:
   ```bash
   python main.py
   ```

## Usage
1. Run `main.py` to open the graphical interface.
2. Select one of the available ETL operations.
3. For data analysis, use the buttons to open Jupyter Notebook or Power BI.

## Project Structure
```
project-work/
│── main.py                 # Graphical interface and ETL operations management
│── requirements.txt        # Project dependencies
│── src/
│   ├── common.py           # Common functions
│   ├── etl/
│   │   ├── customers.py    # ETL for customers
│   │   ├── categories.py   # ETL for categories
│   │   ├── products.py     # ETL for products
│   │   ├── orders.py       # ETL for orders
│   │   ├── sellers.py      # ETL for sellers
│   │   ├── orders_products.py  # ETL for order-product relationships
│── images_pw/              # Graphical resources for the GUI
```

## ITA
## Descrizione
In questo progetto sono stati sviluppati gli ETL (Extract, Transform, Load) per la gestione e l'elaborazione dei dati relativi a clienti, categorie, prodotti, ordini e venditori. Include anche un'interfaccia grafica per facilitare l'esecuzione delle operazioni.

## Funzionalità
- **ETL per diversi dataset**: clienti, categorie, prodotti, ordini, venditori e relazioni tra ordini e prodotti.
- **Formattazione e integrazione dati**: gestione delle regioni e associazione città-regione.
- **Anteprima con Jupyter Notebook**: permette di aprire file `.ipynb` direttamente dall'interfaccia.
- **Integrazione con Power BI**: facilita l'apertura di progetti Power BI `.pbix` per l'analisi dei dati.

## Requisiti
- **Python 3.x**
- Librerie necessarie installabili con:
  ```
  pip install -r requirements.txt
  ```
- **Jupyter Notebook** (se si desidera aprire file `.ipynb`)
- **Power BI Desktop** (se si intende aprire file `.pbix` altrimenti visionare il pdf)

## Installazione
1. Clonare il repository o scaricare i file.
   ```bash
   git clone <repository-url>
   ```
2. Installare moduli:
   ```bash
   pip install -r requirements.txt
   ```
3. Avviare l'applicazione:
   ```bash
   python main.py
   ```

## Utilizzo
1. Avviare `main.py` per aprire l'interfaccia grafica.
2. Selezionare le operazioni ETL disponibili.
3. Per l'analisi dati, utilizzare i pulsanti per aprire Jupyter Notebook o Power BI.

## Struttura del progetto
```
project-work/
│── main.py # Interfaccia grafica e gestione operazioni ETL
│── requirements.txt        # Dipendenze del progetto
│── src/
│   ├── common.py           # Funzioni comuni
│   ├── etl/
│   │   ├── customers.py    # ETL per clienti
│   │   ├── categories.py   # ETL per categorie
│   │   ├── products.py     # ETL per prodotti
│   │   ├── orders.py       # ETL per ordini
│   │   ├── sellers.py      # ETL per venditori
│   │   ├── orders_products.py  # ETL per relazioni ordini-prodotti
│── images_pw/              # Risorse grafiche per la GUI
```

## Autore
- Edoardo Cerioni














