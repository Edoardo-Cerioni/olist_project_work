import subprocess
import src.common as common
import src.customers as customers
import src.categories_byAda as categories
import src.products_byGabri as products
import src.orders_byGabri as orders

import src.orders_productsbyGio as orders_products






if __name__ == "__main__":
    risposta = ""
    while risposta != "0":
        risposta = input("""Inserisci un comando 
        1 = esegui ETL costumers
        2 = esegui integrazione dei dati regione e città
        3 = formatta nomi regioni per PowerBI
        4 = esegui ETL categories
        5 = esegui ETL products
        6 = esegui ETL orders
        7 = esegui ETL order_products
        8 = Apri Jupyter per eseguire una prima l'analisi dei dati
        0 = esci dal programma
        \n\nComando: """)
        if risposta == "1":
            df_customers = customers.extract()
            df_customers = customers.transform(df_customers)
            customers.load(df_customers)
        elif risposta == "2":
            customers.complete_city_region()
        elif risposta == "3":
            common.format_region()
        elif risposta == "4":
            df_categories = categories.extract()
            df_categories = categories.transform(df_categories)
            categories.load(df_categories)
        elif risposta == "5":
            df_products = products.extract()
            df_products = products.transform(df_products)
            products.load(df_products)
        elif risposta == "6":
            df_orders = orders.extract()
            df_orders = orders.transform(df_orders)
            orders.load(df_orders)
        elif risposta == "7":
            df_orders_products = orders_products.extract()
            df_orders_products = orders_products.transform(df_orders_products)
            orders_products.load(df_orders_products)
        elif risposta == "8":
            print("Avvio Jupyter Notebook...")
            try:
                subprocess.run(["jupyter", "notebook"], check=True)
            except subprocess.CalledProcessError:
                print("Errore nell'avvio di Jupyter Notebook. Assicurati che Jupyter sia installato correttamente.")
        elif risposta == "0":
            print("Uscita dal programma...")
            exit()
        else:
            print("\n\nOpzione non valida. Riprova.\n\n")