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


# metodi ETL per orders

def extract():
    print("questo è il metodo EXTRACT per orders")
    df = common.read_file()
    return df

def transform(df):
    print("questo è il metodo TRANSFORM per orders")
    df = common.dropduplicates(df)
    df = common.checkNull(df,["order_id", "customer_id"])
    df = common.format_string(df, ["order_status"])
    common.save_processed(df)
    return df

def load(df):
    print("questo è il metodo LOAD per orders")
    df["last_updated"] = datetime.datetime.now().isoformat(sep=" ", timespec="seconds")
    df["order_purchase_timestamp"] = pd.to_datetime(df["order_purchase_timestamp"])
    df["order_delivered_customer_date"] = pd.to_datetime(df["order_delivered_customer_date"])
    with psycopg.connect(host=host, dbname=dbname, user=user, password=password, port=port) as conn:
        with conn.cursor() as cur:



            sql = """
            CREATE TABLE orders (
            pk_order VARCHAR PRIMARY KEY,
            fk_customer VARCHAR,
            status VARCHAR,
            purchase_timestamp TIMESTAMP,
            delivered_timestamp TIMESTAMP,
            estimated_date DATE,
            last_updated TIMESTAMP,
            FOREIGN KEY (fk_customer)
            REFERENCES customers (pk_customer)
            );
            """

            try:
                cur.execute(sql)
            except psycopg.errors.DuplicateTable as ex:
                conn.commit()
                print(ex)
                domanda = input("Vuoi sostituire la tabella? SI NO(aggiunge i valori della tabella a quella originale) ").strip().upper()
                if domanda == "SI":
                    # cancellare tabella se risponde si
                    sql_delete = """DROP TABLE orders"""
                    cur.execute(sql_delete)
                    conn.commit()
                    print("ricreo tabella orders")
                    cur.execute(sql)

            sql = """
            INSERT INTO orders ( 
            pk_order, fk_customer, status, purchase_timestamp, delivered_timestamp, estimated_date, last_updated
            )
            VALUES (%s, %s, %s, %s, %s, %s, %s) ON CONFLICT (pk_order) DO NOTHING
            """
            common.caricamento_barra(df, cur, sql)


            conn.commit()
