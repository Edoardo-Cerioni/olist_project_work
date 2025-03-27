import psycopg
from dotenv import load_dotenv
import os
import  src.common as common
import datetime
import pandas as pd
from tkinter import filedialog

load_dotenv()
host = os.getenv("host")
dbname = os.getenv("dbname")
user = os.getenv("user")
password = os.getenv("password")
port = os.getenv("port")


# metodi ETL per products

def extract():
    print("--EXTRACT products--")
    csv_file_path = filedialog.askopenfilename(
        title="Select csv file (.csv)",
        filetypes=((" Files", "*.csv"), ("All Files", "*.*"))
    )
    df = pd.read_csv(csv_file_path)
    return df

def transform(df):
    print("--TRANSFORM products--")
    df = common.dropduplicates(df)
    df = common.checkNull(df,["pk_product"])

    common.save_processed(df)
    return df

def load(df):
    print("--LOAD products--")

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
                domanda = input("Do you want to replace the table? YES/NO(updates the table) ").strip().upper()
                if domanda == "YES":
                    # cancellare tabella se risponde si
                    sql_delete = """DROP TABLE products CASCADE"""
                    cur.execute(sql_delete)
                    conn.commit()
                    print("Recreating the products table")
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



if __name__ == "__main__":
    df = extract()
