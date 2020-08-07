# -*- coding: utf-8 -*-
"""
Created on Sat Aug  1 13:25:25 2020

@author: Bellemiss972
"""


#chargement des librairies 
import pandas as pd
import numpy as np
import joblib 
from xgboost import XGBRFClassifier
import streamlit as st
import base64 
from io import BytesIO
import xlsxwriter

#Chargement du modèle enregistré en pkl
model= joblib.load('germancredit.pkl')



#Preparation de la Prediction
def predict(df):
    predictions = model.predict(df)
    return predictions

def predict2(df) :
    predictions1=model.predict_proba(df)
    return(predictions1)

def run():
    
    #Titre de la page
    html_template = """
    <div style = "background-color : #6495ED ; padding:15px">
    <h2 style="color : black; text-align :large ; ">Interface de prédiction pour l'accord d'un prêt</h2>"""
   
    st.markdown(html_template, unsafe_allow_html=True)
    st.write("")   
       
    #Intertitre de présentation
    st.write("Cette interface facilite l'accord d'un prêt et permet d'identifier les personnes considérées comme étant de bons clients. A partir d'une base de données d'un établissement bancaire allemand, nous avons pu entraîner un algorithme de machine learning ayant obtenu 72 % de précision.")
    
    #Création de la sidebar
    selection = st.sidebar.selectbox("Quelle méthode souhaitez-vous utiliser?:",("Prédiction en temps réel","Prédiction par lot"))
    
    #Logo de l'entreprise
    from PIL import Image
    logo = Image.open('logo.png')
    
    #Personnalisation de la sidebar
    st.sidebar.image(logo,use_column_width=True)
    
    st.sidebar.info("Cette application est une démonstration conçue par l'Agence Marketic")
    
    st.sidebar.success('Retrouvez-nous sur http://www.agence-marketic.fr')
    
    #Charger une image pour le thème
    image2 =Image.open('CREDIT.jpg')
    st.sidebar.image(image2,use_column_width=True)
    
    #PERSONNALISATION DE LA PAGE PRINCIPALE
    
    st.subheader("Identification des clients à risques selon les caractéristiques suivantes :")
    
    if selection == "Prédiction en temps réel" :
        
        Age = st.number_input('Age du client',min_value=1,max_value=70, value=30)
        Job= st.selectbox("Indiquez la situation professionnelle",['qualifié', 'non_qualifié', 'haut_qualifié'])
        Checking_account = st.selectbox("Indiquez l'état d'approvisionnement du compte courant du client:",['little','moderate','rich'])
        Sex = st.selectbox("Indiquez le sexe",["male","female"])
        Credit_amount = st.text_input("Indiquez le montant du compte courant du client:", "2000")
        Saving_accounts = st.selectbox("Indiquez l'état d'approvisionnement du compte épargne du client",["little","moderate","rich"])
        Housing = st.selectbox("Indiquez le type de bien immobilier occupé ",["free","own","rent" ])
        Duration = st.slider("Indiquez la durée du prêt:",min_value=3,max_value=94, value=12)
        
        resultat=""
        
        data={'Age':Age,
              'Job':Job,
              'Checking_account':Checking_account,
              'Sex':Sex,
              'Credit_amount': Credit_amount,
              'Saving_accounts':Saving_accounts,
              'Housing': Housing,
              'Duration': Duration}
            
        
        df = pd.DataFrame(data,index=[0])
                 
    #Prediction finale
        
        if st.button("Prédire"):
            
            preds = resultat=model.predict(df)
            if preds == 0:
                st.success("***Il s'agit d'un client à risque.***")
            else:
                st.success("***Il s'agit d'un client sans risque.***")
               
            proba=model.predict_proba(df)
            st.write(proba)
            st.write("Probalité du type de client: o=client à risque, 1=client sans risque") 
          
            
    #Traitement par lot
    
    if selection == 'Prédiction par lot':
        st.write("Afin d'accéder aux résultats de prédiction du présent projet :")
        st.markdown("""[1-Télécharger le fichier de démonstration du projet](https://drive.google.com/uc?export=download&id=1mCg5LF8rBCYhRDDJfndbl5G7N8Iba4aT)""")
        
        batch = st.file_uploader("2-Veuillez charger ci-dessous le fichier de données de démonstration au format.csv:")
        if batch is not None:
            data = pd.read_csv(batch)
            
            predictions=model.predict(data)
           
            #test
            pred=pd.Series(predictions.reshape(data.shape[0],))
            dataframe=pd.DataFrame([[data,predictions]])
            concat=pd.concat([data,pred], axis=1)
            concat.columns=['Age', 'Sex', 'Job', 'Housing', 'Saving_accounts', 'Checking_account', 'Duration','Credit_amount','predictions']
            concat['predictions']=concat['predictions'].map({0:'à risque',1:'sans risque'})
            st.write(concat)
            
            
            def to_excel(concat):
                output = BytesIO()
                writer = pd.ExcelWriter(output, engine='xlsxwriter')
                concat.to_excel(writer, sheet_name='Sheet1')
                writer.save()
                processed_data = output.getvalue()
                return processed_data

            def get_table_download_link(concat):
                
                val = to_excel(concat)
                b64 = base64.b64encode(val)  # val looks like b'...'
                return f'<a href="data:application/octet-stream;base64,{b64.decode()}" download="extract.xlsx">Download xls file</a>' # decode b'abc' => abc

            
            st.markdown(get_table_download_link(concat), unsafe_allow_html=True)


    
if __name__=='__main__': run()