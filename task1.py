#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

import plotly.express as px
import datetime


# In[2]:


file_path = r"C:\Users\tanna\OneDrive - MSFT\Nullclass\Play Store Data.csv"
df = pd.read_csv(file_path)
df = df[df["Type"] == "Paid"]

# Convert 'Installs' to numeric (removing '+' and ',')
df["Installs"] = df["Installs"].str.replace("[+,]", "", regex=True).astype(float)

# Convert 'Revenue' to numeric
df["Revenue"] = pd.to_numeric(df["Revenue"], errors='coerce')

# Drop rows with missing values in essential columns
df = df.dropna(subset=["Installs", "Revenue", "Category"])

# Set plot style
sns.set_style("whitegrid")
plt.figure(figsize=(10, 6))

# Create scatter plot
scatter = sns.scatterplot(data=df, x="Installs", y="Revenue", hue="Category", palette="viridis", alpha=0.7)

# Fit and plot the trendline using seaborn
sns.regplot(data=df, x="Installs", y="Revenue", scatter=False, color="red", line_kws={"linestyle": "dashed"})

# Log scale for better visualization
plt.xscale("log")
plt.yscale("log")

# Labels and title
plt.xlabel("Number of Installs (log scale)")
plt.ylabel("Revenue (log scale)")
plt.title("Relationship Between Revenue and Installs for Paid Apps")
plt.legend(title="Category", bbox_to_anchor=(1.05, 1), loc="upper left")

plt.savefig("scatter_plot.png", dpi=300, bbox_inches="tight")
# Show the plot
plt.show()


