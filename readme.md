## TITOLO
# esempio

* elenco
* puntato

**Grassetto**
_Corsivo_
qui tutte le istruzioni 

**Tabelle**

_costumers_
- pk_customer VARCHAR   
- region VARCHAR
- city VARCHAR
- cap VARCHAR

_categories_
- pk_categories SERIAL
- name (in inglese) VARCHAR

_products_
- pk_product VARCHAR
- fk_category INTEGER
- name_length INTEGER (errore ortografico)
- description_length INTEGER
- imgs_qty INTEGER

_orders_
- pk_order VARCHAR
- fk_costumer VARCHAR
- status VARCHAR
- purchase_timestamp TIMESTAMP
- delivered_timestamp TIMESTAMP
- estimated_date DATE

_sellers_
- pk_seller VARCHAR
- region VARCHAR

_orders_products_
- pk_order_product SERIAL
- fk_order VARCHAR
- fk_product VARCHAR
- fk_seller VARCHAR
- price FLOAT
- freight (costo spedizione) FLOAT

## Todo opzionale

- colonna che tracci la data di inserimento dei dati
- check sulle 20 regioni ammesse


