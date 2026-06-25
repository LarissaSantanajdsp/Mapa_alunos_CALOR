import streamlit as st
from streamlit_gsheets import GSheetsConnection
import plotly.graph_objects as go
import pandas as pd
import json
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

# --- Conexão com Google Sheets ---
try:
    conn = st.connection("gsheets", type=GSheetsConnection)
    df_existente = conn.read(ttl=0)
except Exception as e:
    df_existente = pd.DataFrame(columns=['Aluno', 'Texto', 'Clareza', 'Impacto', 'Visão', 'Conexão'])

def salvar_na_planilha(df):
    conn.update(data=df)
    st.cache_data.clear()

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
    dados_aluno = df_existente[df_existente['Aluno'] == aluno_nome]
    
    if not dados_aluno.empty:
        st.title(f"🎯 Sua Evolução por Pilares")
        st.markdown(f"<h3 style='text-align: center; color: {SECONDARY_COLOR};'>{aluno_nome}</h3>", unsafe_allow_html=True)
        
        fig = go.Figure()
        pilares = ['Clareza', 'Impacto', 'Visão', 'Conexão']
        
        for i, row in enumerate(dados_aluno.itertuples()):
            color = CORES_CALOR_REFINADA[i % len(CORES_CALOR_REFINADA)]
            fig.add_trace(go.Scatterpolar(
                r=[row.Clareza, row.Impacto, row.Visão, row.Conexão, row.Clareza],
                theta=pilares + [pilares[0]],
                fill='toself',
                name=row.Texto,
                line=dict(color=color, width=4),
                marker=dict(size=10),
                fillcolor=f"rgba{tuple(list(int(color.lstrip('#')[i:i+2], 16) for i in (0, 2, 4)) + [0.1])}"
            ))
        
        fig.update_layout(
            height=750,
            polar=dict(
                bgcolor=BG_COLOR,
                radialaxis=dict(visible=True, range=[0, 5.5], tickvals=[1, 2, 3, 4, 5], tickfont=dict(size=14, family="Arial Black")),
                angularaxis=dict(tickfont=dict(size=20, family="Arial Black"), rotation=90, direction="clockwise")
            ),
            legend=dict(orientation="v", yanchor="middle", y=0.5, xanchor="left", x=1.05, font=dict(size=16)),
            paper_bgcolor=BG_COLOR,
            plot_bgcolor=BG_COLOR,
            margin=dict(l=80, r=150, t=50, b=50)
        )
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.error(f"Aluno '{aluno_nome}' não encontrado.")
    
    if st.button("⬅️ Voltar para Gestão"):
        st.query_params.clear()
        st.rerun()
    st.stop()

# --- MODO GESTÃO (MENTOR) ---
st.title("🎯 Gestão de Pilares - Movimento Calor")
st.markdown("---")

# Entrada de Alunos
col1, col2 = st.columns([2, 1])
with col1:
    novo_aluno = st.text_input("Nome do Aluno:", placeholder="Ex: Leandro Souza")
with col2:
    if st.button("➕ Adicionar Aluno"):
        if novo_aluno and novo_aluno not in df_existente['Aluno'].unique():
            nova_linha = pd.DataFrame([{'Aluno': novo_aluno, 'Texto': 'Inicial', 'Clareza': 0, 'Impacto': 0, 'Visão': 0, 'Conexão': 0}])
            df_atualizado = pd.concat([df_existente, nova_linha], ignore_index=True)
            salvar_na_planilha(df_atualizado)
            st.rerun()

st.markdown("---")

# Listagem e Edição
alunos_unicos = df_existente['Aluno'].unique()
if len(alunos_unicos) > 0:
    for aluno in alunos_unicos:
        with st.expander(f"👤 {aluno}", expanded=False):
            base_url = "https://mapa-alunos-calor.streamlit.app/"
            link_aluno = f"{base_url}?aluno={urllib.parse.quote(aluno)}"
            st.markdown(f"**🔗 Link Único do Aluno:**")
            st.code(link_aluno, language="text")
            st.divider()
            
            dados_aluno = df_existente[df_existente['Aluno'] == aluno]
            
            for idx, row in dados_aluno.iterrows():
                c1, c2, c3, c4, c5, c6 = st.columns([2, 1, 1, 1, 1, 0.5])
                with c1: n_nome = st.text_input(f"Nome", value=row['Texto'], key=f"n_{idx}", label_visibility="collapsed")
                with c2: n_c = st.number_input(f"C", 0.0, 5.0, float(row['Clareza']), 0.5, key=f"c_{idx}", label_visibility="collapsed")
                with c3: n_im = st.number_input(f"I", 0.0, 5.0, float(row['Impacto']), 0.5, key=f"i_{idx}", label_visibility="collapsed")
                with c4: n_v = st.number_input(f"V", 0.0, 5.0, float(row['Visão']), 0.5, key=f"v_{idx}", label_visibility="collapsed")
                with c5: n_co = st.number_input(f"Co", 0.0, 5.0, float(row['Conexão']), 0.5, key=f"co_{idx}", label_visibility="collapsed")
                with c6: 
                    if st.button("🗑️", key=f"del_{idx}"):
                        df_existente = df_existente.drop(idx)
                        salvar_na_planilha(df_existente)
                        st.rerun()
                
                if n_nome != row['Texto'] or n_c != row['Clareza'] or n_im != row['Impacto'] or n_v != row['Visão'] or n_co != row['Conexão']:
                    df_existente.at[idx, 'Texto'] = n_nome
                    df_existente.at[idx, 'Clareza'] = n_c
                    df_existente.at[idx, 'Impacto'] = n_im
                    df_existente.at[idx, 'Visão'] = n_v
                    df_existente.at[idx, 'Conexão'] = n_co
                    salvar_na_planilha(df_existente)
            
            st.write("**Adicionar Avaliação**")
            a1, a2, a3, a4, a5, a6 = st.columns([2, 1, 1, 1, 1, 0.5])
            with a1: a_nome = st.text_input("Texto", placeholder="Ex: Pitch", key=f"an_{aluno}")
            with a2: a_c = st.number_input("C", 0.0, 5.0, 2.5, 0.5, key=f"ac_{aluno}")
            with a3: a_im = st.number_input("I", 0.0, 5.0, 2.5, 0.5, key=f"ai_{aluno}")
            with a4: a_v = st.number_input("V", 0.0, 5.0, 2.5, 0.5, key=f"av_{aluno}")
            with a5: a_co = st.number_input("Co", 0.0, 5.0, 2.5, 0.5, key=f"aco_{aluno}")
            with a6:
                if st.button("✅", key=f"ab_{aluno}"):
                    nova_av = pd.DataFrame([{'Aluno': aluno, 'Texto': a_nome if a_nome else "Novo", 'Clareza': a_c, 'Impacto': a_im, 'Visão': a_v, 'Conexão': a_co}])
                    df_atualizado = pd.concat([df_existente, nova_av], ignore_index=True)
                    salvar_na_planilha(df_atualizado)
                    st.rerun()

st.markdown("---")
st.markdown("<div style='text-align: center; color: #4E2C1C; font-size: 12px;'>🎓 Movimento Calor | Gestão de Pilares Permanente</div>", unsafe_allow_html=True)
