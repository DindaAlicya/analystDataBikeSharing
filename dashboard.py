import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import time

# pastikan dataset ada
day_df = pd.read_csv("day.csv")
hour_df = pd.read_csv("hour.csv")

# penggabungan semua dataset
all_df = pd.concat([day_df, hour_df])

# rentang tanggal minimal dan amximal di kedua dataset
min_date = all_df['date'].min()
max_date = all_df['date'].max()

# judul dashboard interaktif
text = ":bicyclist: Welcome to Dinda's Bike Rental Dashboard :bicyclist:"
titlePlaceholder = st.empty()
titleText = ""
for char in text:
    titleText += char
    titlePlaceholder.markdown(f"### {titleText}")
    time.sleep(0.03)
st.image("dataset-cover.jpg") # gambar didapatkan pada sumber dataset (kaggle)

# sidebar yang berisi filtering
with st.sidebar:
    st.header(":bicyclist: Bike Rental Dashboard :bicyclist:")
    st.image("dataset-cover.jpg")

    # Pilihan mode filter waktu (Rentang Waktu atau Tahun & Bulan), hanya bisa menggunakan salah satu
    useDateRange = st.checkbox(" Use range time", value=True)

    if useDateRange:
        # jika pakai rentang waktu, filter tahun dan bulan dinonaktifkan
        start_date, end_date = st.date_input(
            label=':calendar: Range time',
            min_value=min_date,
            max_value=max_date,
            value=[min_date, max_date]
        )
        year_filter = None
        month_filter = None
    else:
        # jika pakai filter tahun & bulan, rentang waktu dinonaktifkan
        start_date, end_date = None, None
        year_filter = st.selectbox(":date: Select Year", sorted(day_df["year"].unique()))
        month_filter = st.selectbox(":calendar: Select Month", sorted(day_df["month"].unique()))

    # Filter cuaca bisa filter cuaca apa saja yang mau ditampilkan
    weatherFilter = st.sidebar.multiselect(
        ":sun_behind_rain_cloud: Select weather condition",
        day_df["weather"].unique(),
        default=day_df["weather"].unique()
    
    )

# menampilkan hasil pilihan
st.write("### :mag: Selected Filter:")

if useDateRange:
    st.write(f"Range time: {start_date} to {end_date}")
else:
    st.write(f"Year: {year_filter}, Month: {month_filter}")

if useDateRange:
    dayFiltered = day_df[
        (day_df["date"] >= str(start_date)) &
        (day_df["date"] <= str(end_date)) &
        (day_df["weather"].isin(weatherFilter))
    ]
    hourFiltered = hour_df[
        (hour_df["date"] >= str(start_date)) &
        (hour_df["date"] <= str(end_date)) &
        (hour_df["weather"].isin(weatherFilter))
    ]
else:
    dayFiltered = day_df[
        (day_df["year"] == year_filter) &
        (day_df["month"] == month_filter) &
        (day_df["weather"].isin(weatherFilter))
    ]
    hourFiltered = hour_df[
        (hour_df["year"] == year_filter) &
        (hour_df["month"] == month_filter) &
        (hour_df["weather"].isin(weatherFilter))
    ]

# line chart total penyewaan sepeda berdasarkan filter waktu yang dipilih (default, rentang waktu minimal dan maximal pada data)
st.subheader(" Total bike rentals over time")
fig, ax = plt.subplots()
ax.plot(dayFiltered["date"], dayFiltered["total_rent"], marker='o', linestyle='-', color='blue')
ax.set_xticklabels(dayFiltered["date"], rotation=90)
ax.set_ylabel("Total Rentals")
st.pyplot(fig)

# pie chart total penyewaan sepeda berdasarkan musim
st.subheader("Bike rentals by reason")
seasonTotal = dayFiltered.groupby("season")["total_rent"].sum()
fig2, ax2 = plt.subplots()
ax2.pie(seasonTotal, labels=seasonTotal.index, autopct='%1.1f%%', startangle=90, colors=['#95abaf','#eda325','#ffee6a','#74a2ea'])
ax2.axis('equal')
st.pyplot(fig2)

# bar chart total penyewaan sepeda berdasarkan filter cuaca yang dipilih (default, semua cuaca terlihat)
st.subheader("Bike rentals by weather condition")
weatherTotal = day_df.groupby("weather")[["user_casual", "user_registered"]].sum()
st.bar_chart(weatherTotal)

# bar chart perbandingan total penyewaan sepeda dalam seminggu(sesuai rentang waktu yang dipilih)
st.subheader("Bike rentals in a week")
fig4, ax4 = plt.subplots()
weekCount = dayFiltered.groupby("weekday")[["user_casual", "user_registered"]].sum()
st.bar_chart(weekCount)

# bar chart perbandingan total penyewaan sepeda di hari working day and not working day
st.subheader("Bike rentals workingday & Non-working day")
fig5, ax5 = plt.subplots()
workingCount = dayFiltered.groupby("workingday")[["user_casual", "user_registered"]].sum()
st.bar_chart(workingCount)


# bar chart perbandingan total penyewaan sepeda di hari holiday and not holiday
st.subheader("Bike rentals holiday & Non-Holiday")
fig6, ax6 = plt.subplots()
holidayCount = dayFiltered.groupby("holiday")[["user_casual", "user_registered"]].sum()
st.bar_chart(holidayCount)
 

# data display, statistik deskriptif
st.subheader(":bar_chart: Filtered Data")
st.dataframe(dayFiltered.style.set_properties(**{'background-color': '#f9f9f9', 'color': 'black'}))

# tambahan info mengenai data
st.subheader(":pushpin: Key Metrics")
col1, col2, col3 = st.columns(3)
col1.metric("Total Rentals", dayFiltered["total_rent"].sum())
col2.metric("Avg Rentals per Day", round(dayFiltered["total_rent"].mean(), 2))
col3.metric("Max Rentals in a Day", dayFiltered["total_rent"].max())

# Download data jika ingin
st.subheader(" Download filtered data")
st.download_button(
    label="Download as CSV",
    data=dayFiltered.to_csv().encode('utf-8'),
    file_name='bike sharing data recap.csv',
    mime='text/csv',
)

# copyright hehe
st.write("\u00A9 2025 Dicoding Indonesia. All Rights Reserved.")