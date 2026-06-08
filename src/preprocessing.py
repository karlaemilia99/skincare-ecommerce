import pandas as pd
import numpy as np

# Cargar tablas
customers   = pd.read_csv('data/customers.csv')
products    = pd.read_csv('data/products.csv')
orders      = pd.read_csv('data/orders.csv')
order_items = pd.read_csv('data/order_items.csv')
returns     = pd.read_csv('data/returns.csv')
reviews     = pd.read_csv('data/reviews.csv')

# Convertir fechas
orders['order_date']     = pd.to_datetime(orders['order_date'], dayfirst=True)
products['launch_date']  = pd.to_datetime(products['launch_date'], dayfirst=True)
returns['return_date']   = pd.to_datetime(returns['return_date'], dayfirst=True)
reviews['review_date']   = pd.to_datetime(reviews['review_date'], dayfirst=True)

# ── Tabla maestra de rentabilidad por producto ──
# Margen bruto base
products['gross_margin']    = products['mrp'] - products['cost_price']
products['margin_pct']      = (products['gross_margin'] / products['mrp'] * 100).round(2)

# Unir order_items con products
items_products = order_items.merge(products[['product_id','product_name','category',
                                              'skin_type','mrp','cost_price',
                                              'gross_margin','margin_pct']], on='product_id')

# Revenue real después de descuento
items_products['real_revenue'] = items_products['item_total']
items_products['real_cost']    = items_products['cost_price'] * items_products['quantity']
items_products['real_margin']  = items_products['real_revenue'] - items_products['real_cost']
items_products['real_margin_pct'] = (items_products['real_margin'] / items_products['real_revenue'] * 100).round(2)

# Unir con orders para traer order_status
items_products = items_products.merge(
    orders[['order_id','order_status','order_date','sales_channel']], on='order_id'
)

# Solo órdenes entregadas
delivered = items_products[items_products['order_status'] == 'Delivered'].copy()

print(f"Items entregados: {len(delivered)}")

# ── Métricas por producto ──
product_stats = delivered.groupby(['product_id','product_name','category','skin_type']).agg(
    units_sold    = ('quantity', 'sum'),
    total_revenue = ('real_revenue', 'sum'),
    total_cost    = ('real_cost', 'sum'),
    total_margin  = ('real_margin', 'sum'),
    avg_discount  = ('discount_pct', 'mean'),
    orders_count  = ('order_id', 'nunique')
).reset_index()

product_stats['avg_margin_pct'] = (product_stats['total_margin'] / product_stats['total_revenue'] * 100).round(2)

# ── Tasa de devolución por producto ──
return_counts = returns.groupby('product_id').size().reset_index(name='return_count')
product_stats = product_stats.merge(return_counts, on='product_id', how='left')
product_stats['return_count'] = product_stats['return_count'].fillna(0)
product_stats['return_rate']  = (product_stats['return_count'] / product_stats['orders_count'] * 100).round(2)

# ── Rating promedio por producto ──
avg_rating = reviews.groupby('product_id')['rating'].mean().round(2).reset_index(name='avg_rating')
product_stats = product_stats.merge(avg_rating, on='product_id', how='left')

# ── Score de rentabilidad real ──
# Penaliza margen bajo, descuento alto y devoluciones altas
product_stats['profitability_score'] = (
    product_stats['avg_margin_pct'] * 0.5 +
    (100 - product_stats['avg_discount']) * 0.3 +
    (100 - product_stats['return_rate']) * 0.2
).round(2)

print("\n=== TOP 5 MÁS RENTABLES ===")
print(product_stats.nlargest(5, 'profitability_score')[
    ['product_name','avg_margin_pct','avg_discount','return_rate','profitability_score']
].to_string())

print("\n=== TOP 5 MENOS RENTABLES ===")
print(product_stats.nsmallest(5, 'profitability_score')[
    ['product_name','avg_margin_pct','avg_discount','return_rate','profitability_score']
].to_string())

# Guardar
product_stats.to_csv('data/product_profitability.csv', index=False)
delivered.to_csv('data/delivered_items.csv', index=False)
print("\nArchivos guardados.")