import pandas as pd
import numpy as np

# Cargar datos
customers   = pd.read_csv('data/customers.csv')
orders      = pd.read_csv('data/orders.csv')
order_items = pd.read_csv('data/order_items.csv')
returns     = pd.read_csv('data/returns.csv')

# Fechas
orders['order_date'] = pd.to_datetime(orders['order_date'], dayfirst=True)

# Solo órdenes entregadas
delivered = orders[orders['order_status'] == 'Delivered'].copy()

# ── CLV por cliente ──
clv = delivered.groupby('customer_id').agg(
    total_revenue  = ('final_amount', 'sum'),
    total_orders   = ('order_id', 'nunique'),
    first_purchase = ('order_date', 'min'),
    last_purchase  = ('order_date', 'max')
).reset_index()

# Días activo como cliente
clv['days_active'] = (clv['last_purchase'] - clv['first_purchase']).dt.days + 1
clv['avg_order_value'] = (clv['total_revenue'] / clv['total_orders']).round(2)
clv['purchase_frequency'] = clv['total_orders']

# CLV simple = revenue total (dataset histórico completo)
clv['clv'] = clv['total_revenue'].round(2)

# ── Unir con canal de adquisición ──
clv = clv.merge(customers[['customer_id', 'acquisition_channel',
                             'gender', 'age_group', 'city', 'state']], on='customer_id')

print("=== CLV GENERAL ===")
print(f"Clientes con compras: {len(clv)}")
print(f"CLV promedio: ₹{clv['clv'].mean():.2f}")
print(f"CLV mediana:  ₹{clv['clv'].median():.2f}")
print(f"CLV máximo:   ₹{clv['clv'].max():.2f}")

print("\n=== CLV POR CANAL DE ADQUISICIÓN ===")
channel_clv = clv.groupby('acquisition_channel').agg(
    customers     = ('customer_id', 'count'),
    avg_clv       = ('clv', 'mean'),
    median_clv    = ('clv', 'median'),
    avg_orders    = ('total_orders', 'mean'),
    avg_order_val = ('avg_order_value', 'mean'),
    total_revenue = ('clv', 'sum')
).round(2).sort_values('avg_clv', ascending=False)
print(channel_clv.to_string())

print("\n=== CLV POR GRUPO DE EDAD ===")
age_clv = clv.groupby('age_group')['clv'].agg(['mean','median','count']).round(2)
print(age_clv.sort_values('mean', ascending=False).to_string())

print("\n=== CLV POR GÉNERO ===")
gender_clv = clv.groupby('gender')['clv'].agg(['mean','median','count']).round(2)
print(gender_clv.to_string())

# Guardar
clv.to_csv('data/clv.csv', index=False)
channel_clv.reset_index().to_csv('data/channel_stats.csv', index=False)
print("\nArchivos guardados.")