# -*- coding: utf-8 -*-
"""
Created on Thu Sep 12 14:04:54 2024

@author: jgabriel
"""

import streamlit as st
import pandas as pd
from google.oauth2 import service_account
from gspread_pandas import Spread, Client
from gspread_dataframe import set_with_dataframe

# Definir escopos para Google Sheets e Google Drive
scope = [
    "https://spreadsheets.google.com/feeds",
    "https://www.googleapis.com/auth/drive"
]

# Carregar as credenciais de acesso do arquivo JSON
creds = service_account.Credentials.from_service_account_info(st.secrets["gcp_service_account"], scopes= scope)
# Autenticar com o Google Sheets (conectar as credencias)
client = Client(scope=scope, creds=creds)
spreadsheetname = "atividades"
spread = Spread(spreadsheetname, client = client)
#link com a planilha do google sheets
sheet = client.open(spreadsheetname).sheet1

val = sheet.get_all_values()
# fr é a variavel da planilha do google sheets
fr = pd.DataFrame(val)
#separa a primeira linha da planilha google sheets
cab = fr.iloc[0]
#fazendo com que a planilha seja lida a partir da primeira linha
fr = fr[1:]
#seta as colunas
fr.columns = cab



if 'jsoninput' not in st.session_state:
    st.session_state.jsoninput = None
        
def adicionar(Residencial, Atividade, Registros):
    entrega = {
        'residencial': Residencial,
        'atividade': Atividade,
        'registros': Registros
    }

    st.session_state.jsoninput = pd.concat(
        [st.session_state.jsoninput,
         pd.DataFrame(entrega, index=[0])],
        ignore_index=True)

    return st.session_state.jsoninput

st.header('Controle de Atividades')

with st.form('dados', clear_on_submit=True, border=True): 
    
    st.subheader('Atividade')
    op = st.selectbox('Escolha um dos residencias abaixo:',
             ('Virgílio Távora I', 'Virgílio Távora II', 'Virgílio Távora III',
             'Bonaparte Viana', 'Blanchard Girão', 'Demócrito Dummar I', 'Demócrito Dummar II', 'Demócrito Dummar III'))
    atv = st.selectbox('Escolha uma atividade',
                   ('Atv 01', 'Atv 02', 'Atv 03', 'Atv 04',
                    'Atv 08', 'Atv 09', 'Atv 10', 'Atv 11',
                    'Atv 12', 'Atv 13', 'Atv 14', 'Atv 15',
                    'Atv 16', 'Atv 17', 'Atv 18'))
    
    
    col1, col2 = st.columns([2, 2])
    with col1:
        st.subheader('Registros')
        ch1 = st.checkbox('Registro Fotográfico')
        ch2 = st.checkbox('Folders/Cartilhas/Apostilas')
        ch3 = st.checkbox('Lista de Presença')
        ch4 = st.checkbox('Ata da Reunião')
    with col2:
        st.subheader('')
        ch5 = st.checkbox('Registro de Avaliação')
        ch6 = st.checkbox('Vídeos(links)')
        ch7 = st.checkbox('Slides')
        ch8 = st.checkbox('Outros(cartazes/convites)')
    
    if ch1:
        st.session_state.jsoninput = adicionar(op, atv, 'Registro Fotográfico')
    if ch2:
        st.session_state.jsoninput = adicionar(op, atv, 'Folders/Cartilhas/Apostilas')
    if ch3:
        st.session_state.jsoninput = adicionar(op, atv, 'Lista de Presença')
    if ch4:
        st.session_state.jsoninput = adicionar(op, atv, 'Ata da Reunião')
    if ch5:
        st.session_state.jsoninput = adicionar(op, atv, 'Registro de Avaliação')
    if ch6:
        st.session_state.jsoninput = adicionar(op, atv, 'Vídeos(links)')
    if ch7:
        st.session_state.jsoninput = adicionar(op, atv, 'Slides')
    if ch8:
        st.session_state.jsoninput = adicionar(op, atv, 'Outros(cartazes/convites)')
    
    st.subheader('Adicionar Entrega')
    
    st.session_state.jsoninput = pd.DataFrame(st.session_state.jsoninput)


    if st.form_submit_button('Adicionar'):
        set_with_dataframe(sheet,
                           st.session_state.jsoninput,
                           row=len(sheet.col_values(1)) + 1,
                           include_column_header=False)
        st.success('Dados enviados com sucesso!')

