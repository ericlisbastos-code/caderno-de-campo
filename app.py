import streamlit as st
import pandas as pd
from datetime import date
from from streamlit_gsheets_connection import GSheetsConnection

# Configuração da página
st.set_page_config(page_title="Caderno de Campo Digital", layout="wide", page_icon="🌱")

st.title("🌱 Caderno de Campo Digital")
st.markdown("---")

# Conexão com Google Sheets usando as credenciais do Secrets
conn = st.connection("gsheets", type=GSheetsConnection)

# Função para carregar os dados sempre atualizados
def get_data():
    return conn.read(ttl=0)

# Carregamento inicial dos dados
try:
    df = get_data()
except Exception as e:
    st.error("Erro ao conectar com a planilha. Verifique se as colunas na Linha 1 estão corretas.")
    st.stop()

# Abas para organizar o App
tab1, tab2 = st.tabs(["📊 Visualizar Registros", "📝 Novo Registro"])

with tab1:
    st.subheader("Histórico de Atividades")
    if not df.empty:
        st.dataframe(df, use_container_width=True)
    else:
        st.info("A planilha está vazia. Comece registrando uma atividade na aba ao lado.")

with tab2:
    st.subheader("Cadastrar Nova Operação")
    with st.form("form_registro", clear_on_submit=True):
        col1, col2 = st.columns(2)
        
        with col1:
            data_reg = st.date_input("Data da Atividade", date.today())
            talhao = st.text_input("Talhão", placeholder="Ex: Área Norte")
            cultura = st.text_input("Cultura", placeholder="Ex: Milho")
            
        with col2:
            atividade = st.selectbox("Atividade", ["Plantio", "Pulverização", "Adubação", "Colheita", "Roçada", "Outros"])
            responsavel = st.text_input("Responsável Técnico")
            
        obs = st.text_area("Observações Adicionais")
        
        submit = st.form_submit_button("✅ Salvar no Google Sheets")

        if submit:
            if talhao and cultura:
                # Criar nova linha com os nomes EXATOS das colunas da sua planilha
                nova_linha = pd.DataFrame([{
                    "Data": data_reg.strftime("%d/%m/%Y"),
                    "Talhão": talhao,
                    "Cultura": cultura,
                    "Atividade": atividade,
                    "Responsável": responsavel,
                    "Observações": obs
                }])
                
                # Concatenar dados novos aos antigos e atualizar
                df_final = pd.concat([df, nova_linha], ignore_index=True)
                conn.update(data=df_final)
                st.success("Dados enviados com sucesso!")
                st.rerun()
            else:
                st.warning("Por favor, preencha o Talhão e a Cultura antes de salvar.")
 
