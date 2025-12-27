import streamlit as st
import pandas as pd
from datetime import date
from streamlit_gsheets_connection import GSheetsConnection

# Configuração da página
st.set_page_config(page_title="Caderno de Campo Digital", layout="wide", page_icon="🌱")

st.title("🌱 Caderno de Campo Digital")
st.markdown("---")

# Conexão com Google Sheets usando Secrets
conn = st.connection("gsheets", type=GSheetsConnection)

# Função para carregar os dados
def get_data():
    return conn.read(ttl=0)

try:
    df = get_data()
except Exception as e:
    st.error("Erro ao conectar com a planilha. Verifique os Secrets e os cabeçalhos da Linha 1.")
    st.stop()

# Abas do App
tab1, tab2 = st.tabs(["📊 Visualizar Registros", "📝 Novo Registro"])

with tab1:
    st.subheader("Histórico de Atividades")
    if not df.empty:
        st.dataframe(df, use_container_width=True)
    else:
        st.info("Nenhum registro encontrado.")

with tab2:
    st.subheader("Cadastrar Nova Operação")
    with st.form("form_registro", clear_on_submit=True):
        col1, col2 = st.columns(2)
        with col1:
            data_reg = st.date_input("Data", date.today())
            talhao = st.text_input("Talhão")
            cultura = st.text_input("Cultura")
        with col2:
            atividade = st.selectbox("Atividade", ["Plantio", "Pulverização", "Adubação", "Colheita", "Outros"])
            responsavel = st.text_input("Responsável")
        
        obs = st.text_area("Observações")
        submit = st.form_submit_button("✅ Salvar")

        if submit:
            if talhao and cultura:
                nova_linha = pd.DataFrame([{
                    "Data": data_reg.strftime("%d/%m/%Y"),
                    "Talhão": talhao,
                    "Cultura": cultura,
                    "Atividade": atividade,
                    "Responsável": responsavel,
                    "Observações": obs
                }])
                df_final = pd.concat([df, nova_linha], ignore_index=True)
                conn.update(data=df_final)
                st.success("Salvo com sucesso!")
                st.rerun()
