import streamlit as st
import plotly.graph_objects as go
import pandas as pd
from io import BytesIO
import json
import os
from datetime import datetime
import urllib.parse

# Configuração da página
st.set_page_config(page_title="Avaliação por Pilares", layout="wide", initial_sidebar_state="expanded")

# Estilos do Movimento Calor
BG_COLOR = '#F2F0E4'
TEXT_COLOR = '#4E2C1C'
ACCENT_COLOR = '#E65100'
SECONDARY_COLOR = '#8B4513'

# Paleta Refinada Movimento Calor (Contraste Máximo)
CORES_CALOR_REFINADA = [
    '#E65100', # Laranja Vibrante
    '#2E7D32', # Verde Floresta
    '#4E2C1C', # Marrom Café Profundo
    '#1565C0', # Azul Oceano
    '#D4A574', # Bege Dourado
    '#C62828', # Vermelho Intenso
    '#FF8F00', # Âmbar/Amarelo Queimado
    '#6A1B9A', # Roxo Berinjela
    '#AD1457', # Rosa Velho/Bordô
    '#37474F'  # Cinza Azulado Escuro
]

# Arquivo de armazenamento de dados
DATA_FILE = "/tmp/pilares_data.json"

# Funções de persistência
def carregar_dados():
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        except:
            return {}
    return {}

def salvar_dados(dados):
    try:
        with open(DATA_FILE, 'w', encoding='utf-8') as f:
            json.dump(dados, f, ensure_ascii=False, indent=2)
    except Exception as e:
        st.error(f"Erro ao salvar dados: {e}")

# Inicializar session state
if 'alunos_pilares' not in st.session_state:
    st.session_state.alunos_pilares = carregar_dados()

# --- Lógica de Parâmetros de URL ---
query_params = st.query_params
aluno_selecionado_url = query_params.get("aluno", None)

# Estilos CSS
st.markdown(f"""
    <style>
        body {{ background-color: {BG_COLOR}; }}
        .main {{ background-color: {BG_COLOR}; }}
        h1 {{ color: {TEXT_COLOR}; text-align: center; }}
        h2 {{ color: {TEXT_COLOR}; }}
        .stButton>button {{ background-color: {ACCENT_COLOR}; color: white; border-radius: 5px; }}
    </style>
""", unsafe_allow_html=True)

# --- MODO VISUALIZAÇÃO DO ALUNO ---
if aluno_selecionado_url:
    aluno_nome = aluno_selecionado_url
    if aluno_nome in st.session_state.alunos_pilares:
        st.title(f"🎯 Sua Evolução por Pilares")
        st.markdown(f"<h3 style='text-align: center; color: {SECONDARY_COLOR};'>{aluno_nome}</h3>", unsafe_allow_html=True)
        
        pontos = st.session_state.alunos_pilares[aluno_nome]
        if pontos:
            fig = go.Figure()
            pilares = ['Clareza', 'Impacto', 'Visão', 'Conexão']
            
            for i, (nome_texto, clareza, impacto, visao, conexao) in enumerate(pontos):
                color = CORES_CALOR_REFINADA[i % len(CORES_CALOR_REFINADA)]
                fig.add_trace(go.Scatterpolar(
                    r=[clareza, impacto, visao, conexao, clareza],
                    theta=pilares + [pilares[0]],
                    fill='toself',
                    name=nome_texto,
                    line=dict(color=color, width=4),
                    marker=dict(size=10),
                    fillcolor=f"rgba{tuple(list(int(color.lstrip('#')[i:i+2], 16) for i in (0, 2, 4)) + [0.1])}"
                ))
            
            fig.update_layout(
                height=700,
                polar=dict(
                    bgcolor=BG_COLOR,
                    radialaxis=dict(
                        visible=True, 
                        range=[0, 5.5], 
                        tickvals=[1, 2, 3, 4, 5], 
                        tickfont=dict(size=14, color=TEXT_COLOR, family="Arial Black"),
                        angle=45, # Move a escala para a lateral (45 graus)
                        tickangle=0
                    ),
                    angularaxis=dict(tickfont=dict(size=20, family="Arial Black"), rotation=90, direction="clockwise")
                ),
                legend=dict(orientation="h", yanchor="bottom", y=-0.2, xanchor="center", x=0.5, font=dict(size=16)),
                paper_bgcolor=BG_COLOR,
                plot_bgcolor=BG_COLOR,
                margin=dict(l=50, r=50, t=50, b=100)
            )
            st.plotly_chart(fig, use_container_width=True)
            st.info("💡 Este é o seu gráfico interativo. Você pode clicar na legenda para filtrar os textos ou passar o mouse para ver as notas.")
        else:
            st.warning("Ainda não há avaliações registradas para você.")
    else:
        st.error(f"Aluno '{aluno_nome}' não encontrado.")
    
    if st.button("⬅️ Voltar para Gestão (Apenas Mentor)"):
        st.query_params.clear()
        st.rerun()
    st.stop()

