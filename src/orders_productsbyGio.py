import src.common as common
import os
from dotenv import load_dotenv
import psycopg
import datetime


load_dotenv()
host = os.getenv("host")
dbname = os.getenv("dbname")
user = os.getenv("user")
password = os.getenv("password")
port = os.getenv("port")


def extract():
    print("questo è il metodo EXTRACT per order_products")
    df = common.read_file()
    return df

def transform(df):
    print("Transformation Data")
    df = common.checkNull(df, ["order_id","product_id"])#seller_id da aggiungere x sellers
    df = common.dropduplicates(df)
    common.save_processed(df)
    return df

def main():
    print("questo è il metodo Main")
    df = extract()
    print("file di partenza")
    print(df)
    df = transform(df)
    print("file formattato")
    print(df, end="\n\n")
    load(df)

def load(df):
    print("LOAD")
    df["last_updated"] = datetime.datetime.now().isoformat(sep=" ", timespec="seconds")
    with psycopg.connect(host=host, dbname=dbname, user=user, password=password, port=port) as conn:
        with conn.cursor() as cur:
            sql = """
            CREATE TABLE orders_products (
            pk_order_product SERIAL PRIMARY KEY,
            fk_order character varying,
            order_item INTEGER,
            fk_product character varying,
            seller_id character varying,
            price NUMERIC(10,2),
            freight NUMERIC(10,2),
            last_updated TIMESTAMP,
            FOREIGN KEY(fk_order)
            REFERENCES orders(pk_order),
            FOREIGN KEY(fk_product)
            REFERENCES products(pk_product)
            );"""


            try:
                cur.execute(sql)
                # Inserimento report nel database
            except psycopg.errors.DuplicateTable as ex:
                conn.commit()
                print(ex)
                domanda = input("Vuoi sostituire la tabella? SI | NO (aggiunge i valori della tabella a quella originale) ").strip().upper()
                if domanda == "SI":
                    # cancellare tabella se risponde si
                    sqldelete = """DROP TABLE orders_products;"""
                    cur.execute(sqldelete)
                    conn.commit()
                    print("Recreating orders_products table")
                    cur.execute(sql)


            sql = """
            INSERT INTO orders_products (fk_order, order_item, fk_product, seller_id, price, freight,last_updated)
            VALUES (%s, %s, %s, %s, %s, %s , %s)
            """
            common.caricamento_barra(df, cur, sql)

            conn.commit()
            #except psycopg.OperationalError as e:
                #print(f"Error connecting to database: {e}")

if __name__ == "__main__":
    main()
