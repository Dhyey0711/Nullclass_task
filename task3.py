#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import plotly.graph_objects as go
from datetime import datetime
import pytz
import matplotlib.pyplot as plt
import seaborn as sns


# In[2]:


file_path = r"C:\Users\tanna\OneDrive - MSFT\Nullclass\Play Store Data.csv"
df = pd.read_csv(file_path)


# In[3]:


# Data Cleaning
# Clean 'Installs' - remove ',' and '+' then convert to numeric
df['Installs'] = pd.to_numeric(df['Installs'].str.replace('[+,]', '', regex=True), errors='coerce')

# Clean 'Revenue' - convert to numeric
df['Revenue'] = pd.to_numeric(df['Revenue'], errors='coerce')

# Clean 'Size' - convert sizes like '25M' to 25 and '1000k' to 1M
def clean_size(size):
    if 'M' in size:
        return float(size.replace('M', ''))
    elif 'k' in size:
        return float(size.replace('k', '')) / 1000
    else:
        return None

df['Size'] = df['Size'].apply(clean_size)

# Clean 'Android Ver' - extract numeric version
def extract_android_version(version):
    try:
        return float(version.split()[0])
    except:
        return None

df['Android Ver'] = df['Android Ver'].apply(extract_android_version)

# Filter data based on specified conditions
filtered_data = df[
    (df['Installs'] >= 10000) &
    (df['Revenue'] >= 10000) &
    (df['Size'] > 15) &
    (df['Android Ver'] > 4.0) &
    (df['Content Rating'] == 'Everyone') &
    (df['App'].str.len() <= 30)
]

# Identify top 3 categories by total installs
top_3_categories = filtered_data.groupby('Category')['Installs'].sum().nlargest(3).index

# Filter for top 3 categories
top_categories_data = filtered_data[filtered_data['Category'].isin(top_3_categories)]

# Aggregate data for average installs and revenue
chart_data = top_categories_data.groupby(['Category', 'Type']).agg({
    'Installs': 'mean',
    'Revenue': 'mean'
}).reset_index()

# Check time condition - Show graph only between 1 PM IST and 2 PM IST
ist = pytz.timezone('Asia/Kolkata')
current_time = datetime.now(ist)
if current_time.hour == 10:  # 1 PM IST
    # Dual-axis plot with improved styling
    plt.figure(figsize=(12, 7))
    ax = sns.barplot(x='Category', y='Installs', hue='Type', data=chart_data, alpha=0.7, color='blue')

    # Overlay revenue as line plot on the secondary axis
    ax2 = ax.twinx()
    sns.lineplot(x='Category', y='Revenue', hue='Type', data=chart_data, marker='o', linewidth=2.5, color='orange', ax=ax2)

    # Add horizontal reference lines
    ax.axhline(y=chart_data['Installs'].mean(), color='blue', linestyle='--', linewidth=1.5, alpha=0.5)
    ax2.axhline(y=chart_data['Revenue'].mean(), color='orange', linestyle='--', linewidth=1.5, alpha=0.5)

    # Formatting
    ax.set_title('Average Installs Vs. Revenue for Top 3 Categories', fontsize=16, weight='bold')
    ax.set_ylabel('Average Installs (in millions)', color='blue')
    ax2.set_ylabel('Average Revenue (USD)', color='orange')

    ax.tick_params(axis='y', colors='blue')
    ax2.tick_params(axis='y', colors='orange')

    ax.legend(title='Type (Installs)', loc='upper left')
    ax2.legend(title='Type (Revenue)', loc='upper right')

    plt.show()
else:
    print("This chart is only available between 1 PM IST and 2 PM IST.")


# In[ ]:





# In[ ]:




