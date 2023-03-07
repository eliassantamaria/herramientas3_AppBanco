#Importamos lo que vamos a requerir en el proyecto
import pandas as pd
import streamlit as st
import pickle
from datetime import date
import urllib.request
import ssl
import os
import json

model = pickle.load(open("model.pkl","rb"))

data = {

        "age": 22,
        "job": "technician",
        "marital": "married",
        "education": "high.school",
        "default": "yes",
        "housing": "yes",
        "loan": "yes",
        "contact": "cellular",
        "month": "may",
        "duration": 6545,
        "campaign": 15,
        "pdays": 176,
        "previous": 4,
        "poutcome": "failure",
        "emp.var.rate": -2.12,
        "cons.price.idx": 92.70,
        "cons.conf.idx": -45.13,
        "euribor3m": 2.15,
        "nr.employed": 5037.24
        }   

df = pd.json_normalize(data)

model.predict(df)

st.write(model.predict(df))