# --- MODO GESTÃO (MENTOR) ---
st.title("🎯 Gestão de Pilares - Movimento Calor")
st.markdown("---")

# Sidebar
with st.sidebar:
    st.header("📋 Painel do Mentor")
    if st.button("🗑️ Limpar Todos os Dados"):
        if st.checkbox("Confirmar exclusão de tudo?"):
            st.session_state.alunos_pilares = {}
            salvar_dados({})
            st.rerun()

# Entrada de Alunos
col1, col2 = st.columns([2, 1])
with col1:
    novo_aluno = st.text_input("Nome do Aluno:", placeholder="Ex: Leandro Souza")
with col2:
    if st.button("➕ Adicionar Aluno"):
        if novo_aluno and novo_aluno not in st.session_state.alunos_pilares:
            st.session_state.alunos_pilares[novo_aluno] = []
            salvar_dados(st.session_state.alunos_pilares)
            st.rerun()

st.markdown("---")

# Listagem e Edição
if st.session_state.alunos_pilares:
    for aluno in st.session_state.alunos_pilares:
        with st.expander(f"👤 {aluno}", expanded=False):
            # Gerador de Link Único
            base_url = "https://mapa-alunos-calor.streamlit.app/"
            link_aluno = f"{base_url}?aluno={urllib.parse.quote(aluno)}"
            st.markdown(f"**🔗 Link Único do Aluno:**")
            st.code(link_aluno, language="text")
            st.divider()
            
            # Edição de Notas
            pontos = st.session_state.alunos_pilares[aluno]
            if pontos:
                for i, (nome, c, im, v, co) in enumerate(pontos):
                    c1, c2, c3, c4, c5, c6 = st.columns([2, 1, 1, 1, 1, 0.5])
                    with c1: n_nome = st.text_input(f"Nome", value=nome, key=f"n_{aluno}_{i}", label_visibility="collapsed")
                    with c2: n_c = st.number_input(f"C", 0.0, 5.0, float(c), 0.5, key=f"c_{aluno}_{i}", label_visibility="collapsed")
                    with c3: n_im = st.number_input(f"I", 0.0, 5.0, float(im), 0.5, key=f"i_{aluno}_{i}", label_visibility="collapsed")
                    with c4: n_v = st.number_input(f"V", 0.0, 5.0, float(v), 0.5, key=f"v_{aluno}_{i}", label_visibility="collapsed")
                    with c5: n_co = st.number_input(f"Co", 0.0, 5.0, float(co), 0.5, key=f"co_{aluno}_{i}", label_visibility="collapsed")
                    with c6: 
                        if st.button("🗑️", key=f"del_{aluno}_{i}"):
                            st.session_state.alunos_pilares[aluno].pop(i)
                            salvar_dados(st.session_state.alunos_pilares)
                            st.rerun()
                    
                    if n_nome != nome or n_c != c or n_im != im or n_v != v or n_co != co:
                        st.session_state.alunos_pilares[aluno][i] = (n_nome, n_c, n_im, n_v, n_co)
                        salvar_dados(st.session_state.alunos_pilares)
            
            # Adicionar Novo
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
                    salvar_dados(st.session_state.alunos_pilares)
                    st.rerun()
            
            # Visualização Prévia do Gráfico (Plotly)
            if pontos:
                fig = go.Figure()
                pilares = ['Clareza', 'Impacto', 'Visão', 'Conexão']
                for i, (nome, c, im, v, co) in enumerate(pontos):
                    color = CORES_CALOR_REFINADA[i % len(CORES_CALOR_REFINADA)]
                    fig.add_trace(go.Scatterpolar(r=[c, im, v, co, c], theta=pilares + [pilares[0]], fill='toself', name=nome, line=dict(color=color, width=3)))
                fig.update_layout(
                    height=450, 
                    polar=dict(
                        bgcolor=BG_COLOR, 
                        radialaxis=dict(range=[0, 5.5], tickvals=[1, 2, 3, 4, 5], angle=45)
                    ), 
                    showlegend=True, 
                    paper_bgcolor=BG_COLOR
                )
                st.plotly_chart(fig, use_container_width=True)

st.markdown("---")
st.markdown("<div style='text-align: center; color: #4E2C1C; font-size: 12px;'>🎓 Movimento Calor | Gestão de Pilares</div>", unsafe_allow_html=True)
