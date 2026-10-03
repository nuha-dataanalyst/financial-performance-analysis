import pandas as pd
import numpy as np
import os

np.random.seed(42)

years = list(range(2019, 2024))
months = list(range(1, 13))

departments = ['Sales', 'Operations', 'HR', 'Marketing', 'IT', 'Finance']

base_revenue = {
    2019: 15000000,
    2020: 13500000,  # COVID impact
    2021: 16000000,
    2022: 18500000,
    2023: 22000000,
}

expense_ratio = {
    'Sales':       0.15,
    'Operations':  0.25,
    'HR':          0.10,
    'Marketing':   0.12,
    'IT':          0.08,
    'Finance':     0.05,
}

records = []

for year in years:
    annual_revenue = base_revenue[year]
    for month in months:
        seasonal = 1 + 0.05 * np.sin(2 * np.pi * month / 12)
        noise = np.random.uniform(0.95, 1.05)
        monthly_revenue = round(annual_revenue / 12 * seasonal * noise, 2)

        for dept in departments:
            expense = round(monthly_revenue * expense_ratio[dept] * np.random.uniform(0.9, 1.1), 2)
            gross_profit = round(monthly_revenue - expense, 2)
            profit_margin = round((gross_profit / monthly_revenue) * 100, 2)
            tax = round(gross_profit * 0.28, 2)
            net_profit = round(gross_profit - tax, 2)

            records.append({
                'Year': year,
                'Month': month,
                'Month_Name': pd.Timestamp(f'{year}-{month}-01').strftime('%B'),
                'Quarter': f'Q{(month-1)//3+1}',
                'Department': dept,
                'Revenue_LKR': monthly_revenue,
                'Expenses_LKR': expense,
                'Gross_Profit_LKR': gross_profit,
                'Profit_Margin_Pct': profit_margin,
                'Tax_LKR': tax,
                'Net_Profit_LKR': net_profit,
            })

df = pd.DataFrame(records)
os.makedirs('data', exist_ok=True)
df.to_csv('data/ceylon_tech_financials.csv', index=False)
print(f"Dataset created: {len(df)} rows")
print(df.head(10))