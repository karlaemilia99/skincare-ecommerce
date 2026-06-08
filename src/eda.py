import pandas as pd

# Cargar todas las tablas
customers   = pd.read_csv('data/customers.csv')
products    = pd.read_csv('data/products.csv')
orders      = pd.read_csv('data/orders.csv')
order_items = pd.read_csv('data/order_items.csv')
returns     = pd.read_csv('data/returns.csv')
reviews     = pd.read_csv('data/reviews.csv')

tables = {
    'customers':   customers,
    'products':    products,
    'orders':      orders,
    'order_items': order_items,
    'returns':     returns,
    'reviews':     reviews
}

for name, df in tables.items():
    print(f"\n{'='*40}")
    print(f"TABLA: {name.upper()}")
    print(f"Shape: {df.shape}")
    print(f"Columnas: {df.columns.tolist()}")
    print(f"Nulos:\n{df.isnull().sum()[df.isnull().sum() > 0]}")
    print(df.head(2).to_string())