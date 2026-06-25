import streamlit as st
import plotly.graph_objects as go
import pandas as pd
import json
import requests
import base64
import urllib.parse

# Configuração da página
st.set_page_config(page_title="Avaliação por Pilares", layout="wide", initial_sidebar_state="expanded")

# Estilos do Movimento Calor
BG_COLOR = '#F2F0E4'
TEXT_COLOR = '#4E2C1C'
ACCENT_COLOR = '#E65100'
SECONDARY_COLOR = '#8B4513'

# Paleta Refinada Movimento Calor
CORES_CALOR_REFINADA = [
    '#E65100', '#2E7D32', '#4E2C1C', '#1565C0', '#D4A574', 
    '#C62828', '#FF8F00', '#6A1B9A', '#AD1457', '#37474F'
]

# Logo da CALOR em Base64
LOGO_BASE64 = "CiAgICAgICAgPHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHhtbG5zOnhsaW5rPSJodHRwOi8vd3d3LnczLm9yZy8xOTk5L3hsaW5rIiB2ZXJzaW9uPSIxLjEiIHdpZHRoPSIzMjQwIiAKICAgICAgICBoZWlnaHQ9Ijk4OS43MTg0ODAzNjYxMDcyIiB2aWV3Qm94PSIwIDAgMzI0MCA5ODkuNzE4NDgwMzY2MTA3MiI+CgkJCQoJCQk8ZyB0cmFuc2Zvcm09InNjYWxlKDEyLjAwMDAwMDAwMDAwMDAwMikgdHJhbnNsYXRlKDEwLCAxMCkiPgoJCQkJPGRlZnMgaWQ9IlN2Z2pzRGVmczEwMzUiPjxsaW5lYXJHcmFkaWVudCBpZD0iU3ZnanNMaW5lYXJHcmFkaWVudDEwMzgiPjxzdG9wIGlkPSJTdmdqc1N0b3AxMDM5IiBzdG9wLWNvbG9yPSIjZWY0MTM2IiBvZmZzZXQ9IjAiPjwvc3RvcD48c3RvcCBpZD0iU3ZnanNTdG9wMTA0MCIgc3RvcC1jb2xvcj0iI2ZiYjA0MCIgb2Zmc2V0PSIxIj48L3N0b3A+PC9saW5lYXJHcmFkaWVudD48L2RlZnM+PGcgaWQ9IlN2Z2pzRzEwMzYiIGZlYXR1cmVLZXk9Im5hbWVGZWF0dXJlLTAiIHRyYW5zZm9ybT0ibWF0cml4KDIuMzAwMzE0Mjg1NDkzNjU3LDAsMCwyLjMwMDMxNDI4NTQ5MzY1NywtNy40NTMwMjIxNDYwMDA1OTksLTMwLjQ1NjE2MDYxMzQzNTg2KSIgZmlsbD0idXJsKCNTdmdqc0xpbmVhckdyYWRpZW50MTAzOCkiPjxwYXRoIGQ9Ik0xNi4yOCAzMC43NTk5OTk5OTk5OTk5OTggbDAgLTEuMjQgYzAgLTAuMiAwLjE2IC0wLjM2IDAuMzYgLTAuMzYgbDQuNTYgMCBjMC4yIDAgMC4zNiAwLjE2IDAuMzYgMC4zNiBsMCAyLjUyIGMwIDUuODggLTMuMTYgOC4zNiAtOS4xMiA4LjM2IGMtNS41NiAwIC05LjIgLTIuMiAtOS4yIC04LjM2IGwwIC0xMC41MiBjMCAtNS45MiAzLjI0IC04LjI4IDkuMiAtOC4yOCBjNS42NCAwIDkuMTIgMi4xNiA5LjEyIDguMjggbDAgMC44NCBjMCAwLjIgLTAuMTYgMC4zNiAtMC4zNiAwLjM2IGwtNC42IDAgYy0wLjIgMCAtMC4zNiAtMC4xNiAtMC4zNiAtMC4zNiBsMCAtMC42NCBjMCAtMi4yIC0xLjY0IC0zLjEyIC0zLjYgLTMuMTIgbC0wLjQ4IDAgYy0xLjMyIDAgLTIuMiAwLjM2IC0yLjggMS4xNiBjLTAuNTYgMC43NiAtMC43NiAxLjc2IC0wLjc2IDMuMDggbDAgNy45MiBjMCAzLjQ4IDEuOTYgNC4yNCAzLjU2IDQuMjQgbDAuNDggMCBjMi41MiAwIDMuNTYgLTEuNjggMy42NCAtNC4yNCB6IE0xMi4zNiAxNS43MTk5OTk5OTk5OTk5OTkgYy00LjI4IDAgLTYuNzYgMS41MiAtNi43NiA2LjQgbDAgOS42NCBjMCA0LjQ0IDIuMjggNi4wOCIgNi43NiA2LjA4IGM0LjIgMCA2LjcyIC0xLjUyIDYuNzIgLTMuMTIgeiBNMzMuMzIgMTMuODQgYzAuMDQgLTAuMTIgMC4xMiAtMC4yNCAwLjI4IC0wLjI0IGw0Ljk2IDAgYzAuMTYgMCAwLjI0IDAuMTIgMC4yOCAwLjI0IGw2LjkyIDI1LjcyIGMwLjA0IDAuMjQgLTAuMTIgMC40NCAtMC4zNiAwLjQ0IGwtNC41NiAwIGMtMC4xMiAwIC0wLjI0IC0wLjA4IC0wLjI4IC0wLjI0IGwtMS41NiAtNS42IGwtNS44NCAwIGwtMS41MiA1LjYgYy0wLjA0IDAuMTYgLTAuMTIgMC4yNCAtMC4yOCAwLjI0IGwtNC42IDAgYy0wLjI0IDAgLTAuNCAtMC4yIC0wLjM2IC0wLjQ0IHogTTM0LjQ0MDAwMDAwMDAwMDAwNSAyOS4yIGwzLjMyIDAgbC0xLjcyIC02LjA0IHogTTQwLjYgMzEuNTYwMDAwMDAwMDAwMDIgbDEuODQgNiBjMC4wOCAwLjI0IDAuNTIgMC4yIDAuNCAtMC4xMiBsLTYuNCAtMjEuMjggYy0wLjEyIC0wLjUyIC0wLjggLTAuNTYgLTAuOTIgMCBsLTYuMiAyMS4yOCBjLTAuMTIgMC4yOCAwLjMyIDAuNCAwLjQ0IDAuMTYgbDEuNzYgLTMuMDQgTTU2LjI0IDEzLjYwMDAwMDAwMDAwMDAwMSBjMC4yIDAgMC4zNiAwLjE2IDAuMzYgMC4zNiBsMCAyMSBsOC42NCAwIGMwLjIgMCAwLjM2IDAuMTYgMC4zNiAwLjM2IGwwIDQuMzIgYzAgMC4yIC0wLjE2IDAuMzYgLTAuMzYgMC4zNiBsLTEzLjU2IDAgYy0wLjIgMCAtMC4zMiAtMC4xNiAtMC4zMiAtMC4zNiBsMCAtMjUuNjggYzAgLTAuMiAwLjEyIC0wLjM2IDAuMiwgLTAuMzYgbDQuNTYgMCB6IE01My43NjAwMDAwMDAwMDAwMDUgMTYuMDQgbDAgMjEuNTIgYzAgMC4wOCAwLjA4IDAuMiAwLjI0IDAuMiBsOS4yNCAwIGMwLjMyIDAgMC4zMiAtMC41MiAwIC0wLjUyIGwtOS4wNCAwIGwwIC0yMS4yIGMwIC0wLjI4IC0wLjQ0IC0wLjMyIC0wLjQ0IDAgeiBNNzkuODggMTMuMjM5OTk5OTk5OTk5OTk4IGMzLjQ0IDAgNS44NCAwLjc2IDcuMzYgMi40IGMxLjIgMS4zMiAxLjc2IDMuMiAxLjc2IDUuODggbDAgMTAuNTIgYzAgMi43NiAtMC41NiA0LjY4IC0xLjc2IDUuOTYgYy0xLjU2IDEuNiAtMy45MiAyLjQgLTcuMzYgMi40IGMtMy41NiAwIC01Ljg4IC0wLjggLTcuNCAtMi40IGMtMS4xNiAtMS4yOCAtMS44IC0zLjIgLTEuOCAtNS45NiBsMCAtMTAuNTIgYzAgLTIuNjggMC42NCAtNC41NiAxLjggLTUuOTIgYzEuNTYgLTEuNiAzLjkyIC0yLjM2IDcuNCAtMi4zNiB6IE04My42Nzk5OTk5OTk5OTk5OSAzMC44NCBsMCAtOCBjMCAtMy41MiAtMS44OCAtNC4yNCAtMy42IC00LjI0IGwtMC40OCAwIGMtMi41NiAwIC0zLjU2IDEuNjQgLTMuNTYgNC4yNCBsMCA4IGMwIDMuNTIgMS44OCA0LjI4IDMuNTYgNC4yOCBsMC40OCAwIGMyLjU2IDAgMy41NiAtMS43MiAzLjYgLTQuMjggeiBNNzMuMiAyMS44IGwwIDkuOTIgYzAgMS44OCAwLjQ4IDMuNDQgMS42IDQuNiBjMS4wNCAxLjA0IDIuNjQgMS42IDQuNiAxLjYgbDEuMDQgMCBjMy43NiAwIDYuMiAtMi40IDYuMiAtNi4yIGwwIC05LjkyIGMwIC00LjA4IC0yLjE2IC02LjI4IC02LjIgLTYuMjggbC0xLjA0IDAgYy00LjA4IDAgLTYuMiAyLjIgLTYuMiA2LjI4IHogTTgwLjQ0IDM3LjQgbC0xLjA0IDAgYy0xLjg4IDAgLTMuMjggLTAuNDggLTQuMjggLTEuNDggcy0xLjUyIC0yLjQgLTEuNTIgLTQuMiBsMCAtOS45MiBjMCAtMy44IDIuMDQgLTUuOCA1LjggLTUuOCBsMS4wNCAwIGMzLjggMCA1LjY4IDEuOTYgNS42OCA1LjggbDAgOS45MiBjMCAxLjY4IC0wLjUyIDMuMiAtMS42IDQuMjQgYy0xLjA0IDAuODggLTIuNDQgMS40NCAtNC4wOCAxLjQ0IHogTTExMSAyOS41NjAwMDAwMDAwMDAwMDIgYy0wLjU2IDEuMTYgLTEuMzYgMi4wNCAtMi40OCAyLjU2IGwzLjM2IDcuNCBjMC4xMiAwLjI0IC0wLjA0IDAuNDggLTAuMjggMC40OCBsLTQuOTIgMCBjLTAuMTYgMCAtMC4yNCAtMC4wOCAtMC4yOCAtMC4yIGwtMy4xMiAtNi44IGwtMi4wNCAwIGwwIDYuNjQgYzAgMC4yIC0wLjE2IDAuMzYgLTAuMzYgMC4zNiBsLTQuNiAwIGMtMC4xNiAwIC0wLjI4IC0wLjE2IC0wLjI4IC0wLjM2IGwwIC0yNS42OCBjMCAtMC4yIDAuMTIgLTAuMzYgMC4yOCAtMC4zNiBsOC4zMiAwIGM0LjQ0IDAgNy4xMiAyLjUyIDcuMTIgNy4yIGwwIDUuMDQgYzAgMS40IC0wLjI0IDIuNzIgLTAuNzIgMy43MiB6IE0xMDYuNDc5OTk5OTk5OTk5OTkgMjQuNiBsMCAtMi42IGMwIC0yLjggLTEuMDQgLTMuMDggLTQuMDggLTMuMDggbC0xLjE2IDAgbDAgOC44NCBsMS4xNiAwIGMyLjUyIDAgNCAtMC4wNCA0LjA4IC0zLjE2IHogTTk4LjkxOTk5OTk5OTk5OTk5IDM3LjU2IGwwIC02Ljg0IGw1Ljc2IDAgbDMuMzYgNi45MiBjMC4wOCAwLjIgMC41NiAwLjEyIDAuNDQgLTAuMjQgbC0zLjM2IC02LjggYzMuMTIgLTAuNDQgNC4yIC0yLjA4IDQuMiAtNS4wNCBsMCAtNSBjMCAtNC40IC00IC00Ljc2IC01LjI0IC00Ljc2IGwtNS40IDAgYy0wLjA4IDAgLTAuMjQgMC4xMiAtMC4yNCAwLjI0IGwwIDIxLjUyIGMwIDAuMjggMC40OCAwLjI4IDAuNDggMCB6IE0xMDguODQgMjAuNTYgbDAgNSBjMCA0LjA4IC0yLjYgNC42NCAtNS4xMiA0LjY0IGwtNC44IDAgbDAgLTEzLjg4IGw1LjE2IDAgYzQuMzIgMCA0Ljc2IDIuOTIgNC43NiA0LjI0IHoiPjwvcGF0aD48L2c+CgkJCTwvZz4KCQk8L3N2Zz4KCQ=="

