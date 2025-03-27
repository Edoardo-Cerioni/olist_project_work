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


def extract():
    print("--EXTRACT sellers--")
    csv_file_path = filedialog.askopenfilename(
        title="Select csv file (.csv)",
        filetypes=((" Files", "*.csv"), ("All Files", "*.*"))
    )
    df = pd.read_csv(csv_file_path)
    return df

def transform(df):
    print("--TRANSFORM sellers--")
    df = common.dropduplicates(df)
    df = common.checkNull(df, ["seller_id"])
    common.save_processed(df)
    return df

def load(df):
    print("--LOAD sellers--")

    df["last_updated"] = datetime.datetime.now().isoformat(sep=" ", timespec="seconds")

    with psycopg.connect(host=host, dbname=dbname, user=user, password=password, port=port) as conn:
        with conn.cursor() as cur:
            sql = """
                        CREATE TABLE sellers (
                        pk_seller VARCHAR PRIMARY KEY,
                        region VARCHAR,
                        last_updated TIMESTAMP
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
                    sql_delete = """DROP TABLE sellers CASCADE"""
                    cur.execute(sql_delete)
                    conn.commit()
                    print("Recreating the sellers table")
                    cur.execute(sql)

            sql = """
                        INSERT INTO sellers (
                        pk_seller,
                        region,
                        last_updated)
                        VALUES (%s, %s, %s) 
                        ON CONFLICT (pk_seller)
                        DO UPDATE SET
                        region = EXCLUDED.region,
                        last_updated = EXCLUDED.last_updated;
                        """
            common.caricamento_barra(df, cur, sql)

            conn.commit()