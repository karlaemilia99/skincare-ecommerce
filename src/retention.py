import pandas as pd
import numpy as np

customers   = pd.read_csv('data/customers.csv')
orders      = pd.read_csv('data/orders.csv')
returns     = pd.read_csv('data/returns.csv')
products    = pd.read_csv('data/products.csv')
order_items = pd.read_csv('data/order_items.csv')

orders['order_date']   = pd.to_datetime(orders['order_date'], dayfirst=True)
customers['signup_date'] = pd.to_datetime(customers['signup_date'], dayfirst=True)
returns['return_date'] = pd.to_datetime(returns['return_date'], dayfirst=True)

delivered = orders[orders['order_status'] == 'Delivered'].copy()

# ── Retención por canal ──
customer_orders = delivered.groupby('customer_id')['order_id'].nunique().reset_index()
customer_orders.columns = ['customer_id', 'order_count']
customer_orders = customer_orders.merge(
    customers[['customer_id', 'acquisition_channel']], on='customer_id'
)

customer_orders['is_repeat'] = (customer_orders['order_count'] > 1).astype(int)

retention = customer_orders.groupby('acquisition_channel').agg(
    total_customers = ('customer_id', 'count'),
    repeat_customers = ('is_repeat', 'sum'),
).reset_index()
retention['retention_rate'] = (retention['repeat_customers'] / retention['total_customers'] * 100).round(2)
retention = retention.sort_values('retention_rate', ascending=False)

print("=== RETENCIÓN POR CANAL ===")
print(retention.to_string())

# ── Cohortes por mes de primera compra ──
first_purchase = delivered.groupby('customer_id')['order_date'].min().reset_index()
first_purchase.columns = ['customer_id', 'first_purchase']
first_purchase['cohort'] = first_purchase['first_purchase'].dt.to_period('Q')

delivered_cohort = delivered.merge(first_purchase, on='customer_id')
delivered_cohort['order_quarter'] = delivered_cohort['order_date'].dt.to_period('Q')
delivered_cohort['quarters_since'] = (
    delivered_cohort['order_quarter'] - delivered_cohort['cohort']
).apply(lambda x: x.n)

cohort_size = first_purchase.groupby('cohort')['customer_id'].nunique()
cohort_retention = delivered_cohort.groupby(
    ['cohort', 'quarters_since']
)['customer_id'].nunique().reset_index()
cohort_retention['cohort_size'] = cohort_retention['cohort'].map(cohort_size)
cohort_retention['retention_pct'] = (
    cohort_retention['customer_id'] / cohort_retention['cohort_size'] * 100
).round(2)

print("\n=== COHORTES TRIMESTRALES ===")
cohort_pivot = cohort_retention.pivot(
    index='cohort', columns='quarters_since', values='retention_pct'
).fillna(0).round(1)
print(cohort_pivot.to_string())

# ── Análisis de devoluciones ──
returns_full = returns.merge(
    order_items[['order_id','product_id']], on=['order_id','product_id'], how='left'
).merge(
    products[['product_id','category','skin_type']], on='product_id', how='left'
).merge(
    orders[['order_id','customer_id','sales_channel']], on='order_id', how='left'
).merge(
    customers[['customer_id','acquisition_channel']], on='customer_id', how='left'
)

print("\n=== MOTIVOS DE DEVOLUCIÓN ===")
print(returns['return_reason'].value_counts())

print("\n=== DEVOLUCIONES POR CATEGORÍA ===")
print(returns_full['category'].value_counts())

print("\n=== DEVOLUCIONES POR CANAL DE VENTA ===")
print(returns_full['sales_channel'].value_counts())

print("\n=== DEVOLUCIONES POR TIPO DE PIEL ===")
print(returns_full['skin_type'].value_counts())

# Guardar
retention.to_csv('data/retention.csv', index=False)
cohort_retention.to_csv('data/cohort_retention.csv', index=False)
returns_full.to_csv('data/returns_full.csv', index=False)
print("\nArchivos guardados.")