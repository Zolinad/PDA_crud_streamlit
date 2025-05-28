import streamlit as st
from gsheets import add_contato, listar_contatos

st.set_page_config(page_title="Agenda", layout="centered")
st.title("📇 Agenda de Contatos (Google Sheets)")

# Formulário de cadastro
with st.form("form_contato"):
    nome = st.text_input("Nome")
    email = st.text_input("Email")
    enviar = st.form_submit_button("Salvar")

    if enviar:
        if nome and email:
            add_contato(nome, email)
            st.success("Contato salvo com sucesso!")
        else:
            st.warning("Preencha todos os campos.")

# Listagem de contatos
st.subheader("📋 Contatos cadastrados")
dados = listar_contatos()

if dados:
    for contato in dados:
        nome = contato.get("nome", "Sem nome")
        email = contato.get("email", "Sem email")
        st.write(f"**{nome}** - {email}")
else:
    st.info("Nenhum contato cadastrado.")
