import gspread
import json
import os
import streamlit as st
from google.oauth2.service_account import Credentials

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
        return sheet
    except Exception as e:
        st.error(f"Erro ao acessar a planilha: {e}")
        return None

def inicializar_planilha():
    sheet = get_sheet()
    if sheet:
        primeira_linha = sheet.row_values(1)
        if not primeira_linha or primeira_linha != ["nome", "email"]:
            sheet.clear()
            sheet.append_row(["nome", "email"])

def add_contato(nome, email):
    inicializar_planilha()
    sheet = get_sheet()
    if sheet:
        sheet.append_row([nome, email])

def listar_contatos():
    inicializar_planilha()
    sheet = get_sheet()
    if sheet:
        try:
            return sheet.get_all_records()
        except:
            return []
    return []
