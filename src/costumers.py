import psycopg
from dotenv import load_dotenv
import os
from src.common import readFile, caricamento_percentuale

load_dotenv()
host = os.getenv("host")
dbname = os.getenv("dbname")
user = os.getenv("user")
password = os.getenv("password")
port = os.getenv("port")


# metodi ETL per costumers


def extract():
    print("questo è il metodo EXTRACT per costumers")
    df = readFile()
    return df

def transform(df):
    print("questo è il metodo TRANSFORM per costumers")
    return df

def load(df):
    print("questo è il metodo LOAD per costumers")
    #print(df) debug
    with psycopg.connect(host=host, dbname=dbname, user=user, password=password, port=port) as conn:
        with conn.cursor() as cur:
            sql = """
            CREATE TABLE IF NOT EXISTS customers (
            pk_customer VARCHAR PRIMARY KEY,
            region VARCHAR,
            city VARCHAR,
            cap VARCHAR
            );
            """
            cur.execute(sql)
            sql = """
            INSERT INTO customers
            (pk_customer, region, city, cap) 
            VALUES (%s, %s, %s, %s);
            """
            caricamento_percentuale(df, cur, sql)


            conn.commit()


def main():
    print("questo è il metodo Main")
    df = extract()
    df = transform(df)
    load(df)

#per usare questo file come fosse un modulo
#i metodi usati vanno importati sopra
if __name__ == "__main__":
    main()
