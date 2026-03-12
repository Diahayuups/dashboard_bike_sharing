import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

st.set_page_config(
    page_title="Dashboard Analisis Bike Sharing",
    page_icon="🚲",
    layout="wide"
)

# Load dataset
main_df = pd.read_csv("dashboard/main_data.csv")

main_df["dteday"] = pd.to_datetime(main_df["dteday"])

# ===== SIDEBAR =====
with st.sidebar:
    st.header("Submission Proyek BFDA")

    st.image("dashboard/foto.jpg")

    st.markdown("## Profil Cohort")

    st.write("Nama: Diah Ayu Puspasari")

    st.write("ID Cohort: cdcc156d6x1244")

    st.write("Kelas: CDC - 12")

    st.markdown("---")

    min_date = main_df["dteday"].min()
    max_date = main_df["dteday"].max()

    date_range = st.date_input(
        "Pilih Rentang Waktu",
        min_value=min_date,
        max_value=max_date,
        value=(min_date, max_date)
    )

    if len(date_range) == 2:
        start_date, end_date = date_range
    else:
        start_date = end_date = date_range[0]

# Filter data
filtered_df = main_df[
    (main_df["dteday"] >= str(start_date)) &
    (main_df["dteday"] <= str(end_date))
]

# ===== HEADER =====
st.header("Bike Sharing Data Analysis")
st.markdown(
"""
Dashboard ini menampilkan analisis pola penyewaan sepeda berdasarkan:

- Kondisi cuaca  
- Jenis hari (hari kerja vs hari libur)  
- Pola aktivitas berdasarkan jam  
"""
)

st.markdown("---")

# ===== METRIC =====
st.subheader("Summary")

col1, col2 = st.columns(2)

with col1:
    total_rentals = filtered_df["cnt_hour"].sum()
    st.metric("Total Rentals", total_rentals)

with col2:
    avg_rentals = round(filtered_df["cnt_hour"].mean(), 2)
    st.metric("Average Rentals", avg_rentals)

# ===== RENTAL BY WEATHER =====
st.subheader("Average Bike Rentals by Weather")

weather_df = filtered_df.groupby("weathersit_day")["cnt_hour"].mean().reset_index()

fig, ax = plt.subplots()

sns.barplot(
    x="weathersit_day",
    y="cnt_hour",
    data=weather_df,
    palette="Blues",
    ax=ax
)

ax.set_xlabel("Weather Condition")
ax.set_ylabel("Average Rentals")

st.pyplot(fig)
st.markdown("---")

# ===== RENTAL BY WORKING DAY =====
st.subheader("Bike Rentals: Working Day vs Holiday")

workingday_df = filtered_df.groupby("workingday_day")["cnt_hour"].mean().reset_index()

fig, ax = plt.subplots()

sns.barplot(
    x="workingday_day",
    y="cnt_hour",
    data=workingday_df,
    palette="Blues",
    ax=ax
)

ax.set_xlabel("Working Day (1 = Yes, 0 = No)")
ax.set_ylabel("Average Rentals")

st.pyplot(fig)
st.markdown("---")

# ===== RENTAL BY HOUR =====
st.subheader("Bike Rental Activity by Hour")

hour_df = filtered_df.groupby("hr")["cnt_hour"].mean().reset_index()

fig, ax = plt.subplots(figsize=(10,5))

sns.lineplot(
    x="hr",
    y="cnt_hour",
    data=hour_df,
    marker="o",
    ax=ax
)

ax.set_xlabel("Hour")
ax.set_ylabel("Average Rentals")

st.pyplot(fig)
st.markdown("---")

st.subheader("Bike Rental Usage Category")

# membuat kategori penggunaan sepeda
filtered_df["rental_category"] = pd.cut(
    filtered_df["cnt_hour"],
    bins=3,
    labels=["Low Usage", "Medium Usage", "High Usage"]
)

usage_df = filtered_df["rental_category"].value_counts().reset_index()
usage_df.columns = ["category", "count"]

fig, ax = plt.subplots()

sns.barplot(
    x="category",
    y="count",
    hue="category",
    data=usage_df,
    palette="Blues",
    legend=False,
    ax=ax
)

ax.set_xlabel("Rental Category")
ax.set_ylabel("Number of Records")

st.pyplot(fig)


st.caption("© 2026 - Diah Ayu Puspasari | Dicoding Submission")
