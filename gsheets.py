import gspread # Biblioteca para acessar e manipular planilhas do Google Sheets
import json # Usada para ler e manipular dados em formato JSON (como as credenciais)
import os # Permite acessar variáveis de ambiente (como os secrets no Streamlit)
from oauth2client.service_account import ServiceAccountCredentials 
# Importa a classe que permite autenticação via conta de serviço com credenciais JSON

# Conecta à API do Google usando o conteúdo do secret
def get_client():
    scope = [
        "https://spreadsheets.google.com/feeds",
        "https://www.googleapis.com/auth/drive"
    ]
    creds_dict = json.loads(os.getenv("GOOGLE_SHEETS_CREDENTIALS_JSON"))
    creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_dict, scope)
    return gspread.authorize(creds)

# Acessa a planilha e retorna a primeira aba
def get_sheet():
    client = get_client()
    sheet = client.open("basecontatos").sheet1  # Nome exato da planilha criada!!!!
    return sheet

# Adiciona um novo contato à planilha
def add_contato(nome, email):
    sheet = get_sheet()
    sheet.append_row([nome, email])

# Lista todos os contatos da planilha
def listar_contatos():
    sheet = get_sheet()
    rows = sheet.get_all_records()  # Retorna como lista de dicionários
    return rows