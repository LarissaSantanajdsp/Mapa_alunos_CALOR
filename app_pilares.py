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

# --- Configurações do GitHub (Banco de Dados) ---
GITHUB_USER = "LarissaSantanajdsp"
GITHUB_REPO = "Mapa_alunos_CALOR"
DATA_FILE_PATH = "dados_alunos.json"

# Tenta pegar o token dos Secrets do Streamlit
try:
    GITHUB_TOKEN = st.secrets["GITHUB_TOKEN"]
except:
    GITHUB_TOKEN = None

def carregar_dados_github():
    if not GITHUB_TOKEN:
        return {}
    
    url = f"https://api.github.com/repos/{GITHUB_USER}/{GITHUB_REPO}/contents/{DATA_FILE_PATH}"
    headers = {"Authorization": f"token {GITHUB_TOKEN}"}
    
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            content = response.json()
            decoded_data = base64.b64decode(content['content']).decode('utf-8')
            return json.loads(decoded_data)
        elif response.status_code == 404:
            return {} # Arquivo ainda não existe
    except Exception as e:
        st.sidebar.error(f"Erro ao carregar: {str(e)}")
    return {}

def salvar_dados_github(dados):
    if not GITHUB_TOKEN:
        return False
    
    url = f"https://api.github.com/repos/{GITHUB_USER}/{GITHUB_REPO}/contents/{DATA_FILE_PATH}"
    headers = {"Authorization": f"token {GITHUB_TOKEN}"}
    
    # Pega o SHA do arquivo atual para poder atualizar
    sha = None
    get_response = requests.get(url, headers=headers)
    if get_response.status_code == 200:
        sha = get_response.json()['sha']
    
    content_json = json.dumps(dados, ensure_ascii=False, indent=2)
    encoded_content = base64.b64encode(content_json.encode('utf-8')).decode('utf-8')
    
    payload = {
        "message": "Atualização automática de dados dos alunos",
        "content": encoded_content
    }
    if sha:
        payload["sha"] = sha
        
    put_response = requests.put(url, headers=headers, json=payload)
    
    if put_response.status_code in [200, 201]:
        return True
    else:
        st.sidebar.error(f"Erro ao salvar: {put_response.status_code}")
        return False

# Inicializar dados
if 'alunos_pilares' not in st.session_state:
    st.session_state.alunos_pilares = carregar_dados_github()

# --- Lógica de Parâmetros de URL ---
query_params = st.query_params
aluno_selecionado_url = query_params.get("aluno", None)

# Estilos CSS
st.markdown(f"""
    <style>
        body {{ background-color: {BG_COLOR}; }}
        .main {{ background-color: {BG_COLOR}; }}
        h1 {{ color: {TEXT_COLOR}; text-align: center; font-family: 'Arial Black'; }}
        h2 {{ color: {TEXT_COLOR}; }}
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
    
    fig.update_layout(
        title=dict(
            text=f"Mapa de Evolução: {aluno_nome}",
            x=0.5,
            y=0.95,
            font=dict(size=24, color=TEXT_COLOR, family="Arial Black")
        ),
        height=800,
        polar=dict(
            bgcolor=BG_COLOR,
            radialaxis=dict(
                visible=True, 
                range=[0, 5.5], 
                tickvals=[1, 2, 3, 4, 5], 
                tickfont=dict(size=14, color=TEXT_COLOR, family="Arial Black"),
                gridcolor="rgba(78, 44, 28, 0.2)"
            ),
            angularaxis=dict(
                tickfont=dict(size=22, color=TEXT_COLOR, family="Arial Black"), 
                rotation=90, 
                direction="clockwise",
                gridcolor="rgba(78, 44, 28, 0.2)"
            )
        ),
        showlegend=True,
        legend=dict(
            title=dict(text="Avaliações Inseridas", font=dict(size=16, family="Arial Black")),
            orientation="v",
            yanchor="middle",
            y=0.5,
            xanchor="left",
            x=1.1,
            font=dict(size=16, color=TEXT_COLOR)
        ),
        paper_bgcolor=BG_COLOR,
        plot_bgcolor=BG_COLOR,
        margin=dict(l=80, r=150, t=100, b=50),
        dragmode='zoom'
    )
    return fig

# --- MODO VISUALIZAÇÃO DO ALUNO ---
if aluno_selecionado_url:
    aluno_nome = aluno_selecionado_url
    if aluno_nome in st.session_state.alunos_pilares:
        st.title(f"🎯 Sua Evolução por Pilares")
        pontos = st.session_state.alunos_pilares[aluno_nome]
        if pontos:
            fig = criar_grafico_radar(aluno_nome, pontos)
            st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': True, 'scrollZoom': True})
    else:
        st.error(f"Aluno '{aluno_nome}' não encontrado.")
    
    if st.button("⬅️ Voltar para Gestão"):
        st.query_params.clear()
        st.rerun()
    st.stop()

# --- MODO GESTÃO (MENTOR) ---
st.title("🎯 Gestão de Pilares - Movimento Calor")
st.markdown("---")

# Sidebar com Diagnóstico
with st.sidebar:
    st.header("⚙️ Configurações")
    if GITHUB_TOKEN:
        st.success("✅ Token do GitHub detectado.")
    else:
        st.error("❌ Token do GitHub NÃO detectado nos Secrets.")
        st.info("Adicione GITHUB_TOKEN nos Secrets do Streamlit Cloud.")
    
    if st.button("🔄 Sincronizar Dados"):
        st.session_state.alunos_pilares = carregar_dados_github()
        st.rerun()

# Entrada de Alunos
col1, col2 = st.columns([2, 1])
with col1:
    novo_aluno = st.text_input("Nome do Aluno:", placeholder="Ex: Leandro Souza")
with col2:
    if st.button("➕ Adicionar Aluno"):
        if novo_aluno and novo_aluno not in st.session_state.alunos_pilares:
            st.session_state.alunos_pilares[novo_aluno] = []
            if salvar_dados_github(st.session_state.alunos_pilares):
                st.success(f"Aluno {novo_aluno} salvo com sucesso!")
                st.rerun()
            else:
                st.error("Falha ao salvar no GitHub. Verifique o Token.")

st.markdown("---")

# Listagem e Edição
if st.session_state.alunos_pilares:
    for aluno in st.session_state.alunos_pilares:
        with st.expander(f"👤 {aluno}", expanded=False):
            base_url = "https://mapa-alunos-calor.streamlit.app/"
            link_aluno = f"{base_url}?aluno={urllib.parse.quote(aluno)}"
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
