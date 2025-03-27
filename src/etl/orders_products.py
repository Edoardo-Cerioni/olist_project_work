import src.common as common
import os
from dotenv import load_dotenv
import psycopg
import datetime
import pandas as pd
from tkinter import filedialog


load_dotenv()
host = os.getenv("host")
dbname = os.getenv("dbname")
user = os.getenv("user")
password = os.getenv("password")
port = os.getenv("port")



def extract():
    print("--EXTRACT orders products--")
    csv_file_path = filedialog.askopenfilename(
        title="Select csv file (.csv)",
        filetypes=((" Files", "*.csv"), ("All Files", "*.*"))
    )
    df = pd.read_csv(csv_file_path)
    return df

def transform(df):
    print("--TRANSFORM orders products--")
    df = common.dropduplicates(df)
    df = common.checkNull(df, ["order_id", "product_id"])#seller_id da aggiungere x sellers
    common.save_processed(df)
    return df

def load(df):
    print("--LOAD orders products--")
    df["last_updated"] = datetime.datetime.now().isoformat(sep=" ", timespec="seconds")
    with psycopg.connect(host=host, dbname=dbname, user=user, password=password, port=port) as conn:
        with conn.cursor() as cur:
            sql = """
            CREATE TABLE orders_products (
            pk_order_product SERIAL PRIMARY KEY,
            fk_order VARCHAR UNIQUE,
            order_item INTEGER UNIQUE,
            fk_product VARCHAR,
            fk_seller VARCHAR,
            price NUMERIC(10,2),
            freight NUMERIC(10,2),
            last_updated TIMESTAMP,
            FOREIGN KEY (fk_order) REFERENCES orders(pk_order),
            FOREIGN KEY (fk_product) REFERENCES products(pk_product),
            FOREIGN KEY (fk_seller) REFERENCES sellers(pk_seller)
            );"""




            try:
                cur.execute(sql)
                # Inserimento report nel database
            except psycopg.errors.DuplicateTable as ex:
                conn.commit()
                print(ex)
                domanda = input("Do you want to replace the table? YES | NO(add records from the new CSV) ").strip().upper()
                if domanda == "YES":
                    # cancellare tabella se risponde si
                    sqldelete = """DROP TABLE orders_products CASCADE;"""
                    cur.execute(sqldelete)
                    conn.commit()
                    print("Recreating the orders_products table")
                    cur.execute(sql)

            sql = """
            INSERT INTO orders_products (fk_order, order_item, fk_product, fk_seller, price, freight, last_updated)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
            ON CONFLICT DO NOTHING
            """
            common.caricamento_barra(df, cur, sql)

            conn.commit()
            delete_invalid_orders()

def delete_invalid_orders():
    with psycopg.connect(host=host, dbname=dbname, user=user, password=password, port=port) as conn:
        with conn.cursor() as cur:

            sql = f"""DELETE FROM orders_products 
            WHERE fk_order IN (
            SELECT pk_order FROM orders 
            WHERE delivered_timestamp IS NULL 
            AND status = 'delivered'
            ); """

            cur.execute(sql)

            sql = f"""DELETE FROM orders  
            WHERE delivered_timestamp IS NULL 
            AND status = 'delivered'
            ; """

            cur.execute(sql)


            conn.commit()

"""def main():
    print("questo è il metodo Main")
    df = extract()
    print("file di partenza")
    print(df)
    df = transform(df)
    print("file formattato")
    print(df, end="\n\n")
    load(df)


if __name__ == "__main__":
    main()"""
