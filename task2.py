#!/usr/bin/env python
# coding: utf-8

# In[19]:


import plotly.express as px
import pandas as pd
from datetime import datetime, time
import pytz


# In[20]:


file_path = r"C:\Users\tanna\OneDrive - MSFT\Nullclass\Play Store Data.csv"
data = pd.read_csv(file_path)


# In[21]:


ist = pytz.timezone("Asia/Kolkata")
current_time = datetime.now(ist).time()
allowed_start = time(18, 0)  # 6 PM IST
allowed_end = time(20, 0)    # 8 PM IST

if allowed_start <= current_time <= allowed_end:
    data['Installs'] = data['Installs'].astype(str).str.replace('[+,]', '', regex=True)
    data['Installs'] = pd.to_numeric(data['Installs'], errors='coerce')

    filtered_data = data[(~data['Category'].str.startswith(('A', 'C', 'G', 'S'))) & (data['Installs'] > 1_000_000)]

    # Top 5 categories with highest installs
    top_5_categories = filtered_data.groupby('Category')['Installs'].sum().nlargest(5).reset_index()

    # Plotting the top 5 app categories using Plotly
    fig = px.bar(top_5_categories, x='Category', y='Installs',
                 title='Top 5 App Categories with Installs Over 1 Million',
                 color='Installs', color_continuous_scale='Blues')
    fig.show()

    # Mapping categories to sample country codes for visualization
    category_country_map = {
        "FAMILY": "USA",
        "NEWS_AND_MAGAZINES": "IND",
        "PHOTOGRAPHY": "FRA",
        "PRODUCTIVITY": "JPN",
        "TOOLS": "BRA"
    }

    final_data = filtered_data[filtered_data['Category'].isin(top_5_categories['Category'])]
    final_data['Country'] = final_data['Category'].map(category_country_map)

    # Create a choropleth map with distinct colors for each category
    global_map = px.choropleth(final_data,
                               locations="Country",
                               locationmode="ISO-3",
                               color="Category",
                               hover_name="Category",
                               color_discrete_sequence=px.colors.qualitative.Set1,
                               projection="natural earth"
                              )

    global_map.update_layout(margin={"r":0, "t":0, "l":0, "b":0})
    global_map.show()
else:
    print("Graph is only available between 6 PM and 8 PM IST.")


# In[ ]:




