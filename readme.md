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

## Todo
19-20 marzo
- etl dei vari file csv - riguardasi bene insieme le varie colonne e categorie
prendere come riferimento le categorie di categories.load.py e creare un metodo tipo quello che abbiamo usato per sistemare region con il cap

- pensare a qualche idea carina da implementare eventualmente


- cosa chiedere a Barbara? 
dove reperire esempi di lavoro ben fatto?
quali grafici è più opportuno usare?


21 marzo
- postsgreSQL

22-23-24 marzo
- jupyter(forse)
- powerBI
Definisci le relazioni tra le tabelle
Customers ↔ Orders (pk_customer → fk_customer)
Orders ↔ Orders_Products (pk_order → fk_order)
Orders_Products ↔ Products (fk_product → pk_product)
Orders_Products ↔ Sellers (fk_seller → pk_seller)
Products ↔ Categories (fk_category → pk_category)

METRICHE PRINCIPALI
## Analisi delle vendite

Fatturato totale: SUM(orders_products.price)
Costo medio di spedizione: AVG(orders_products.freight)
Numero ordini per stato: COUNT(orders.status)

## Prodotti e Categorie

Numero di prodotti per categoria
Media lunghezza nome/descrizione prodotti
Numero di immagini per prodotto (imgs_qty)

## Analisi Geografica

Ordini per regione/città
Vendite per regione dei seller

## Performance di Consegna

Tempo medio di consegna: DATEDIFF(delivered_timestamp, purchase_timestamp, DAY)
Percentuale di ritardi: confronto tra estimated_date e delivered_timestamp


25 marzo
- organizzare presentazione
Layout consigliato da chatgpt
Mappa interattiva: ordini per regione/città.
Grafico a barre: categorie più vendute.
KPI cards: ricavi totali, numero ordini, % ritardi consegne.
Timeline interattiva: numero di ordini nel tempo.
Tabella dettagliata: informazioni su ordini e venditori.



## IDEE
- creare un metodo dinamico in grado di sistemare e aggiornare tutte le categorie seguendo modello amazon ecc
- menu di ricerca dei prodotti e delle categorie


