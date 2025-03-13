#!/usr/bin/env python
# coding: utf-8

# In[4]:


import pandas as pd
import plotly.express as px
from datetime import datetime
import pytz
import matplotlib.pyplot as plt
import seaborn as sns


# In[5]:


file_path = r"C:\Users\tanna\OneDrive - MSFT\Nullclass\Play Store Data.csv"
df = pd.read_csv(file_path)


# In[6]:


df['Installs'] = pd.to_numeric(df['Installs'].str.replace('[+,]', '', regex=True), errors='coerce')
df['Reviews'] = pd.to_numeric(df['Reviews'], errors='coerce')
df['Size'] = df['Size'].apply(lambda x: float(x.replace('M', '')) if 'M' in str(x) else None)
df['Rating'] = pd.to_numeric(df['Rating'], errors='coerce')
df['Last Updated'] = pd.to_datetime(df['Last Updated'], errors='coerce')

# Filter data based on conditions
filtered_data = df[(df['Rating'] >= 4.0) &
                    (df['Size'] >= 10) &
                    (df['Last Updated'].dt.month == 1)]

# Identify top 10 categories by total installs
top_10_categories = filtered_data.groupby('Category')['Installs'].sum().nlargest(10).index

# Filter for top 10 categories
top_categories_data = filtered_data[filtered_data['Category'].isin(top_10_categories)]

# Aggregate data for average rating and total reviews
chart_data = top_categories_data.groupby('Category').agg({
    'Rating': 'mean',
    'Reviews': 'sum'
}).reset_index()

# Check time condition - Show graph only between 3 PM IST and 5 PM IST
ist = pytz.timezone('Asia/Kolkata')
current_time = datetime.now(ist)
if 15 <= current_time.hour < 17:
    # Grouped bar chart with improved styling
    fig, ax1 = plt.subplots(figsize=(12, 6))

    x = range(len(chart_data))
    ax1.bar(x, chart_data['Rating'], width=0.35, label='Average Rating', color='dodgerblue')
    ax1.set_ylabel('Average Rating', color='blue')
    ax1.tick_params(axis='y', labelcolor='blue')

    ax2 = ax1.twinx()
    ax2.bar([i + 0.35 for i in x], chart_data['Reviews'], width=0.35, label='Total Reviews', color='yellow')
    ax2.set_ylabel('Total Reviews', color='orange')
    ax2.tick_params(axis='y', labelcolor='orange')

    ax1.set_xticks([i + 0.35 / 2 for i in x])
    ax1.set_xticklabels(chart_data['Category'], rotation=45, ha='right')

    plt.title('Average Rating vs Total Reviews for Top 10 Categories', fontsize=16, weight='bold')
    ax1.legend(loc='upper left')
    ax2.legend(loc='upper right')

    plt.tight_layout()
    plt.show()
else:
    print("This chart is only available between 3 PM IST and 5 PM IST.")


# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:




