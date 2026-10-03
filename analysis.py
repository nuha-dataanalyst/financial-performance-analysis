import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import seaborn as sns
import numpy as np
import os

df = pd.read_csv('data/ceylon_tech_financials.csv')
os.makedirs('charts', exist_ok=True)

sns.set_theme(style='whitegrid')

def format_millions(x, _):
    return f'LKR {x/1e6:.1f}M'

COLORS = ['#E23744', '#1B3A5C', '#F4A261', '#2EC4B6', '#A8DADC', '#6B4226']

# ── CHART 1: Annual Revenue vs Net Profit ──────────────────────
annual = df.groupby('Year').agg(
    Revenue=('Revenue_LKR', 'sum'),
    Net_Profit=('Net_Profit_LKR', 'sum')
).reset_index()

fig, ax1 = plt.subplots(figsize=(12, 6))
ax2 = ax1.twinx()
bars = ax1.bar(annual['Year'], annual['Revenue'], color='#1B3A5C',
               alpha=0.8, label='Revenue', width=0.4)
ax2.plot(annual['Year'], annual['Net_Profit'], color='#E23744',
         marker='o', linewidth=2.5, label='Net Profit')
ax1.set_xlabel('Year', fontsize=12)
ax1.set_ylabel('Revenue (LKR)', fontsize=12)
ax2.set_ylabel('Net Profit (LKR)', fontsize=12)
ax1.yaxis.set_major_formatter(mticker.FuncFormatter(format_millions))
ax2.yaxis.set_major_formatter(mticker.FuncFormatter(format_millions))
plt.title('Annual Revenue vs Net Profit (2019–2023)', fontsize=15, fontweight='bold')
lines1, labels1 = ax1.get_legend_handles_labels()
lines2, labels2 = ax2.get_legend_handles_labels()
ax1.legend(lines1 + lines2, labels1 + labels2, loc='upper left')
plt.tight_layout()
plt.savefig('charts/chart1_revenue_vs_profit.png', dpi=150)
plt.close()
print("Chart 1 saved.")

# ── CHART 2: Department Expense Breakdown ──────────────────────
dept = df.groupby('Department').agg(
    Total_Expenses=('Expenses_LKR', 'sum'),
    Total_Revenue=('Revenue_LKR', 'sum')
).reset_index()
dept['Expense_Ratio'] = (dept['Total_Expenses'] / dept['Total_Revenue'] * 100).round(2)
dept = dept.sort_values('Total_Expenses', ascending=True)

plt.figure(figsize=(12, 6))
bars = plt.barh(dept['Department'], dept['Total_Expenses'], color=COLORS)
plt.xlabel('Total Expenses (LKR)', fontsize=12)
plt.title('Department Expense Breakdown (2019–2023)', fontsize=15, fontweight='bold')
plt.gca().xaxis.set_major_formatter(mticker.FuncFormatter(format_millions))
for bar, val in zip(bars, dept['Total_Expenses']):
    plt.text(bar.get_width() + 1000000, bar.get_y() + bar.get_height()/2,
             f'LKR {val/1e6:.1f}M', va='center', fontsize=9)
plt.tight_layout()
plt.savefig('charts/chart2_department_expenses.png', dpi=150)
plt.close()
print("Chart 2 saved.")

# ── CHART 3: Profit Margin Trend by Year ───────────────────────
margin = df.groupby(['Year', 'Department'])['Profit_Margin_Pct'].mean().reset_index()

plt.figure(figsize=(12, 6))
for i, dept_name in enumerate(margin['Department'].unique()):
    data = margin[margin['Department'] == dept_name]
    plt.plot(data['Year'], data['Profit_Margin_Pct'], marker='o',
             label=dept_name, color=COLORS[i], linewidth=2.5)

plt.title('Profit Margin % by Department (2019–2023)', fontsize=15, fontweight='bold')
plt.xlabel('Year', fontsize=12)
plt.ylabel('Profit Margin (%)', fontsize=12)
plt.legend(title='Department')
plt.tight_layout()
plt.savefig('charts/chart3_profit_margin_trend.png', dpi=150)
plt.close()
print("Chart 3 saved.")

# ── CHART 4: Monthly Revenue Heatmap ───────────────────────────
monthly = df.groupby(['Year', 'Month'])['Revenue_LKR'].sum().reset_index()
pivot = monthly.pivot(index='Year', columns='Month', values='Revenue_LKR')
pivot.columns = ['Jan','Feb','Mar','Apr','May','Jun',
                 'Jul','Aug','Sep','Oct','Nov','Dec']

plt.figure(figsize=(14, 6))
sns.heatmap(pivot, annot=True, fmt='.0f', cmap='RdYlGn',
            linewidths=0.5, cbar_kws={'label': 'Revenue (LKR)'})
plt.title('Monthly Revenue Heatmap by Year', fontsize=15, fontweight='bold')
plt.tight_layout()
plt.savefig('charts/chart4_monthly_revenue_heatmap.png', dpi=150)
plt.close()
print("Chart 4 saved.")

# ── CHART 5: Revenue Forecast (Simple Linear) ──────────────────
from numpy.polynomial import polynomial as P

annual2 = df.groupby('Year')['Revenue_LKR'].sum().reset_index()
x = annual2['Year'].values
y = annual2['Revenue_LKR'].values
coefs = np.polyfit(x, y, 1)
forecast_years = np.array([2024, 2025, 2026])
forecast_values = np.polyval(coefs, forecast_years)

plt.figure(figsize=(12, 6))
plt.plot(x, y, marker='o', color='#1B3A5C', linewidth=2.5,
         label='Actual Revenue')
plt.plot(forecast_years, forecast_values, marker='s', color='#E23744',
         linewidth=2.5, linestyle='--', label='Forecasted Revenue')
plt.axvline(x=2023.5, color='grey', linestyle=':', linewidth=1.5)
plt.text(2023.6, max(y)*0.95, 'Forecast →', color='grey', fontsize=10)
plt.title('Revenue Forecast 2024–2026', fontsize=15, fontweight='bold')
plt.xlabel('Year', fontsize=12)
plt.ylabel('Revenue (LKR)', fontsize=12)
plt.gca().yaxis.set_major_formatter(mticker.FuncFormatter(format_millions))
plt.legend()
plt.tight_layout()
plt.savefig('charts/chart5_revenue_forecast.png', dpi=150)
plt.close()
print("Chart 5 saved.")

# ── CHART 6: Quarterly Performance ─────────────────────────────
quarterly = df.groupby(['Year', 'Quarter']).agg(
    Revenue=('Revenue_LKR', 'sum'),
    Net_Profit=('Net_Profit_LKR', 'sum')
).reset_index()
quarterly['Label'] = quarterly['Year'].astype(str) + ' ' + quarterly['Quarter']

plt.figure(figsize=(14, 6))
x = range(len(quarterly))
plt.bar([i - 0.2 for i in x], quarterly['Revenue'],
        width=0.4, color='#1B3A5C', label='Revenue')
plt.bar([i + 0.2 for i in x], quarterly['Net_Profit'],
        width=0.4, color='#E23744', label='Net Profit')
plt.xticks(list(x), quarterly['Label'], rotation=45, ha='right')
plt.title('Quarterly Revenue vs Net Profit (2019–2023)', fontsize=15, fontweight='bold')
plt.ylabel('Amount (LKR)', fontsize=12)
plt.gca().yaxis.set_major_formatter(mticker.FuncFormatter(format_millions))
plt.legend()
plt.tight_layout()
plt.savefig('charts/chart6_quarterly_performance.png', dpi=150)
plt.close()
print("Chart 6 saved.")

print("\n✅ All 6 charts saved to charts folder.")