# --- Configurações do GitHub (Banco de Dados) ---
GITHUB_USER = "LarissaSantanajdsp"
GITHUB_REPO = "Mapa_alunos_CALOR"
DATA_FILE_PATH = "dados_alunos.json"
BASE_URL = "https://mapaalunoscalor-fozyfgucjj7skfkjfscwyt.streamlit.app/"

try:
    GITHUB_TOKEN = st.secrets["GITHUB_TOKEN"]
except:
    GITHUB_TOKEN = None

def carregar_dados_github():
    if not GITHUB_TOKEN: return {}
    url = f"https://api.github.com/repos/{GITHUB_USER}/{GITHUB_REPO}/contents/{DATA_FILE_PATH}"
    headers = {"Authorization": f"token {GITHUB_TOKEN}"}
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            content = response.json()
            decoded_data = base64.b64decode(content['content']).decode('utf-8')
            return json.loads(decoded_data)
    except: pass
    return {}

def salvar_dados_github(dados):
    if not GITHUB_TOKEN: return False
    url = f"https://api.github.com/repos/{GITHUB_USER}/{GITHUB_REPO}/contents/{DATA_FILE_PATH}"
    headers = {"Authorization": f"token {GITHUB_TOKEN}"}
    sha = None
    get_response = requests.get(url, headers=headers)
    if get_response.status_code == 200: sha = get_response.json()['sha']
    content_json = json.dumps(dados, ensure_ascii=False, indent=2)
    encoded_content = base64.b64encode(content_json.encode('utf-8')).decode('utf-8')
    payload = {"message": "Atualização automática", "content": encoded_content}
    if sha: payload["sha"] = sha
    requests.put(url, headers=headers, json=payload)
    return True

