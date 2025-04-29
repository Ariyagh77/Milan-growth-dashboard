
import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium

# Load the data
df = pd.read_csv("realistic_milan_data_with_cluster.csv")

# Fix the missing label mapping
cluster_map = {0: 'low', 1: 'medium', 2: 'high'}
df['growth_cluster_label'] = df['growth_cluster'].map(cluster_map)

# Sidebar filters
st.sidebar.header("Filter properties")
price_range = st.sidebar.slider("Price range (€)", int(df["price"].min()), int(df["price"].max()), (int(df["price"].min()), int(df["price"].max())))
area_range = st.sidebar.slider("Area range (sqm)", int(df["area_sqm"].min()), int(df["area_sqm"].max()), (int(df["area_sqm"].min()), int(df["area_sqm"].max())))
growth_filter = st.sidebar.multiselect("Growth category", options=["low", "medium", "high"], default=["low", "medium", "high"])

# Filter the dataframe
filtered_df = df[
    (df["price"] >= price_range[0]) & 
    (df["price"] <= price_range[1]) &
    (df["area_sqm"] >= area_range[0]) &
    (df["area_sqm"] <= area_range[1]) &
    (df["growth_cluster_label"].isin(growth_filter))
]

# App layout
st.title("🏙️ Investment Potential in Milan")
st.markdown("Explore neighborhoods in Milan based on property value and growth potential.")

# Display table
st.write(f"Showing {len(filtered_df)} properties")
st.dataframe(filtered_df[["district", "price", "area_sqm", "growth_cluster_label"]])

# Map
st.subheader("📍 Property Map")
m = folium.Map(location=[45.4642, 9.19], zoom_start=12)

for _, row in filtered_df.iterrows():
    folium.Marker(
        location=[row["latitude"], row["longitude"]],
        popup=f"{row['district']} - €{int(row['price'])}",
        tooltip=row["growth_cluster_label"]
    ).add_to(m)

st_folium(m, width=700)
