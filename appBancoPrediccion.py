#Importamos lo que vamos a requerir en el proyecto
import pandas as pd
import streamlit as st
from datetime import date
import urllib.request
import ssl
import os
import json

#Parte de codigo que conexion
def allowSelfSignedHttps(allowed):
    if allowed and not os.environ.get('PYTHONHTTPSVERIFY', '') and getattr(ssl, '_create_unverified_context', None):
        ssl._create_default_https_context = ssl._create_unverified_context
    allowSelfSignedHttps(True)

#Importancion de del archivo de excel
data = pd.read_csv("Herramientas3_2023_banco.csv.csv")

#Creacion de el dataframe
df = pd.DataFrame(data)

#Realizamos la limpieza de nuestro dataframe para los archivos duplicados y lo convertimos en lista para utilizarlo en los selectbox
listaAge = df["age"].drop_duplicates().tolist() #numerico
listaJob = df["job"].drop_duplicates().tolist()
listaMarital = df["marital"].drop_duplicates().tolist()
listaEducation = df["education"].drop_duplicates().tolist()
listaDefault = df["default"].drop_duplicates().tolist()
listaHousing = df["housing"].drop_duplicates().tolist()
listaLoan = df["loan"].drop_duplicates().tolist()
listaContact = df["contact"].drop_duplicates().tolist()
listaDate = df["month"].drop_duplicates().tolist()
listaDuration = df["duration"].drop_duplicates().tolist() #numerico
listaCampaign = df["campaign"].drop_duplicates().tolist() #numerico
listaPdays = df["pdays"].drop_duplicates().tolist() #numerico
listaPrevious = df["previous"].drop_duplicates().tolist() #numerico
listaPoutcome = df["poutcome"].drop_duplicates().tolist()
listaRate = df["emp.var.rate"].drop_duplicates().tolist() #numerico
listaPriceIdx = df["cons.price.idx"].drop_duplicates().tolist() #numerico
listaConfIdx = df["cons.conf.idx"].drop_duplicates().tolist() #numerico
listaEuribor3m = df["euribor3m"].drop_duplicates().tolist() #numerico
listaEmployed = df["nr.employed"].drop_duplicates().tolist() #numerico

#Vemos los valores que hay en los numericos para saber que rangos pondremos en nuestro formulario

print("valores age", listaAge, "\n", "Valores Duration:", listaDuration, "\n",
      "Valores campaign:", listaCampaign, "\n", "Valores Pdays:", listaPdays, "\n",
      "Valores previous:", listaPrevious, "\n", "Valores rate:", listaRate, "\n",
      "Valores priceIdx:", listaPriceIdx, "\n", "Valores confIdx:", listaConfIdx, "\n",
      "Valores Euribor3m:", listaEuribor3m, "\n", "Valores employed:", listaEmployed)

#Ponemos titulo a la pagina
st.title("PRUEBA SI ERES APTO PARA EL CREDITO:)")

#Realizacion de el formulario con las listas que limpiamos y realizamos anteriormente
RespAge = st.slider("Indique su edad", 0, 98)
RespJob = st.selectbox("Seleccione su trabajo", listaJob)
RespMarital = st.selectbox("Seleccione su estado civil", listaMarital)
RespEducation = st.selectbox("Seleccione su nivel educativo", listaEducation)
RespDefault = st.selectbox("Seleccione una opción", listaDefault)
RespHousing = st.selectbox("Cuenta con vivienda propia", listaHousing)
RespLoan = st.selectbox("Ha tenido algún préstamo anteriormente", listaLoan)
RespContact = st.selectbox("Seleccione su tipo de contacto", listaContact)
RespDate = st.selectbox("Selecciona una fecha", listaDate)
RespDuration = st.slider("Indique su Duration", 0, 49018)
RespCampaign = st.slider("Indique su Campaign", 0, 56)
RespPdays = st.slider("Indique su pdays", 0, 999)
RespPrevious = st.slider("Indique su Previous", 0, 7)
RespPoutcome = st.selectbox("Seleccione poutcome", listaPoutcome)
RespRate = st.slider("Indique su rate", -3.4, 1.4)
RespPriceIdx = st.slider("Indique su PriceIdx", 92.201, 94.767)
RespConfIdx = st.slider("Indique su ConfIdx", -50.8, -26.9)
RespEuribor3m = st.slider("Indique su Euribor3m", 0.634, 5.045)
RespEmployed = st.slider("Indique su Employed", 4963.6, 5228.1)

#Realizamos la conectividad y el botón que enviará los datos
if st.button('COMPROBAR'):
        data = {
            "Inputs": {
                "data": [
                    {
                        "age": RespAge,
                        "job": RespJob,
                        "marital": RespMarital,
                        "education": RespEducation,
                        "default": RespDefault,
                        "housing": RespHousing,
                        "loan": RespLoan,
                        "contact": RespContact,
                        "month": RespDate,
                        "duration": RespDuration,
                        "campaign": RespCampaign,
                        "pdays": RespPdays,
                        "previous": RespPrevious,
                        "poutcome": RespPoutcome,
                        "emp.var.rate": RespRate,
                        "cons.price.idx": RespPriceIdx,
                        "cons.conf.idx": RespConfIdx,
                        "euribor3m": RespEuribor3m,
                        "nr.employed": RespEmployed
                    }
                ]
            },
            "GlobalParameters": {
                "method": "predict"
            }
        }

        body = str.encode(json.dumps(data))
        #Datos del modelo a consumir
        url = 'https://fca-regression.eastus2.inference.ml.azure.com/score'
        api_key = 'AnVcIXbYyV9KbCKmAGmbV2gNhpMAdmXg'
        if not api_key:
            raise Exception("A key should be provided to invoke the endpoint")
        headers = {'Content-Type': 'application/json', 'Authorization': ('Bearer ' + api_key),
                   'azureml-model-deployment': 'fca-deploy2'}

        req = urllib.request.Request(url, body, headers)
        #Realizamos envio de mensaje de aceptación o negacion segun sea la respuesta que recibamos del modelo
        try:
            response = urllib.request.urlopen(req)
            result = response.read()
            print(data)
            result = str(result)
            if "yes" in result:
                st.success("¡FELICICIDADES! Usted si es apto para recibir un credito:)")
            if "no" in result:
                n = SystemError("¡LO SENTIMOS! Usted no es apto para recibir un credito en este momento:(")
                st.exception(n)

        except urllib.error.HTTPError as error:
            print("The request failed with status code: " + str(error.code))
            print(error.info())
            print(error.read().decode("utf8", 'ignore'))