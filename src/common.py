import os

import numpy as np
import pandas as pd
import datetime

import psycopg
from dotenv import load_dotenv

load_dotenv()
host = os.getenv("host")
dbname = os.getenv("dbname")
user = os.getenv("user")
password = os.getenv("password")
port = os.getenv("port")



def read_file():
    isvalid = False
    df = pd.DataFrame()
    while not isvalid:
        path = input("Enter the file path:\n").strip()
        try:
            path_list = path.split(".")

            if path_list[-1] == "csv" or path_list[-1] == "txt":
                df = pd.read_csv(path)
            elif path_list[-1] == "xlsx" or path_list[-1] == "xls":
                df = pd.read_excel(path)
            else:
                df = pd.read_json(path)

        #puoi usare una lista che è + DRY!
        except FileNotFoundError as ex:
            print(ex)
        except OSError as ex:
            print(ex)
        else:
            print("Path entered correctly: proceeding with file reading")
            isvalid = True
    else:
        return df

def caricamento_percentuale(df, cur, sql):
    # eseguo la query per caricare i dati (il risultato del caricamento è in percentuale)
    print(f"Loading... {str(len(df))} records")
    perc_int = 0
    for index, row in df.iterrows():
        perc = float("%.2f" % ((index + 1) / len(df) * 100))
        if perc >= perc_int:
            print(f"{round(perc)}% Completed")
            perc_int += 5
        cur.execute(sql, row.to_list())

def caricamento_barra(df,cur,sql):
    print(f"Loading... \n{str(len(df))} records")
    Tmax = 50
    if len(df)/2 < 50:
        Tmax = len(df)
    print("┌" + "─" * Tmax + "┐")
    print("│",end="")
    perc_int = 2
    for index, row in df.iterrows():
        perc = float("%.2f" % ((index + 1) / len(df) * 100))
        if perc >= perc_int:
            print("\r│" + "█" * (perc_int//2) + str(int(perc)) + "%",end="")
            #print(perc,end="")
            perc_int += 2
        cur.execute(sql, row.to_list())
    print("\r│" + "█" * Tmax + "│ 100% Completed!")
    print("└" + "─" * Tmax + "┘")

def format_cap(df):
    #if "cap" in df.columns:
    df["cap"] = df["cap"].apply(lambda cap: str(int(cap)).zfill(5) if cap == cap else cap)
    return df

def format_string(df, cols):
    #print(df[cols])
    for col in cols:
        df[col] = df[col].str.strip()
        df[col] = df[col].str.replace("[0-9]", "",regex=True)
        df[col] = df[col].str.replace("[\\[\\]$&+:;=?@#|<>.^*(/_)%!]", "", regex=True)
        df[col] = df[col].str.replace(r"\s+", " ", regex=True)
    return df

def dropduplicates (df):
    #print(df.duplicated().sum())
    df.drop_duplicates(inplace = True)
    return df

def checkNull(df, subset=""):
    print(f"Null values for column:\n{df.isnull().sum()}\n")
    subset = df.columns.tolist()[0] if not subset else subset
    df.dropna(subset=subset, inplace=True, ignore_index=True)
    #df = fillNull(df)
    #print(df)
    return df

def fillNull(df):
    df.fillna(value="nd", axis=0, inplace=True)
    return df

def save_processed(df):
    print("Saving the changes to a CSV file in the 'processed' folder")
    name = input("What's the name of the file?").strip().lower()
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    file_name = name + "_processed" + "_datetime" + timestamp + ".csv"
    print(f"Creating the file {file_name}", end="\n\n")
    if __name__ == "__main__":
        directory_name = "../data/processed/"
    else:
        directory_name = "data/processed/"
    df.to_csv(directory_name + file_name, index = False)

def format_region():
    nome_tabella = input("Enter the name of the table to modify ").strip().lower()
    with psycopg.connect(host=host, dbname=dbname, user=user, password=password, port=port) as conn:
        with conn.cursor() as cur:


            sql = f"""
                 UPDATE {nome_tabella} 
                 SET region = 'Emilia-Romagna'
                 WHERE region = 'Emilia Romagna'
                 RETURNING *
                 """
            cur.execute(sql)
            #print("Record con regione aggiornata \n")
            #for record in cur:
                #print(record)

            sql = f"""
                 UPDATE {nome_tabella} 
                 SET region = 'Trentino-Alto Adige'
                 WHERE region = 'Trentino Alto Adige'
                 RETURNING *
                 """
            cur.execute(sql)
            #print("Record con regione aggiornata \n")
            #for record in cur:
                #print(record)

            sql = f"""
                UPDATE {nome_tabella} 
                SET region = 'Friuli-Venezia Giulia'
                WHERE region = 'Friuli Venezia Giulia'
                RETURNING *
                """
            cur.execute(sql)
            print("Records updated \n")
            #for record in cur:
                #print(record)








#DEBUG
if __name__ == "__main__":
    df = read_file()
    #df = format_string(df, ["region", "city"])
    #print("file di partenza")
    #print(df)
    #format_cap(df)
    #print("dati con CAP formattato ")
    #print (df)
    #checkNull(df) #modifica di default la prima colonna a meno che non gli si da la lista es [customers_id]
    #save_processed(df)

