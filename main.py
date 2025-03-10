import src.costumers as costumers
import src.products as products

if __name__ == "__main__":
    costumers.extract()
    costumers.transform()
    costumers.load()
    products.extract()
    products.transform()
    products.load()