import datetime
import pandas as pd
import src.common as common
import os
import psycopg
from dotenv import load_dotenv

load_dotenv()
host = os.getenv("host")
dbname = os.getenv("dbname")
user = os.getenv("user")
password = os.getenv("password")
port = os.getenv("port")

def extract():
    df = common.read_file()
    print(df.dtypes)
    print(f"Valori nulli per colonna:\n {df.isnull().sum()} \n")
    return df

def transform(df):
    df = common.dropduplicates(df)
    return df

def load(df):
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
                domanda = input("Desideri cancellare questa tabella? SI/NO").upper()
                if domanda == "SI":
                    sql_delete ="""DROP TABLE categories"""
                    cur.execute(sql_delete)
                    conn.commit()
                    print("Ricreando la tabella categories")
                    cur.execute(sql)
            sql = """
            INSERT INTO categories (
            pk_category, name)
            VALUES ( %s, %s)
            """
            common.caricamento_barra(df, cur, sql)
            conn.commit()

def dump():
    with psycopg.connect(host=host, dbname=dbname, user=user, password=password, port=port) as conn:
        with conn.cursor() as cur:
            sql = "SELECT DISTINCT macro_category_id, macro_category_name_english FROM categories"
            cur.execute(sql)
            df = pd.DataFrame(cur, columns= ["pk_category", "name"])
            df.to_csv("../data/processed/categories_processed.csv", index = False)


if __name__ == "__main__":
    extract()

