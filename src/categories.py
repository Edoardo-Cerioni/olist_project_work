import pandas as pd
import src.common as common
import os
import psycopg
from dotenv import load_dotenv
from tkinter import filedialog


load_dotenv()
host = os.getenv("host")
dbname = os.getenv("dbname")
user = os.getenv("user")
password = os.getenv("password")
port = os.getenv("port")

def extract():
    print("--EXTRACT categories--")
    csv_file_path = filedialog.askopenfilename(
        title="Select csv file (.csv)",
        filetypes=((" Files", "*.csv"), ("All Files", "*.*"))
    )
    df = pd.read_csv(csv_file_path)
    return df

def transform(df):
    print("--TRANSFORM categories--")
    df = common.dropduplicates(df)
    df = common.checkNull(df, ["pk_category"])
    common.save_processed(df)
    return df

def load(df):
    print("--LOAD categories--")
    with psycopg.connect(host=host,
                         dbname=dbname,
                         user=user,
                         password=password,
                         port=port) as conn:
        with conn.cursor() as cur:
            sql = """
            CREATE TABLE categories (
            pk_category INTEGER PRIMARY KEY,
            name VARCHAR
            );
            """
            try:
                cur.execute(sql)
            except psycopg.errors.DuplicateTable as ex:
                conn.commit()
                print(ex)
                domanda = input("Do you want to replace the table? YES/NO(updates the table) ").upper()
                if domanda == "YES":
                    sql_delete ="""DROP TABLE categories CASCADE"""
                    cur.execute(sql_delete)
                    conn.commit()
                    print("Recreating the categories table")
                    cur.execute(sql)
            sql = """
            INSERT INTO categories (
            pk_category, name)
            VALUES ( %s, %s) 
            ON CONFLICT (pk_category) 
            DO UPDATE SET name = EXCLUDED.name
            """
            common.caricamento_barra(df, cur, sql)
            conn.commit()




if __name__ == "__main__":
    extract()

