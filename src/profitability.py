import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec

product_stats = pd.read_csv('data/product_profitability.csv')
delivered     = pd.read_csv('data/delivered_items.csv')
products      = pd.read_csv('data/products.csv')

print(product_stats['category'].unique())

fig = plt.figure(figsize=(20, 14))
fig.patch.set_facecolor('#0f1117')
gs = gridspec.GridSpec(2, 3, figure=fig, hspace=0.45, wspace=0.35)

TEXT  = '#e0e0e0'
GRID  = '#2a2a3e'
COLORS = ['#00d4ff','#51cf66','#ff6b6b','#fcc419','#a78bfa']

def style_ax(ax):
    ax.set_facecolor('#1a1a2e')
    ax.tick_params(colors=TEXT, labelsize=8)
    ax.xaxis.label.set_color(TEXT)
    ax.yaxis.label.set_color(TEXT)
    ax.title.set_color(TEXT)
    for spine in ax.spines.values():
        spine.set_edgecolor(GRID)
    ax.grid(color=GRID, linestyle='--', linewidth=0.5)

# 1. Profitability score por producto (top 15)
ax1 = fig.add_subplot(gs[0, :2])
style_ax(ax1)
top15 = product_stats.nlargest(15, 'profitability_score').sort_values('profitability_score')
colors_bar = ['#51cf66' if s >= 74 else '#fcc419' if s >= 72 else '#ff6b6b'
              for s in top15['profitability_score']]
names = [n[:30] for n in top15['product_name']]
ax1.barh(names, top15['profitability_score'], color=colors_bar, edgecolor='none', height=0.65)
ax1.set_title('Profitability Score por Producto', fontweight='bold')
ax1.set_xlabel('Score (margen + descuento + devoluciones)')
ax1.axvline(x=product_stats['profitability_score'].mean(), color='#fcc419',
            linestyle='--', lw=1.5, label=f"Promedio: {product_stats['profitability_score'].mean():.1f}")
ax1.legend(fontsize=8, labelcolor=TEXT, facecolor='#1a1a2e', edgecolor=GRID)
for i, (val, name) in enumerate(zip(top15['profitability_score'], names)):
    ax1.text(val + 0.1, i, f'{val:.1f}', va='center', color=TEXT, fontsize=8)

# 2. Margen vs Devoluciones (scatter)
ax2 = fig.add_subplot(gs[0, 2])
style_ax(ax2)
cats = product_stats['category'].unique()
palette = ['#00d4ff','#51cf66','#ff6b6b','#fcc419','#a78bfa','#f06595','#74c0fc','#63e6be','#ff922b']
cat_colors = dict(zip(cats, palette[:len(cats)]))
for cat in cats:
    mask = product_stats['category'] == cat
    ax2.scatter(product_stats.loc[mask, 'return_rate'],
                product_stats.loc[mask, 'avg_margin_pct'],
                c=cat_colors[cat], s=80, alpha=0.8, label=cat, edgecolors='none')
ax2.set_title('Margen vs Tasa de Devolución', fontweight='bold')
ax2.set_xlabel('Tasa de devolución (%)')
ax2.set_ylabel('Margen promedio (%)')
ax2.legend(fontsize=7, labelcolor=TEXT, facecolor='#1a1a2e', edgecolor=GRID)

# 3. Revenue vs Margen por categoría
ax3 = fig.add_subplot(gs[1, 0])
style_ax(ax3)
cat_stats = product_stats.groupby('category').agg(
    total_revenue=('total_revenue','sum'),
    avg_margin=('avg_margin_pct','mean')
).reset_index().sort_values('total_revenue', ascending=True)
bars = ax3.barh(cat_stats['category'], cat_stats['total_revenue'],
                color=[cat_colors.get(c,'#888') for c in cat_stats['category']],
                edgecolor='none', height=0.5)
ax3.set_title('Revenue Total por Categoría', fontweight='bold')
ax3.set_xlabel('Revenue (INR)')
ax3.xaxis.set_major_formatter(plt.FuncFormatter(lambda x,_: f'₹{x/1000:.0f}K'))

# 4. Descuento promedio por categoría
ax4 = fig.add_subplot(gs[1, 1])
style_ax(ax4)
cat_disc = product_stats.groupby('category')['avg_discount'].mean().sort_values(ascending=True)
ax4.barh(cat_disc.index, cat_disc.values,
         color=[cat_colors.get(c,'#888') for c in cat_disc.index],
         edgecolor='none', height=0.5)
ax4.set_title('Descuento Promedio por Categoría (%)', fontweight='bold')
ax4.set_xlabel('Descuento %')
for i, val in enumerate(cat_disc.values):
    ax4.text(val + 0.1, i, f'{val:.1f}%', va='center', color=TEXT, fontsize=8)

# 5. Rating vs Profitability score
ax5 = fig.add_subplot(gs[1, 2])
style_ax(ax5)
ps_with_rating = product_stats.dropna(subset=['avg_rating'])
ax5.scatter(ps_with_rating['avg_rating'],
            ps_with_rating['profitability_score'],
            c='#a78bfa', s=80, alpha=0.8, edgecolors='none')
z = np.polyfit(ps_with_rating['avg_rating'], ps_with_rating['profitability_score'], 1)
p = np.poly1d(z)
x_line = np.linspace(ps_with_rating['avg_rating'].min(), ps_with_rating['avg_rating'].max(), 100)
ax5.plot(x_line, p(x_line), color='#fcc419', lw=1.5, linestyle='--')
ax5.set_title('Rating vs Profitability Score', fontweight='bold')
ax5.set_xlabel('Rating promedio')
ax5.set_ylabel('Profitability Score')

fig.text(0.5, 0.97, 'Skincare E-Commerce — Análisis de Rentabilidad',
         ha='center', fontsize=16, fontweight='bold', color=TEXT)
fig.text(0.5, 0.94, '28 productos  |  1,671 items entregados  |  Score = Margen · Descuento · Devoluciones',
         ha='center', fontsize=9, color='#888888')

plt.savefig('reports/profitability.png', dpi=150, bbox_inches='tight',
            facecolor=fig.get_facecolor())
plt.show()
print("Dashboard guardado en reports/profitability.png")