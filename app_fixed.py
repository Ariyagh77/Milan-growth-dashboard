
import streamlit as st
import pandas as pd

# Load data
df = pd.read_csv("realistic_milan_data.csv")

# Sidebar filters
st.sidebar.header("Filter properties")

price_min, price_max = st.sidebar.slider("Price range (€)", 
                                          int(df["price"].min()), 
                                          int(df["price"].max()), 
                                          (int(df["price"].min()), int(df["price"].max())))

area_min, area_max = st.sidebar.slider("Area range (sqm)", 
                                       int(df["area_sqm"].min()), 
                                       int(df["area_sqm"].max()), 
                                       (int(df["area_sqm"].min()), int(df["area_sqm"].max())))

growth_filter = st.sidebar.multiselect("Growth category", 
                                       options=df["growth_cluster"].unique(), 
                                       default=list(df["growth_cluster"].unique()))

# Filtered dataframe
filtered_df = df[
    (df["price"] >= price_min) & (df["price"] <= price_max) &
    (df["area_sqm"] >= area_min) & (df["area_sqm"] <= area_max) &
    (df["growth_cluster"].isin(growth_filter))
]

# Main content
st.title("Investment Potential in Milan")
st.markdown("Explore neighborhoods in Milan based on property value and growth potential.")

st.dataframe(filtered_df)
