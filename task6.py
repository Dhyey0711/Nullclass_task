#!/usr/bin/env python
# coding: utf-8

# In[7]:


import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
import pytz


# In[8]:


file_path = r"C:\Users\tanna\OneDrive - MSFT\Nullclass\Play Store Data.csv"
df = pd.read_csv(file_path)


# In[9]:


df['Installs'] = pd.to_numeric(df['Installs'].str.replace('[+,]', '', regex=True), errors='coerce')
df['Reviews'] = pd.to_numeric(df['Reviews'], errors='coerce')
df['Last Updated'] = pd.to_datetime(df['Last Updated'], errors='coerce')

# Filtering Data
df_filtered = df[(df['Last Updated'] >= df['Last Updated'].max() - timedelta(days=5*365)) &
                 (df['Installs'] >= 100000) &
                 (df['Reviews'] > 1000) &
                 (~df['Genres'].str[0].isin(['A', 'F', 'E', 'G', 'I', 'K']))]

# Check current time in IST
current_time = datetime.now(pytz.timezone('Asia/Kolkata')).time()
start_time = datetime.strptime("14:00", "%H:%M").time()
end_time = datetime.strptime("16:00", "%H:%M").time()

# Generate heatmap only within the specified timeframe
if start_time <= current_time <= end_time:
    plt.figure(figsize=(8, 6))
    corr_matrix = df_filtered[['Installs', 'Rating', 'Reviews']].corr()
    sns.heatmap(corr_matrix, annot=True, cmap='coolwarm', linewidths=0.5, vmin=-1, vmax=1)
    plt.title('Correlation Heatmap: Installs, Ratings, and Reviews (Filtered Data)')
    plt.show()
else:
    print("Heatmap is only available between 2 PM IST and 4 PM IST.")


# In[ ]:




