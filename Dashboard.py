
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

# Function to load the data
@st.cache_data
def load_data():
    df = pd.read_csv('day.csv')
    df.rename(columns={
        'instant': 'Instant',
        'dteday': 'Date_Day',
        'season': 'Season',
        'yr': 'Year',
        'mnth': 'Month',
        'hr': 'Hour',
        'holiday': 'Holiday',
        'weekday': 'Weekday',
        'workingday': 'Working_Day',
        'weathersit': 'Weather_Situation',
        'temp': 'Temperature',
        'atemp': 'Apparent_Temperature',
        'hum': 'Humidity',
        'windspeed': 'Wind_Speed',
        'casual': 'Casual_Users',
        'registered': 'Registered_Users',
        'cnt': 'Total_Count'
    }, inplace=True)
    return df
    
def plot_yearly_trend(df):
    st.markdown('##### Tren Tahunan Penggunaan Sepeda')
    yearly_usage = df.groupby('Year')['Total_Count'].sum().reset_index()
    yearly_usage['Year'] = yearly_usage['Year'].map({0: '2011', 1: '2012'})

    fig, ax = plt.subplots(figsize=(8, 6))
    ax.plot(yearly_usage['Year'], yearly_usage['Total_Count'], marker='o')
    ax.set_xlabel('Tahun')
    ax.set_ylabel('Jumlah Total Penggunaan Sepeda')
    st.pyplot(fig)

def plot_usage_comparison(df):
    st.markdown('##### Rata-Rata Penggunaan Sepeda: Hari Kerja vs Hari Libur')
    usage_by_workingday = df.groupby('Working_Day')['Total_Count'].mean().reset_index()
    usage_by_workingday['Day_Type'] = usage_by_workingday['Working_Day'].map({0: 'Weekend/Holiday', 1: 'Weekday'})

    fig, ax = plt.subplots(figsize=(8, 6))
    # bar_colors = ['skyblue', 'sandybrown']
    sns.barplot(data=usage_by_workingday, x='Day_Type', y='Total_Count')
    ax.set_xlabel('Tipe Hari')
    ax.set_ylabel('Rata-Rata Jumlah Penggunaan')
    st.pyplot(fig)

def plot_actual_temp(df):
    st.markdown('##### Pengaruh Suhu Aktual Terhadap Jumlah Pengguna Sepeda')
    fig, ax = plt.subplots(figsize=(8, 6))
    sns.scatterplot(x='Temperature', y='Total_Count', data=df)
    ax.set_xlabel('Suhu (°C)')
    ax.set_ylabel('Jumlah Pengguna Sepeda')
    st.pyplot(fig)

def plot_apparent_temp(df):
    st.markdown('##### Pengaruh Suhu yang Dirasakan Terhadap Jumlah Pengguna Sepeda')
    fig, ax = plt.subplots(figsize=(8, 6))
    sns.scatterplot(x='Apparent_Temperature', y='Total_Count', data=df)
    ax.set_xlabel('Suhu (°C)')
    ax.set_ylabel('Jumlah Pengguna Sepeda')
    st.pyplot(fig)

def plot_humidity(df):
    st.markdown('##### Pengaruh Kelembapan Terhadap Jumlah Pengguna Sepeda')
    fig, ax = plt.subplots(figsize=(8, 6))
    sns.scatterplot(x='Humidity', y='Total_Count', data=df)
    ax.set_xlabel('Kelembapan (%)')
    ax.set_ylabel('Jumlah Pengguna Sepeda')
    st.pyplot(fig)

def plot_wind_speed(df):
    st.markdown('##### Pengaruh Kecepatan Angin Terhadap Jumlah Pengguna Sepeda')
    fig, ax = plt.subplots(figsize=(8, 6))
    sns.scatterplot(x='Wind_Speed', y='Total_Count', data=df)
    ax.set_xlabel('Kecepatan Angin (m/s)')
    ax.set_ylabel('Jumlah Pengguna Sepeda')
    st.pyplot(fig)

def plot_by_type_usage(df):
    st.markdown('##### Perbandingan Distribusi Pengguna Terdaftar vs Tidak Terdaftar')

    fig, ax = plt.subplots(figsize=(8, 6))
    bins = np.linspace(0, max(df['Registered_Users'].max(), df['Casual_Users'].max()), 30)

    sns.histplot(df['Registered_Users'], bins=bins, kde=True, stat='density', common_norm=True, label='Terdaftar', ax=ax)
    sns.histplot(df['Casual_Users'], bins=bins, kde=True, stat='density', common_norm=True, label='Tidak Terdaftar', ax=ax)

    ax.set_xlabel('Jumlah Penggunaan Sepeda')
    ax.set_ylabel('Densitas')
    ax.legend()
    st.pyplot(fig)
    
