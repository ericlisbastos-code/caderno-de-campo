import streamlit as st
import pandas as pd
from datetime import date, datetime
import uuid

from st_gsheets_connection import GSheetsConnection

st.set_page_config(page_title="Caderno de Campo", layout="centered")
st.title("🥬 Caderno de Campo Digital")

SITIOS = ["Colégio", "Ressaca"]
LOTES = [f"Lote {i}" for i in range(1, 9)]
ATIVIDADES = ["Plantio", "Adubação", "Tratamento", "Irrigação", "Capina", "Colheita"]

# Conexão com Google Sheets (worksheet = aba "registros")
conn = st.connection("gsheets", type=GSheetsConnection)
df = conn.read(worksheet="registros", ttl=0)

COLS = ["ID", "TIMESTAMP", "SITIO", "LOTE", "DATA", "CULTURA", "ATIVIDADE", "OBS", "STATUS", "FOTO"]

# Garantir colunas, mesmo se a planilha estiver vazia
if df is None or df.empty:
    df = pd.DataFrame(columns=COLS)
else:
    for c in COLS:
        if c not in df.columns:
            df[c] = ""

tab1, tab2 = st.tabs(["➕ Novo Registro", "📚 Histórico"])

with tab1:
    with st.form("novo", clear_on_submit=True):
        sitio = st.selectbox("Sítio", SITIOS)
        lote = st.selectbox("Lote", LOTES)
        data_reg = st.date_input("Data", date.today())
        cultura = st.text_input("Cultura (ex: Alface Americana)")
        atividade = st.selectbox("Atividade", ATIVIDADES)
        obs = st.text_area("Observações")
        salvar = st.form_submit_button("Salvar")

    if salvar:
        if not cultura.strip():
            st.error("Preencha a cultura.")
        else:
            status = "Colhido" if atividade == "Colheita" else "Ativo"
            novo = {
                "ID": str(uuid.uuid4())[:8],
                "TIMESTAMP": datetime.now().strftime("%d/%m/%Y %H:%M"),
                "SITIO": sitio,
                "LOTE": lote,
                "DATA": data_reg.strftime("%d/%m/%Y"),
                "CULTURA": cultura.strip(),
                "ATIVIDADE": atividade,
                "OBS": obs.strip(),
                "STATUS": status,
                "FOTO": ""  # reservado (vazio)
            }

            df2 = pd.concat([df, pd.DataFrame([novo])], ignore_index=True)
            conn.update(worksheet="registros", data=df2)

            st.success("Registro salvo.")
            st.rerun()

with tab2:
    # mostra só colunas úteis
    view_cols = ["TIMESTAMP", "SITIO", "LOTE", "DATA", "CULTURA", "ATIVIDADE", "OBS", "STATUS"]
    st.dataframe(df[view_cols], use_container_width=True, hide_index=True)
