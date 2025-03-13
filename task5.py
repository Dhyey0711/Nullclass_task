#!/usr/bin/env python
# coding: utf-8

# In[7]:


import pandas as pd
import plotly.express as px
from datetime import datetime
import pytz
import matplotlib.pyplot as plt


# In[8]:


file_path = r"C:\Users\tanna\OneDrive - MSFT\Nullclass\Play Store Data.csv"
df = pd.read_csv(file_path)


# In[9]:


df['Installs'] = pd.to_numeric(df['Installs'].str.replace('[+,]', '', regex=True), errors='coerce')
df['Last Updated'] = pd.to_datetime(df['Last Updated'], errors='coerce')
df['Month'] = df['Last Updated'].dt.to_period('M')

# Filter data for conditions
filtered_data = df[(df['Content Rating'] == 'Teen') &
                    (df['App'].str.startswith('E')) &
                    (df['Installs'] > 10000)]

# Aggregate installs by month and category
trend_data = filtered_data.groupby(['Month', 'Category'])['Installs'].sum().unstack().fillna(0)

# Calculate month-over-month growth
growth = trend_data.pct_change() > 0.20

# Check time condition - Show graph only between 6 PM IST and 9 PM IST
ist = pytz.timezone('Asia/Kolkata')
current_time = datetime.now(ist)
if 18 <= current_time.hour < 21:
    # Plotting
    plt.figure(figsize=(12, 6))
    for category in trend_data.columns:
        plt.plot(trend_data.index.astype(str), trend_data[category], label=category)
        plt.fill_between(trend_data.index.astype(str),
                         trend_data[category],
                         where=growth[category],
                         alpha=0.3)

    plt.title('Total Installs Trend by Category (Highlighting >20% Growth)', fontsize=14, weight='bold')
    plt.xlabel('Date')
    plt.ylabel('Total Installs')
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()
else:
    print("This chart is only available between 6 PM IST and 9 PM IST.")


# In[ ]:





# In[ ]:




