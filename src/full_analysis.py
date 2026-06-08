import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import seaborn as sns

# Cargar datos procesados
clv           = pd.read_csv('data/clv.csv')
channel_stats = pd.read_csv('data/channel_stats.csv')
retention     = pd.read_csv('data/retention.csv')
cohort        = pd.read_csv('data/cohort_retention.csv')
returns_full  = pd.read_csv('data/returns_full.csv')

fig = plt.figure(figsize=(20, 16))
fig.patch.set_facecolor('#0f1117')
gs = gridspec.GridSpec(3, 3, figure=fig, hspace=0.5, wspace=0.35)

TEXT  = '#e0e0e0'
GRID  = '#2a2a3e'
COLORS = ['#a855f7','#51cf66','#ff6b6b','#fcc419','#00d4ff']

def style_ax(ax):
    ax.set_facecolor('#1a1a2e')
    ax.tick_params(colors=TEXT, labelsize=8)
    ax.xaxis.label.set_color(TEXT)
    ax.yaxis.label.set_color(TEXT)
    ax.title.set_color(TEXT)
    for spine in ax.spines.values():
        spine.set_edgecolor(GRID)
    ax.grid(color=GRID, linestyle='--', linewidth=0.5)

# 1. CLV por canal
ax1 = fig.add_subplot(gs[0, 0])
style_ax(ax1)
ch = channel_stats.sort_values('avg_clv', ascending=True)
bars = ax1.barh(ch['acquisition_channel'], ch['avg_clv'],
                color=COLORS[:len(ch)], edgecolor='none', height=0.55)
ax1.set_title('CLV Promedio por Canal', fontweight='bold')
ax1.set_xlabel('₹ CLV promedio')
for bar, val in zip(bars, ch['avg_clv']):
    ax1.text(val + 10, bar.get_y() + bar.get_height()/2,
             f'₹{val:,.0f}', va='center', color=TEXT, fontsize=8)

# 2. Clientes por canal
ax2 = fig.add_subplot(gs[0, 1])
style_ax(ax2)
ch2 = channel_stats.sort_values('customers', ascending=True)
ax2.barh(ch2['acquisition_channel'], ch2['customers'],
         color=COLORS[:len(ch2)], edgecolor='none', height=0.55)
ax2.set_title('Clientes por Canal', fontweight='bold')
ax2.set_xlabel('Número de clientes')
for i, (val, name) in enumerate(zip(ch2['customers'], ch2['acquisition_channel'])):
    ax2.text(val + 1, i, str(val), va='center', color=TEXT, fontsize=8)

# 3. Retención por canal
ax3 = fig.add_subplot(gs[0, 2])
style_ax(ax3)
ret = retention.sort_values('retention_rate', ascending=True)
colors_ret = ['#ff6b6b' if r < 67 else '#fcc419' if r < 70 else '#51cf66'
              for r in ret['retention_rate']]
bars3 = ax3.barh(ret['acquisition_channel'], ret['retention_rate'],
                 color=colors_ret, edgecolor='none', height=0.55)
ax3.set_title('Tasa de Retención por Canal (%)', fontweight='bold')
ax3.set_xlabel('Retención %')
ax3.set_xlim(0, 100)
for bar, val in zip(bars3, ret['retention_rate']):
    ax3.text(val + 0.5, bar.get_y() + bar.get_height()/2,
             f'{val:.1f}%', va='center', color=TEXT, fontsize=8)

# 4. CLV por grupo de edad
ax4 = fig.add_subplot(gs[1, 0])
style_ax(ax4)
age_clv = clv.groupby('age_group')['clv'].mean().sort_values(ascending=True)
ax4.barh(age_clv.index, age_clv.values,
         color='#a855f7', edgecolor='none', height=0.55)
ax4.set_title('CLV Promedio por Grupo de Edad', fontweight='bold')
ax4.set_xlabel('₹ CLV promedio')
for i, val in enumerate(age_clv.values):
    ax4.text(val + 10, i, f'₹{val:,.0f}', va='center', color=TEXT, fontsize=8)

# 5. Motivos de devolución
ax5 = fig.add_subplot(gs[1, 1])
style_ax(ax5)
reasons = returns_full['return_reason'].value_counts().sort_values()
colors_r = ['#ff6b6b','#fcc419','#fcc419','#fcc419','#51cf66']
ax5.barh(reasons.index, reasons.values, color=colors_r, edgecolor='none', height=0.55)
ax5.set_title('Motivos de Devolución', fontweight='bold')
ax5.set_xlabel('Número de devoluciones')
for i, val in enumerate(reasons.values):
    ax5.text(val + 0.3, i, str(val), va='center', color=TEXT, fontsize=8)

# 6. Devoluciones por categoría
ax6 = fig.add_subplot(gs[1, 2])
style_ax(ax6)
cat_ret = returns_full['category'].value_counts().sort_values()
ax6.barh(cat_ret.index, cat_ret.values,
         color='#ff6b6b', edgecolor='none', height=0.55)
ax6.set_title('Devoluciones por Categoría', fontweight='bold')
ax6.set_xlabel('Devoluciones')
for i, val in enumerate(cat_ret.values):
    ax6.text(val + 0.2, i, str(val), va='center', color=TEXT, fontsize=8)

# 7. Heatmap de cohortes
ax7 = fig.add_subplot(gs[2, :])
style_ax(ax7)
cohort_pivot = cohort.pivot(
    index='cohort', columns='quarters_since', values='retention_pct'
).fillna(0)
cohort_pivot.columns = [f'Q+{c}' for c in cohort_pivot.columns]
mask = cohort_pivot == 0
sns.heatmap(cohort_pivot, ax=ax7, cmap='BuPu', annot=True, fmt='.0f',
            linewidths=0.5, linecolor=GRID, mask=mask,
            vmin=0, vmax=35,
            cbar_kws={'label': 'Retención %'},
            annot_kws={'size': 9, 'color': 'white', 'fontweight': 'bold'})
ax7.set_title('Análisis de Cohortes — Retención Trimestral (%)', fontweight='bold')
ax7.set_xlabel('Trimestres desde primera compra')
ax7.set_ylabel('Cohorte')
ax7.tick_params(colors=TEXT)

fig.text(0.5, 0.97, 'Skincare E-Commerce — Análisis Completo de Negocio',
         ha='center', fontsize=16, fontweight='bold', color=TEXT)
fig.text(0.5, 0.94, 'CLV · Canales · Retención · Cohortes · Devoluciones  |  438 clientes  |  Dataset D2C Skincare',
         ha='center', fontsize=9, color='#888888')

plt.savefig('reports/full_analysis.png', dpi=150, bbox_inches='tight',
            facecolor=fig.get_facecolor())
plt.show()
print("Dashboard guardado en reports/full_analysis.png")