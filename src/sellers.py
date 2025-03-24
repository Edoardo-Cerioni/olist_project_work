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


def extract():
    print("questo è il metodo EXTRACT per sellers")
    df = common.read_file()
    return df

def transform(df):
    print("questo è il metodo TRANSFORM per sellers")
    df = common.dropduplicates(df)
    df = common.checkNull(df,["seller_id"])
    common.save_processed(df)
    return df

def load(df):
    print("questo è il metodo LOAD per sellers")

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
                domanda = input(
                    "Vuoi sostituire la tabella? SI NO(aggiunge i valori della tabella a quella originale) ").strip().upper()
                if domanda == "SI":
                    # cancellare tabella se risponde si
                    sql_delete = """DROP TABLE sellers CASCADE"""
                    cur.execute(sql_delete)
                    conn.commit()
                    print("ricreo tabella sellers")
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