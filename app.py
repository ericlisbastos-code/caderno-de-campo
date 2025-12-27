import streamlit as st
import pandas as pd
from datetime import datetime
from streamlit_gsheets import GSheetsConnection

st.set_page_config(page_title="Caderno de Campo Digital", layout="wide")
st.title("🥬 Caderno de Campo Digital")

conn = st.connection("gsheets", type=GSheetsConnection)

SHEET_ID = "1IBA7XcjXzH9YiWVjdIf2D7oZh3SYyGohG4EAuem16FM"
WORKSHEET = "Página1"  # troque se sua aba tiver outro nome

df = conn.read(spreadsheet=SHEET_ID, worksheet=WORKSHEET)
st.dataframe(df, use_container_width=True)

st.divider()
st.subheader("Novo registro")

with st.form("novo", clear_on_submit=True):
    data = st.date_input("Data", value=datetime.today())
    atividade = st.text_input("Atividade")
    observacao = st.text_input("Observação")
    salvar = st.form_submit_button("Salvar")

if salvar:
    novo = pd.DataFrame(
        [[data.strftime("%Y-%m-%d"), atividade, observacao]],
        columns=df.columns
    )
    df2 = pd.concat([df, novo], ignore_index=True)
    conn.update(spreadsheet=SHEET_ID, worksheet=WORKSHEET, data=df2)
    st.success("Salvo ✅")
