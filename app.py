import streamlit as st
import pandas as pd
from datetime import date
from streamlit_gsheets_connection import GSheetsConnection

# Configuração da página
st.set_page_config(page_title="Caderno de Campo Digital", layout="wide", page_icon="🌱")

st.title("🌱 Caderno de Campo Digital")

# Conexão com o Google Sheets usando as credenciais do Secrets
conn = st.connection("gsheets", type=GSheetsConnection)

# Função para carregar os dados sempre atualizados
def get_data():
    return conn.read(ttl=0)

df = get_data()

# Abas para organizar o App
tab1, tab2 = st.tabs(["📋 Visualizar Registros", "📝 Novo Registro"])

with tab1:
    st.subheader("Histórico de Atividades")
    if not df.empty:
        st.dataframe(df, use_container_width=True)
    else:
        st.info("A planilha está vazia ou não foi encontrada.")

with tab2:
    st.subheader("Registrar Nova Operação")
    with st.form("form_registro"):
        col1, col2 = st.columns(2)
        
        with col1:
            data_obs = st.date_input("Data", date.today())
            talhao = st.text_input("Talhão", placeholder="Ex: Área Norte 01")
            cultura = st.text_input("Cultura", placeholder="Ex: Soja, Milho...")
            
        with col2:
            atividade = st.selectbox("Atividade", ["Plantio", "Adubação", "Pulverização", "Colheita", "Outros"])
            responsavel = st.text_input("Responsável")
            obs = st.text_area("Observações Adicionais")
        
        botao_salvar = st.form_submit_button("Salvar na Planilha")

        if botao_salvar:
            if talhao and cultura:
                # Criar nova linha
                nova_linha = pd.DataFrame([{
                    "Data": data_obs.strftime("%d/%m/%Y"),
                    "Talhão": talhao,
                    "Cultura": cultura,
                    "Atividade": atividade,
                    "Responsável": responsavel,
                    "Observações": obs
                }])
                
                # Adicionar aos dados existentes
                df_atualizado = pd.concat([df, nova_linha], ignore_index=True)
                
                # Enviar para o Google Sheets
                conn.update(data=df_atualizado)
                
                st.success("✅ Registro salvo com sucesso!")
                st.rerun()
            else:
                st.warning("⚠️ Preencha os campos obrigatórios (Talhão e Cultura).")

st.sidebar.info("Conectado à planilha: 'Caderno de Campo'")
