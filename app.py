import streamlit as st
import pandas as pd
from streamlit_gsheets_connection import GSheetsConnection

# Configuração básica da página
st.set_page_config(page_title="Caderno de Campo - Teste", layout="wide")

st.title("🌱 Teste de Conexão")

# Tenta estabelecer a conexão usando as credenciais que você colocou no Streamlit Cloud
try:
    conn = st.connection("gsheets", type=GSheetsConnection)
    df = conn.read()
    
    st.success("✅ Conexão estabelecida com sucesso!")
    st.subheader("Dados da sua planilha:")
    st.dataframe(df)

except Exception as e:
    st.error("❌ Erro na conexão.")
    st.info("Verifique se o JSON no 'Secrets' do Streamlit Cloud está formatado corretamente.")
    st.exception(e)
