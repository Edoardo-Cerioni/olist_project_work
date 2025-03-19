import src.common as common

def extract():
    print("questo è il metodo EXTRACT per categories")
    df = common.read_file()
    print(df)
    print(df.info)
    print(df.nunique())
    return df

def transform():
    print("questo è il metodo TRANSFORM per categories")

def load():
    print("questo è il metodo LOAD per categories")

def main():
    print("questo è il metodo Main per categories")
    extract()
    #transform()
    #load()

#per usare questo file come fosse un modulo
if __name__ == "__main__":
    main()