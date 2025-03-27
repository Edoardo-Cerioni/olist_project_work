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


# metodi ETL per orders

def extract():
    print("--EXTRACT orders--")
    csv_file_path = filedialog.askopenfilename(
        title="Select csv file (.csv)",
        filetypes=((" Files", "*.csv"), ("All Files", "*.*"))
    )
    df = pd.read_csv(csv_file_path)
    return df

def transform(df):
    print("--TRANSFORM orders--")
    df = common.dropduplicates(df)
    df = common.checkNull(df,["order_id", "customer_id"])
    df = common.format_string(df, ["order_status"])
    common.save_processed(df)
    return df

def load(df):
    print("--LOAD orders--")
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
                domanda = input("Do you want to replace the table? YES/NO(updates the table) ").strip().upper()
                if domanda == "YES":
                    # cancellare tabella se risponde si
                    sql_delete = """DROP TABLE orders CASCADE"""
                    cur.execute(sql_delete)
                    conn.commit()
                    print("Recreating the orders table")
                    cur.execute(sql)

            sql = """
            INSERT INTO orders ( 
            pk_order, fk_customer, status, purchase_timestamp, delivered_timestamp, estimated_date, last_updated
            )
            VALUES (%s, %s, %s, %s, %s, %s, %s)
            ON CONFLICT (pk_order) 
            DO UPDATE SET 
            fk_customer = EXCLUDED.fk_customer,
            status = EXCLUDED.status,
            purchase_timestamp = EXCLUDED.purchase_timestamp,
            delivered_timestamp = EXCLUDED.delivered_timestamp,
            estimated_date = EXCLUDED.estimated_date,
            last_updated = EXCLUDED.last_updated;
            """
            common.caricamento_barra(df, cur, sql)

            conn.commit()

            sql = """UPDATE orders SET delivered_timestamp = null 
            WHERE EXTRACT (YEAR FROM delivered_timestamp) = 48113;"""

            cur.execute(sql)
            conn.commit()



