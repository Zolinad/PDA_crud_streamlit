import gspread
import json
import os
from google.oauth2.service_account import Credentials
import streamlit as st  # necessário aqui para exibir erros

def get_client():
    scope = [
        "https://www.googleapis.com/auth/spreadsheets",
        "https://www.googleapis.com/auth/drive"
    ]

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

        # Verifica se os títulos já existem
        dados = sheet.get_all_values()
        if not dados or dados[0] != ["nome", "email"]:
            sheet.clear()
            sheet.append_row(["nome", "email"])

        return sheet
    except Exception as e:
        st.error(f"Erro ao acessar a planilha: {e}")
        return None

def add_contato(nome, email):
    sheet = get_sheet()
    if sheet:
        sheet.append_row([nome, email])

def listar_contatos():
    sheet = get_sheet()
    if sheet:
        try:
            dados = sheet.get_all_records()
            return dados
        except:
            return []
    return []
