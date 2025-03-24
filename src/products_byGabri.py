import psycopg
from dotenv import load_dotenv
import os
import  src.common as common
import datetime
import pandas as pd

load_dotenv()
host = os.getenv("host")
dbname = os.getenv("dbname")
user = os.getenv("user")
password = os.getenv("password")
port = os.getenv("port")


# metodi ETL per products

def extract():
    print("questo è il metodo EXTRACT per products")
    df = common.read_file()
    return df

def transform(df):
    print("questo è il metodo TRANSFORM per products")
    df = common.dropduplicates(df)
    df = common.checkNull(df,["pk_product"])

    common.save_processed(df)
    return df

def load(df):
    print("questo è il metodo LOAD per products")

    df["last_updated"] = datetime.datetime.now().isoformat(sep=" ", timespec="seconds")

    with psycopg.connect(host=host, dbname=dbname, user=user, password=password, port=port) as conn:
        with conn.cursor() as cur:


            sql = """
            CREATE TABLE products (
            pk_product VARCHAR PRIMARY KEY,
            fk_category INTEGER,
            name_length INTEGER, 
            description_length INTEGER,
            imgs_qty INTEGER,
            last_updated TIMESTAMP,
            FOREIGN KEY (fk_category)
            REFERENCES categories (pk_category));
            """

            try:
                cur.execute(sql)
            except psycopg.errors.DuplicateTable as ex:
                conn.commit()
                print(ex)
                domanda = input("Vuoi sostituire la tabella? SI NO(aggiunge i valori della tabella a quella originale) ").strip().upper()
                if domanda == "SI":
                    # cancellare tabella se risponde si
                    sql_delete = """DROP TABLE products CASCADE"""
                    cur.execute(sql_delete)
                    conn.commit()
                    print("ricreo tabella products")
                    cur.execute(sql)

            sql = """
            INSERT INTO products (
            pk_product, fk_category, name_length, description_length, imgs_qty, last_updated
            )
            VALUES (%s, %s, %s, %s, %s, %s) ON CONFLICT (pk_product) DO UPDATE SET 
            ( fk_category, name_length, description_length, imgs_qty, last_updated) = 
            (EXCLUDED.fk_category, EXCLUDED.name_length, EXCLUDED.description_length, EXCLUDED.imgs_qty, EXCLUDED.last_updated)
            """
            common.caricamento_barra(df, cur, sql)


            conn.commit()

"""def dump():
    with psycopg.connect(host=host, dbname=dbname, user=user, password=password, port=port) as conn:
        with conn.cursor() as cur:
            sql = "SELECT * FROM products"
            cur.execute(sql)
            df = pd.DataFrame(cur, columns = ["pk_product", "fk_category", "name_lenght", "description_lentgh","imgs_qty", "last_updated"])
            df = df.to_csv("../data/processed/products_processed.csv", index = False)"""


if __name__ == "__main__":
    df = extract()
