import psycopg
from dotenv import load_dotenv
import os
import  src.common as common
import datetime
from tkinter import filedialog
import pandas as pd

load_dotenv()
host = os.getenv("host")
dbname = os.getenv("dbname")
user = os.getenv("user")
password = os.getenv("password")
port = os.getenv("port")


# metodi ETL per costumers


def extract():
    print("--EXTRACT customers--")
#   df = common.read_file()
    csv_file_path = filedialog.askopenfilename(
        title="Select csv file (.csv)",
        filetypes=((" Files", "*.csv"), ("All Files", "*.*"))
    )
    df = pd.read_csv(csv_file_path)
    return df

def transform(df):
    print("--TRANSFORM customers--")
    df = common.dropduplicates(df)
    df = common.checkNull(df, ["customer_id"])
    df = common.format_string(df, ["region", "city"])
    df = common.format_cap(df)
    common.save_processed(df)
    return df

def load(df):
    print("--LOAD customers--")
    df["last_updated"] = datetime.datetime.now().isoformat(sep=" ", timespec="seconds")
    with psycopg.connect(host=host, dbname=dbname, user=user, password=password, port=port) as conn:
        with conn.cursor() as cur:
            sql = """
            CREATE TABLE customers (
            pk_customer VARCHAR PRIMARY KEY,
            region VARCHAR,
            city VARCHAR,
            cap VARCHAR,
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
                    sqldelete = """DROP TABLE customers CASCADE"""
                    cur.execute(sqldelete)
                    conn.commit()
                    print("Recreating the customers table")
                    cur.execute(sql)

            sql = """
            INSERT INTO customers
            (pk_customer, region, city, cap, last_updated)
            VALUES (%s, %s, %s, %s, %s) ON CONFLICT (pk_customer) DO UPDATE SET 
            (region, city, cap, last_updated) = (EXCLUDED.region, EXCLUDED.city, EXCLUDED.cap, EXCLUDED.last_updated)
            """
            common.caricamento_barra(df, cur, sql)


            conn.commit()

def complete_city_region():
    with psycopg.connect(host=host, dbname=dbname, user=user, password=password, port=port) as conn:
        with conn.cursor() as cur:


            sql = f"""
                UPDATE customers AS c1 
                SET region = c2.region,
                last_updated = '{datetime.datetime.now().isoformat(sep=" ", timespec="seconds")}'
                FROM customers AS c2
                WHERE c1.cap = c2.cap
                AND c1.cap <> 'NaN'
                AND c2.cap <> 'NaN'
                AND c1.region = 'NaN'
                AND c2.region <> 'NaN'
                RETURNING *
                ; """

            cur.execute(sql)

            print("The region records are updated")
            for record in cur:
                print (record)

            sql = f"""
                 UPDATE customers AS c1 
                 SET city = c2.city,
                 last_updated = '{datetime.datetime.now().isoformat(sep=" ", timespec="seconds")}'
                 FROM customers AS c2
                 WHERE c1.cap = c2.cap
                 AND c1.cap <> 'NaN'
                 AND c2.cap <> 'NaN'
                 AND c1.city = 'NaN'
                 AND c2.city <> 'NaN'
                 RETURNING *
                 ; """

            cur.execute(sql)

            print("The city records are updated")
            for record in cur:
                print(record)

            conn.commit()


#DEBUG
def main():
    print("questo è il metodo Main")
    df = extract()
    print("file di partenza")
    print(df)
    df = transform(df)
    print("file formattato")
    print(df, end="\n\n")
    load(df)

#per usare questo file come fosse un modulo
#i metodi usati vanno importati sopra
if __name__ == "__main__":
    main()
