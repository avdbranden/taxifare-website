import streamlit as st
import requests
import datetime
import pandas as pd
import numpy as np

pickup_datetime = st.date_input(
    "Pick-up time",
    datetime.date(2014, 7, 6))
pickup_longitude = st.number_input(
    "Pick-up longitude",
    value=-73.950655
    )
pickup_latitude = st.number_input(
    "Pick-up latitude",
    value=40.783282
    )
dropoff_longitude = st.number_input(
    "Dropoff longitude",
    value=-73.984365)
dropoff_latitude = st.number_input(
    "Dropoff latitude",
    value=40.769802
    )
passenger_count = st.number_input(
    "Passenger count",
    min_value=1,
    max_value=8,
    value=1,
    step=1,
    format="%d"
    )

def get_map_data():
    data = {
        'latitude': [pickup_latitude, dropoff_latitude],
        'longitude': [pickup_longitude, dropoff_longitude]
    }
    df = pd.DataFrame(data)
    return df

if st.button('Get fare'):
    # print is visible in the server output, not in the page
    st.balloons()
    st.write('Here is your fare 🎉')
    url = 'https://taxifare-292355993838.europe-west1.run.app/predict'
    params = {
        "pickup_datetime": pickup_datetime ,
        "pickup_longitude": pickup_longitude,
        "pickup_latitude": pickup_latitude,
        "dropoff_longitude": dropoff_longitude,
        "dropoff_latitude": dropoff_latitude,
        "passenger_count": passenger_count
    }
    response = requests.get(url, params)
    fare_amount = response.json()
    st.write(f"{round(fare_amount['fare'], 2)} $")
    st.write("Check your journey")
    df = get_map_data()
    st.map(df)
