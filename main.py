import src.costumers as costumers
import src.products as products
import src.orders as order

if __name__ == "__main__":
    df_costumers = costumers.extract()
    df_costumers = costumers.transform(df_costumers)
    costumers.load(df_costumers)
    products.extract()
    products.transform()
    products.load()