import gspread
import json
import os
from google.oauth2.service_account import Credentials  # Atualizado para nova biblioteca

def get_client():
    # Escopos atualizados para a API mais recente
    scope = [
        "https://www.googleapis.com/auth/spreadsheets",
        "https://www.googleapis.com/auth/drive"
    ]
    
    # Verifica se está no Streamlit Cloud ou local
    if 'GOOGLE_SHEETS_CREDENTIALS_JSON' in os.environ:
        # Para produção no Streamlit Cloud
        creds_dict = json.loads(os.getenv("GOOGLE_SHEETS_CREDENTIALS_JSON"))
    else:
        # Para desenvolvimento local (usando arquivo credentials.json)
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
        sheet.append_row([nome, email])

def listar_contatos():
    sheet = get_sheet()
    if sheet:
        try:
            return sheet.get_all_records()
        except:
            return []
    return []