def show_user_statistics(df):
    st.markdown("##### Pengguna Terdaftar")
    max_registered = df['Registered_Users'].max()        
    min_registered = df['Registered_Users'].min()
    total_registered = df['Registered_Users'].sum()
        
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric(label="Max (Days)", value=max_registered)
    with col2:
        st.metric(label="Min (Days)", value=min_registered)
    with col3:
        st.metric(label="Total", value=total_registered)
    
    st.markdown("##### Pengguna Tidak Terdaftar")
    max_casual = df['Casual_Users'].max()
    min_casual = df['Casual_Users'].min()
    total_casual = df['Casual_Users'].sum()
        
    col4, col5, col6 = st.columns(3)
    with col4:
        st.metric(label="Max (Days)", value=max_casual)
    with col5:
        st.metric(label="Min (Days)", value=min_casual)
    with col6:
        st.metric(label="Total", value=total_casual)
        
def plot_average_usage(df):
    st.markdown('##### Penggunaan Sepeda Rata-Rata Per Hari')
    df['Date_Day'] = pd.to_datetime(df['Date_Day'])
    daily_avg = df.set_index('Date_Day').resample('D').mean()

    fig, ax = plt.subplots(figsize=(14, 7))
    ax.plot(daily_avg.index, daily_avg['Registered_Users'], label='Terdaftar')
    ax.plot(daily_avg.index, daily_avg['Casual_Users'], label='Tidak Terdaftar')

    ax.set_xlabel('Tanggal')
    ax.set_ylabel('Rata-Rata Jumlah Penggunaan')
    ax.legend(['Terdaftar', 'Tidak Terdaftar'])
    ax.grid(True)
    st.pyplot(fig)

def plot_holiday_usage(df):
    st.markdown('##### Penggunaan Sepeda: Hari Libur vs Hari Non-Libur')

    fig, ax = plt.subplots(figsize=(8, 6))
    # box_color = ['skyblue', 'sandybrown']
    sns.boxplot(x='Holiday', y='Total_Count', data=df, ax=ax)
    ax.set_title('Penggunaan Sepeda: Hari Libur vs Hari Non-Libur')
    ax.set_xticklabels(['Non-Libur', 'Libur'])
    ax.set_ylabel('Jumlah Penggunaan Sepeda')
    st.pyplot(fig)

def plot_usage_by_weather(df):
    st.markdown('##### Rata-Rata Penggunaan Sepeda Berdasarkan Kondisi Cuaca')

    average_usage_by_weather = df.groupby('Weather_Situation')['Total_Count'].mean().reset_index()
    average_usage_by_weather['Weather_Situation'] = average_usage_by_weather['Weather_Situation'].map(
        {1: 'Clear', 2: 'Mist/Cloudy', 3: 'Light Snow/Rain', 4: 'Heavy Rain/Snow'})

    fig, ax = plt.subplots(figsize=(10, 6))
    sns.barplot(x='Weather_Situation', y='Total_Count', data=average_usage_by_weather, ax=ax)
    ax.set_title('Rata-Rata Penggunaan Sepeda Berdasarkan Kondisi Cuaca')
    ax.set_xlabel('Kondisi Cuaca')
    ax.set_ylabel('Rata-Rata Jumlah Penggunaan Sepeda')
    ax.set_xticklabels(ax.get_xticklabels(), rotation=45)
    st.pyplot(fig)

#Main app
def main():
    st.title('Bike Sharing Data Analysis Dashboard')

    df = load_data()
    if st.checkbox('Show raw data'):
        st.write(df.head())

    if st.checkbox('Show data description'):
        st.write(df.describe())
        
    st.markdown('<br>', unsafe_allow_html=True)
    plot_yearly_trend(df)
    st.markdown('<br>', unsafe_allow_html=True)
    plot_usage_comparison(df)

    st.markdown('<br>', unsafe_allow_html=True)
    col1, col2 = st.columns([1,1])
    with col1:
        plot_actual_temp(df)
    with col2:
        plot_apparent_temp(df)
        
    st.markdown('<br>', unsafe_allow_html=True)
    col3, col4 = st.columns(2)
    with col3:
        plot_humidity(df)
    with col4:
        plot_wind_speed(df)

    st.markdown('<br>', unsafe_allow_html=True)
    show_user_statistics(df)
    plot_by_type_usage(df)
    st.markdown('<br>', unsafe_allow_html=True)
    plot_average_usage(df)
    st.markdown('<br>', unsafe_allow_html=True)
    plot_holiday_usage(df)
    st.markdown('<br>', unsafe_allow_html=True)
    plot_usage_by_weather(df)

# Run the main app
if __name__ == "__main__":
    main()
