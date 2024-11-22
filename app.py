import streamlit as st
import requests
import datetime
import pandas as pd
import numpy as np

pickup_address = st.text_input(
    "Pick-up address: ",
    value = "John F. Kennedy International Airport"
    )

dropoff_address = st.text_input(
    "Dropoff address: ",
    value = "10 Wall St, New York, NY 10005, USA"
    )

api_key = st.secrets.api_key
url = "https://maps.googleapis.com/maps/api/geocode/json"

pickup_params = {
    "address": pickup_address,
    "key": api_key
}

dropoff_params = {
    "address": dropoff_address,
    "key": api_key
}

pickup_response = requests.get(url, pickup_params)
dropoff_response = requests.get(url, dropoff_params)

pickup_datetime = st.date_input(
    "Pick-up date: ",
    datetime.date(2014, 7, 6))
pickup_longitude = pickup_response.json()["results"][0]["geometry"]["location"]["lng"]
pickup_latitude = pickup_response.json()["results"][0]["geometry"]["location"]["lat"]
dropoff_longitude = dropoff_response.json()["results"][0]["geometry"]["location"]["lng"]
dropoff_latitude = dropoff_response.json()["results"][0]["geometry"]["location"]["lat"]
passenger_count = st.number_input(
    "Passenger count: ",
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