if 'alunos_pilares' not in st.session_state:
    st.session_state.alunos_pilares = carregar_dados_github()

query_params = st.query_params
aluno_selecionado_url = query_params.get("aluno", None)

st.markdown(f"""
    <style>
        body {{ background-color: {BG_COLOR}; }}
        .main {{ background-color: {BG_COLOR}; }}
        h1 {{ color: {TEXT_COLOR}; text-align: center; font-family: 'Arial Black'; }}
        .stButton>button {{ background-color: {ACCENT_COLOR}; color: white; border-radius: 5px; }}
    </style>
""", unsafe_allow_html=True)

def criar_grafico_radar(aluno_nome, pontos):
    fig = go.Figure()
    pilares = ['Clareza', 'Impacto', 'Visão', 'Conexão']
    for i, p in enumerate(pontos):
        color = CORES_CALOR_REFINADA[i % len(CORES_CALOR_REFINADA)]
        fig.add_trace(go.Scatterpolar(
            r=[p[1], p[2], p[3], p[4], p[1]],
            theta=pilares + [pilares[0]],
            fill='toself',
            name=p[0],
            line=dict(color=color, width=4),
            marker=dict(size=10),
            fillcolor=f"rgba{tuple(list(int(color.lstrip('#')[i:i+2], 16) for i in (0, 2, 4)) + [0.1])}"
        ))
    
    # Adicionar Logo da CALOR
    fig.add_layout_image(
        dict(
            source=f"data:image/svg+xml;base64,{LOGO_BASE64}",
            xref="paper", yref="paper",
            x=1.1, y=-0.1,
            sizex=0.2, sizey=0.2,
            xanchor="right", yanchor="bottom"
        )
    )

    fig.update_layout(
        title=dict(text=f"Mapa de Evolução: {aluno_nome}", x=0.5, y=0.95, font=dict(size=24, color=TEXT_COLOR, family="Arial Black")),
        height=800,
        polar=dict(
            bgcolor=BG_COLOR,
            radialaxis=dict(visible=True, range=[0, 5.5], tickvals=[1, 2, 3, 4, 5], tickfont=dict(size=14, color=TEXT_COLOR, family="Arial Black")),
            angularaxis=dict(tickfont=dict(size=22, color=TEXT_COLOR, family="Arial Black"), rotation=90, direction="clockwise")
        ),
        showlegend=True,
        legend=dict(title=dict(text="Avaliações Inseridas", font=dict(size=16, family="Arial Black")), orientation="v", yanchor="middle", y=0.5, xanchor="left", x=1.1, font=dict(size=16, color=TEXT_COLOR)),
        paper_bgcolor=BG_COLOR,
        plot_bgcolor=BG_COLOR,
        margin=dict(l=80, r=150, t=100, b=100),
        dragmode='zoom'
    )
    return fig

