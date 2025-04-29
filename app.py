
import streamlit as st
import pandas as pd
import folium
from streamlit_folium import folium_static

# Load data
df = pd.read_csv("realistic_milan_data.csv")

# Title
st.title("🏙️ Investment Potential in Milan")
st.markdown("Explore neighborhoods in Milan based on property value and growth potential.")

# Sidebar filters
st.sidebar.header("Filter properties")
min_price, max_price = st.sidebar.slider("Price range (€)", int(df['price'].min()), int(df['price'].max()), (int(df['price'].min()), int(df['price'].max())))
min_area, max_area = st.sidebar.slider("Area range (sqm)", int(df['area_sqm'].min()), int(df['area_sqm'].max()), (int(df['area_sqm'].min()), int(df['area_sqm'].max())))
growth_filter = st.sidebar.multiselect("Growth category", ["low", "medium", "high"], default=["low", "medium", "high"])

# Filter data
filtered_df = df[
    (df['price'] >= min_price) &
    (df['price'] <= max_price) &
    (df['area_sqm'] >= min_area) &
    (df['area_sqm'] <= max_area) &
    (df['growth_cluster_label'].isin(growth_filter))
]

# Show filtered data
st.write(f"Showing {len(filtered_df)} properties")
st.dataframe(filtered_df[['neighborhood', 'price', 'area_sqm', 'growth_cluster_label']])

# Show map
m = folium.Map(location=[45.4642, 9.19], zoom_start=11)
color_map = {"low": "red", "medium": "orange", "high": "green"}

for _, row in filtered_df.iterrows():
    folium.CircleMarker(
        location=[row['latitude'], row['longitude']],
        radius=5,
        popup=f"{row['neighborhood']} - €{int(row['price'])}",
        color=color_map.get(row['growth_cluster_label'], "blue"),
        fill=True,
        fill_opacity=0.7
    ).add_to(m)

st.subheader("📍 Property Map")
folium_static(m)

# Notes
st.markdown("This dashboard uses synthetic yet realistic data for analysis and visualization purposes.")
