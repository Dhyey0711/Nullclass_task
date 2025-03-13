#!/usr/bin/env python
# coding: utf-8

# In[7]:


import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime
import pytz
import numpy as np


# In[8]:


file_path = r"C:\Users\tanna\OneDrive - MSFT\Nullclass\Play Store Data.csv"
data = pd.read_csv(file_path)


# In[9]:


def convert_size(size):
    if 'M' in size:
        return float(size.replace('M', ''))
    elif 'k' in size:
        return float(size.replace('k', '')) / 1024
    else:
        return np.nan
data['Size'] = data['Size'].apply(convert_size)
data['Installs'] = pd.to_numeric(data['Installs'].str.replace('[+,]', '', regex=True), errors='coerce')

# Data Filtering
filtered_data = data[(data['Category'] == 'GAME') &
                     (data['Rating'] > 3.5) &
                     (data['Installs'] > 50000)]

# Time Filter: Display only between 5 PM IST and 7 PM IST
current_time = datetime.now().strftime('%H:%M')
if '17:00' <= current_time <= '19:00':
    # Bubble Chart
    plt.figure(figsize=(12, 8))
    plt.scatter(filtered_data['Size'], filtered_data['Rating'],
                s=filtered_data['Installs'] / 100000,
                alpha=0.6, c=filtered_data['Rating'], cmap='viridis', edgecolors='black')

    plt.title('Bubble Chart: App Size vs. Average Rating (Games Category)', fontsize=16, fontweight='bold')
    plt.xlabel('App Size (MB)', fontsize=12)
    plt.ylabel('Average Rating', fontsize=12)
    plt.colorbar(label='Rating')
    plt.grid(True, linestyle='--', alpha=0.5)
    plt.tight_layout()
    plt.show()
else:
    print("This chart is only available between 5 PM and 7 PM IST.")


# In[ ]:




