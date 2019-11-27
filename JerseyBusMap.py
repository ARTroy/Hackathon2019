import streamlit as st
import pandas as pd
import csv
from datetime import date
import numpy 
import urllib
import time
from datetime import datetime, timedelta

csv_filename = "bus_data.csv" #new_date6.csv
count = 0
ALL_DATES = []

@st.cache
def from_data_file(filename):
    return pd.read_csv(filename)

@st.cache
def getAllData(csv_data):
    date_current = '' 
    BUS_LAYERS = {'Bus':{}} 
    count = 0
    for key, dataRow in csv_data.groupby(by="Date"):
        this_date = key #date_parts = splitdate(key) date_parts[0]
        if(this_date != date_current):
            date_current = key 
            ALL_DATES.append(key)
            count = 0
        if(this_date in BUS_LAYERS['Bus']):
            BUS_LAYERS['Bus'][this_date][count] = { "type": "HexagonLayer",
                    "data": dataRow,
                    "radius": 200,
                    "elevationScale": 4,
                    "elevationRange": [0, 1000],
                    "pickable": True,
                    "extruded": True
            }
        else :
            BUS_LAYERS['Bus'][this_date] = { count : { "type": "HexagonLayer",
                    "data": dataRow,
                    "radius": 200,
                    "elevationScale": 4,
                    "elevationRange": [0, 1000],
                    "pickable": True,
                    "extruded": True
            }}
        count = count+1
    return BUS_LAYERS
    
csv_data = from_data_file(csv_filename)
first = csv_data.values[count] #st.write()
cur_date = first[0]

ALL_DATA = getAllData(csv_data)
viewport={"latitude": 49.203, "longitude": -2.130, "zoom": 11, "pitch": 30}
iterator_text = st.empty()
chart = st.deck_gl_chart(viewport=viewport)

while True:
    for item in ALL_DATES:
        selected_layers = [layer for layer_name, layer in ALL_DATA["Bus"][item].items()]
        chart.deck_gl_chart(viewport=viewport, layers=selected_layers)
        iterator_text.text(item)
        time.sleep(1)

#def splitdate(date):
#    split = date.split('-')
#    split_years = split[0]
#    split_months = split[1]
#    split_days = split[2]
#    split_hours = split[3]
#    split_date = split_years+'-'+split_months+'-'+split_days+'-'+split_hours
#    return [split_date, split_years, split_months, split_days, split_hours]