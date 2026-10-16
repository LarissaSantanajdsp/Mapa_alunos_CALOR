import base64
import json
import urllib.parse
import pandas as pd
import plotly.graph_objects as go
import requests
import streamlit as st

# Configuração da página
st.set_page_config(
    page_title="Mapa de Evolução - Movimento Calor",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Estilos do Movimento Calor
BG_COLOR = "#F2F0E4"
TEXT_COLOR = "#4E2C1C"
ACCENT_COLOR = "#E65100"
SECONDARY_COLOR = "#8B4513"

# Paleta Refinada Movimento Calor
CORES_CALOR_REFINADA = [
    "#E65100",
    "#2E7D32",
    "#4E2C1C",
    "#1565C0",
    "#D4A574",
    "#C62828",
    "#FF8F00",
    "#6A1B9A",
    "#AD1457",
    "#37474F",
]

# --- Configurações do GitHub (Banco de Dados) ---
GITHUB_USER = "LarissaSantanajdsp"
GITHUB_REPO = "Mapa_alunos_CALOR"
DATA_FILE_PATH = "dados_alunos.json"
LOGO_FILE_NAME = "Colorlogo-nobackground(1).jpg"
BASE_URL = "https://mapaalunoscalor-fozyfgucjj7skfkjfscwyt.streamlit.app/"

try:
  GITHUB_TOKEN = st.secrets["GITHUB_TOKEN"]
except:
  GITHUB_TOKEN = None


def carregar_logo_github():
  if not GITHUB_TOKEN:
    return None
  url = f"https://api.github.com/repos/{GITHUB_USER}/{GITHUB_REPO}/contents/{LOGO_FILE_NAME}"
  headers = {"Authorization": f"token {GITHUB_TOKEN}"}
  try:
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
      content = response.json()
      return content["content"]
  except:
    pass
  return None


def carregar_dados_github():
  if not GITHUB_TOKEN:
    return {}
  url = f"https://api.github.com/repos/{GITHUB_USER}/{GITHUB_REPO}/contents/{DATA_FILE_PATH}"
  headers = {"Authorization": f"token {GITHUB_TOKEN}"}
  try:
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
      content = response.json()
      decoded_data = base64.b64decode(content["content"]).decode("utf-8")
      return json.loads(decoded_data)
  except:
    pass
  return {}


def salvar_dados_github(dados):
  if not GITHUB_TOKEN:
    return False
  url = f"https://api.github.com/repos/{GITHUB_USER}/{GITHUB_REPO}/contents/{DATA_FILE_PATH}"
  headers = {"Authorization": f"token {GITHUB_TOKEN}"}
  sha = None
  get_response = requests.get(url, headers=headers)
  if get_response.status_code == 200:
    sha = get_response.json()["sha"]
  content_json = json.dumps(dados, ensure_ascii=False, indent=2)
  encoded_content = base64.b64encode(content_json.encode("utf-8")).decode(
      "utf-8"
  )
  payload = {"message": "Atualização automática", "content": encoded_content}
  if sha:
    payload["sha"] = sha
  requests.put(url, headers=headers, json=payload)
  return True


# Inicialização de dados
if "alunos_pilares" not in st.session_state:
  st.session_state.alunos_pilares = carregar_dados_github()

# Captura de parâmetros de URL de forma compatível
aluno_selecionado_url = st.query_params.get("aluno", None)

st.markdown(
    f"""
    <style>
        body {{ background-color: {BG_COLOR}; }}
        .main {{ background-color: {BG_COLOR}; }}
        h1 {{ color: {TEXT_COLOR}; text-align: center; font-family: 'Arial Black'; }}
        .stButton>button {{ background-color: {ACCENT_COLOR}; color: white; border-radius: 5px; }}
    </style>
""",
    unsafe_allow_html=True,
)


def criar_grafico_radar(aluno_nome, pontos):
  fig = go.Figure()
  pilares = ["Clareza", "Impacto", "Visão", "Conexão"]
  for i, p in enumerate(pontos):
    color = CORES_CALOR_REFINADA[i % len(CORES_CALOR_REFINADA)]
    fig.add_trace(
        go.Scatterpolar(
            r=[p[1], p[2], p[3], p[4], p[1]],
            theta=pilares + [pilares[0]],
            fill="toself",
            name=p[0],
            line=dict(color=color, width=4),
            marker=dict(size=10),
            fillcolor=(
                f"rgba{tuple(list(int(color.lstrip('#')[i:i+2], 16) for i in (0, 2, 4)) + [0.1])}"
            ),
        )
    )

  logo_
