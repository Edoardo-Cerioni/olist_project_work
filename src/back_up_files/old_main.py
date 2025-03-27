import subprocess
import src.common as common
import src.etl.customers as customers
import src.etl.categories as categories
import src.etl.products as products
import src.etl.orders as orders
import src.etl.sellers as sellers
import src.etl.orders_products as orders_products


if __name__ == "__main__":
    risposta = ""
    while risposta != "0":
        risposta = input("""Enter a command 
        1 = run ETL for customers
        2 = run integration of region and city data
        3 = format region names for PowerBI
        4 = run ETL for categories
        5 = run ETL for products
        6 = run ETL for orders
        7 = run ETL for sellers
        8 = run ETL for order_products
        9 = Open Jupyter to perform initial data analysis
        0 = exit the program
        \n\nCommand: """)
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
            df_sellers = sellers.extract()
            df_sellers = sellers.transform(df_sellers)
            sellers.load(df_sellers)
        elif risposta == "8":
            df_orders_products = orders_products.extract()
            df_orders_products = orders_products.transform(df_orders_products)
            orders_products.load(df_orders_products)
            orders_products.delete_invalid_orders()
        elif risposta == "9":
            print("Starting Jupyter Notebook...")
            try:
                subprocess.run(["jupyter", "notebook"], check=True)
            except subprocess.CalledProcessError:
                print("Error starting Jupyter Notebook. Ensure that Jupyter is installed correctly.")
        elif risposta == "0":
            print("Exiting the program...")
            exit()
        else:
            print("\n\nInvalid option. Please try again.\n\n")


