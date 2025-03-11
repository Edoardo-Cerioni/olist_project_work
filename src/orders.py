# metodi ETL per products

def extract():
    print("questo è il metodo EXTRACT per products")

def transform():
    print("questo è il metodo TRANSFORM per orders")

def load():
    print("questo è il metodo LOAD per orders")

def main():
    print("questo è il metodo Main per orders")
    extract()
    transform()
    load()

#per usare questo file come fosse un modulo
if __name__ == "__main__":
    main()