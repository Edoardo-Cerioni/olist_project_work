import psycopg
from dotenv import load_dotenv
import os
import  src.common as common
import datetime


load_dotenv()
host = os.getenv("host")
dbname = os.getenv("dbname")
user = os.getenv("user")
password = os.getenv("password")
port = os.getenv("port")


# metodi ETL per costumers


def extract():
    print("questo è il metodo EXTRACT per costumers")
    df = common.read_file()
    return df

def transform(df):
    print("questo è il metodo TRANSFORM per costumers")
    df = common.dropduplicates(df)
    df = common.checkNull(df,["customer_id"])
    df = common.format_string(df, ["region", "city"])
    df = common.format_cap(df)
    #common.save_processed(df)
    return df

def load(df):
    print("questo è il metodo LOAD per costumers")
    df["last_updated"] = datetime.datetime.now()
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
                domanda = input("Vuoi sostituire la tabella? SI NO(aggiunge i valori della tabella a quella originale) ")
                if domanda == "SI":
                    # cancellare tabella se risponde si
                    sqldelete = """DROP TABLE customers"""
                    cur.execute(sqldelete)
                    conn.commit()
                    print("ricreo tabella costumers")
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


            sql = """
                UPDATE customers AS c1 
                SET region = c2.region
                FROM customers AS c2
                WHERE c1.cap = c2.cap
                AND c1.cap <> 'NaN'
                AND c2.cap <> 'NaN'
                AND c1.region = 'NaN'
                AND c2.region <> 'NaN'
                RETURNING *
                ; """

            cur.execute(sql)

            print("visualizzazione record con regione aggiornata")
            for record in cur:
                print (record)

            sql = """
                            UPDATE customers AS c1 
                            SET city = c2.city
                            FROM customers AS c2
                            WHERE c1.cap = c2.cap
                            AND c1.cap <> 'NaN'
                            AND c2.cap <> 'NaN'
                            AND c1.city = 'NaN'
                            AND c2.city <> 'NaN'
                            RETURNING *
                            ; """

            cur.execute(sql)

            print("visualizzazione record con città aggiornata")
            for record in cur:
                print(record)


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