if aluno_selecionado_url:
    aluno_nome = aluno_selecionado_url
    if aluno_nome in st.session_state.alunos_pilares:
        st.title(f"🎯 Sua Evolução por Pilares")
        pontos = st.session_state.alunos_pilares[aluno_nome]
        if pontos:
            fig = criar_grafico_radar(aluno_nome, pontos)
            st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': True, 'scrollZoom': True})
    else: st.error(f"Aluno '{aluno_nome}' não encontrado.")
    if st.button("⬅️ Voltar para Gestão"):
        st.query_params.clear()
        st.rerun()
    st.stop()

st.title("🎯 Gestão de Pilares - Movimento Calor")
st.markdown("---")

with st.sidebar:
    st.header("⚙️ Configurações")
    if GITHUB_TOKEN: st.success("✅ Token do GitHub detectado.")
    else: st.error("❌ Token do GitHub NÃO detectado.")
    if st.button("🔄 Sincronizar Dados"):
        st.session_state.alunos_pilares = carregar_dados_github()
        st.rerun()

col1, col2 = st.columns([2, 1])
with col1: novo_aluno = st.text_input("Nome do Aluno:", placeholder="Ex: Leandro Souza")
with col2:
    if st.button("➕ Adicionar Aluno"):
        if novo_aluno and novo_aluno not in st.session_state.alunos_pilares:
            st.session_state.alunos_pilares[novo_aluno] = []
            salvar_dados_github(st.session_state.alunos_pilares)
            st.rerun()

