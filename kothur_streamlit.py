import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
toy= pd.read_csv("toy_dataset.csv")
toy.head()
age=toy["Age"]
income=toy["Income"]
city=toy["City"]
plt.figure(figsize=(10, 6))
plt.xticks(rotation=45)
plt.bar(city,income)
plt.title("Income raised by each city")
plt.xlabel("city")
plt.ylabel("income")
st.pyplot(plt)

