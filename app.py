import streamlit as st
import pandas as pd
from datetime import date, datetime
import uuid
import gspread
from google.oauth2.service_account import Credentials

st.set_page_config(page_title="Caderno de Campo", layout="centered")
st.title("🥬 Caderno de Campo Digital")

# ---- AUTH GOOGLE SHEETS ----
scope = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive"
]

creds = Credentials.from_service_account_info(
    st.secrets["gcp_service_account"],
    scopes=scope
)

gc = gspread.authorize(creds)

# ABRA A PLANILHA PELO NOME EXATO
sh = gc.open("Caderno de Campo")
ws = sh.sheet1

# ---- LEITURA ----
data = ws.get_all_records()
df = pd.DataFrame(data)

# ---- FORM ----
with st.form("registro"):
    sitio = st.selectbox("Sítio", ["Colégio", "Ressaca"])
    lote = st.selectbox("Lote", [f"Lote {i}" for i in range(1, 9)])
    cultura = st.text_input("Cultura")
    atividade = st.selectbox("Atividade", ["Plantio", "Adubação", "Tratamento", "Colheita"])
    obs = st.text_area("Observações")
    salvar = st.form_submit_button("Salvar")

if salvar:
    ws.append_row([
        str(uuid.uuid4())[:8],
        datetime.now().strftime("%d/%m/%Y %H:%M"),
        sitio,
        lote,
        cultura,
        atividade,
        obs
    ])
    st.success("Registro salvo")

st.divider()
st.dataframe(df, use_container_width=True)