st.markdown("---")

if st.session_state.alunos_pilares:
    for aluno in st.session_state.alunos_pilares:
        with st.expander(f"👤 {aluno}", expanded=False):
            link_aluno = f"{BASE_URL}?aluno={urllib.parse.quote(aluno)}"
            st.markdown(f"**🔗 Link Único do Aluno:**")
            st.code(link_aluno, language="text")
            st.divider()
            pontos = st.session_state.alunos_pilares[aluno]
            for i, p in enumerate(pontos):
                c1, c2, c3, c4, c5, c6 = st.columns([2, 1, 1, 1, 1, 0.5])
                with c1: n_nome = st.text_input(f"Nome", value=p[0], key=f"n_{aluno}_{i}", label_visibility="collapsed")
                with c2: n_c = st.number_input(f"C", 0.0, 5.0, float(p[1]), 0.5, key=f"c_{aluno}_{i}", label_visibility="collapsed")
                with c3: n_im = st.number_input(f"I", 0.0, 5.0, float(p[2]), 0.5, key=f"i_{aluno}_{i}", label_visibility="collapsed")
                with c4: n_v = st.number_input(f"V", 0.0, 5.0, float(p[3]), 0.5, key=f"v_{aluno}_{i}", label_visibility="collapsed")
                with c5: n_co = st.number_input(f"Co", 0.0, 5.0, float(p[4]), 0.5, key=f"co_{aluno}_{i}", label_visibility="collapsed")
                with c6: 
                    if st.button("🗑️", key=f"del_{aluno}_{i}"):
                        st.session_state.alunos_pilares[aluno].pop(i)
                        salvar_dados_github(st.session_state.alunos_pilares)
                        st.rerun()
                if n_nome != p[0] or n_c != p[1] or n_im != p[2] or n_v != p[3] or n_co != p[4]:
                    st.session_state.alunos_pilares[aluno][i] = (n_nome, n_c, n_im, n_v, n_co)
                    salvar_dados_github(st.session_state.alunos_pilares)
            
            st.write("**Adicionar Avaliação**")
            a1, a2, a3, a4, a5, a6 = st.columns([2, 1, 1, 1, 1, 0.5])
            with a1: a_nome = st.text_input("Texto", placeholder="Ex: Pitch", key=f"an_{aluno}")
            with a2: a_c = st.number_input("C", 0.0, 5.0, 2.5, 0.5, key=f"ac_{aluno}")
            with a3: a_im = st.number_input("I", 0.0, 5.0, 2.5, 0.5, key=f"ai_{aluno}")
            with a4: a_v = st.number_input("V", 0.0, 5.0, 2.5, 0.5, key=f"av_{aluno}")
            with a5: a_co = st.number_input("Co", 0.0, 5.0, 2.5, 0.5, key=f"aco_{aluno}")
            with a6:
                if st.button("✅", key=f"ab_{aluno}"):
                    st.session_state.alunos_pilares[aluno].append((a_nome if a_nome else "Novo", a_c, a_im, a_v, a_co))
                    salvar_dados_github(st.session_state.alunos_pilares)
                    st.rerun()
            if pontos:
                fig = criar_grafico_radar(aluno, pontos)
                st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': True})

st.markdown("---")
st.markdown("<div style='text-align: center; color: #4E2C1C; font-size: 12px;'>🎓 Movimento Calor | Gestão de Pilares Permanente</div>", unsafe_allow_html=True)
