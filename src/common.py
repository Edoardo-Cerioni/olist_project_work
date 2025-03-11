import pandas as pd

def readFile():
    isvalid = False
    df = pd.DataFrame()
    while not isvalid:
        path_file = input("inserire il path del file: ")
        try:
            df = pd.read_csv(path_file)
        except FileNotFoundError as ex:
            print(ex)
        except OSError as ex:
            print(ex)
        else:
            isvalid = True
            print("\n\n file estratto con successo\n\n")
    else:
        return df

def caricamento_percentuale(df, cur, sql):
    # eseguo la query per caricare i dati (il risultato del caricamento è in percentuale)
    print(f"Caricamento in corso... {str(len(df))} righe da inserire.")
    perc_int = 0
    for index, row in df.iterrows():
        perc = float("%.2f" % ((index + 1) / len(df) * 100))
        if perc >= perc_int:
            print(f"{round(perc)}% Completato")
            perc_int += 5
        cur.execute(sql, row.to_list())

if __name__ == "__main__":
    readFile()