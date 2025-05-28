import gspread
import json
import os
from google.oauth2.service_account import Credentials
import streamlit as st

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

        dados = sheet.get_all_values()
        if not dados or dados[0] != ["nome", "email"]:
            sheet.clear()
            sheet.append_row(["nome", "email"])

        return sheet
    except Exception as e:
        st.error(f"Erro ao acessar a planilha: {e}")
        return None

def contato_existe(nome, email, registros):
    for contato in registros:
        if contato.get("nome", "").strip().lower() == nome.strip().lower() and \
           contato.get("email", "").strip().lower() == email.strip().lower():
            return True
    return False

def add_contato(nome, email):
    sheet = get_sheet()
    if sheet:
        registros = sheet.get_all_records()
        if contato_existe(nome, email, registros):
            st.warning("Contato já existe na planilha.")
        else:
            sheet.append_row([nome, email])

def listar_contatos():
    sheet = get_sheet()
    if sheet:
        try:
            return sheet.get_all_records()
        except:
            return []
    return []
