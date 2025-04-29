
import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium

# بارگذاری داده‌ها
df = pd.read_csv("realistic_milan_data_with_cluster.csv")

# تعریف نگاشت خوشه‌ها به برچسب‌های متنی
cluster_map = {0: "low", 1: "medium", 2: "high"}
df["growth_cluster_label"] = df["growth_cluster_label"].map(cluster_map)

# فیلترها
st.sidebar.header("Filter properties")

min_price, max_price = int(df["price"].min()), int(df["price"].max())
price_range = st.sidebar.slider("Price range (€)", min_price, max_price, (min_price, max_price))

min_area, max_area = int(df["area_sqm"].min()), int(df["area_sqm"].max())
area_range = st.sidebar.slider("Area range (sqm)", min_area, max_area, (min_area, max_area))

growth_filter = st.sidebar.multiselect(
    "Growth category",
    options=["low", "medium", "high"],
    default=["low", "medium", "high"]
)

# فیلتر کردن داده‌ها
filtered_df = df[
    (df["price"] >= price_range[0]) & (df["price"] <= price_range[1]) &
    (df["area_sqm"] >= area_range[0]) & (df["area_sqm"] <= area_range[1]) &
    (df["growth_cluster_label"].isin(growth_filter))
]

# نمایش داده‌ها
st.title("🏙️ Investment Potential in Milan")
st.write("Explore neighborhoods in Milan based on property value and growth potential.")
st.write(f"Showing {len(filtered_df)} properties")

st.dataframe(filtered_df[["neighborhood", "price", "area_sqm", "growth_cluster_label"]])

# نقشه
m = folium.Map(location=[45.4642, 9.19], zoom_start=12)

for _, row in filtered_df.iterrows():
    folium.CircleMarker(
        location=[row["latitude"], row["longitude"]],
        radius=5,
        popup=f"{row['neighborhood']} - €{row['price']}",
        color="blue",
        fill=True,
    ).add_to(m)

st.subheader("📍 Property Map")
st_data = st_folium(m, width=700, height=500)
