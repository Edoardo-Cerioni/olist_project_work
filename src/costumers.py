# metodi ETL per costumers

def extract():
    print("questo è il metodo EXTRACT")

def transform():
    print("questo è il metodo TRANSFORM")

def load():
    print("questo è il metodo LOAD")

def main():
    print("questo è il metodo Main")
    extract()
    transform()
    load()

#per usare questo file come fosse un modulo
#i metodi usati vanno importati sopra
if __name__ == "__main__":
    main()
