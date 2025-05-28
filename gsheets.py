import gspread
import json
import os
import streamlit as st  # Faltava essa importação
from google.oauth2.service_account import Credentials  # Biblioteca moderna para autenticação

def get_client():
    scope = [
        "https://www.googleapis.com/auth/spreadsheets",
        "https://www.googleapis.com/auth/drive"
    ]
    
    # Verifica se está no Streamlit Cloud ou local
    if 'GOOGLE_SHEETS_CREDENTIALS_JSON' in os.environ:
        creds_dict = json.loads(os.getenv("GOOGLE_SHEETS_CREDENTIALS_JSON"))
    else:
        with open('credentials.json') as f:
            creds_dict = json.load(f)
    
    creds = Credentials.from_service_account_info(creds_dict, scopes=scope)
    return gspread.authorize(creds)

def get_sheet():
    try:
        client = get_client()
        sheet = client.open("basecontatos").sheet1
        return sheet
    except Exception as e:
        st.error(f"Erro ao acessar a planilha: {e}")
        return None

def add_contato(nome, email):
    sheet = get_sheet()
    if sheet:
        try:
            sheet.append_row([nome, email])
        except Exception as e:
            st.error(f"Erro ao adicionar contato: {e}")

def listar_contatos():
    sheet = get_sheet()
    if sheet:
        try:
            return sheet.get_all_records()
        except Exception as e:
            st.error(f"Erro ao listar contatos: {e}")
            return []
    return []
