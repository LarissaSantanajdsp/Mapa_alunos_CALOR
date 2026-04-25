import streamlit as st
import plotly.graph_objects as go
import pandas as pd
from io import BytesIO
import json
import os
from datetime import datetime

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
    """Carrega os dados do arquivo JSON se existir."""
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        except:
            return {}
    return {}

def salvar_dados(dados):
    """Salva os dados no arquivo JSON."""
    try:
        with open(DATA_FILE, 'w', encoding='utf-8') as f:
            json.dump(dados, f, ensure_ascii=False, indent=2)
    except Exception as e:
        st.error(f"Erro ao salvar dados: {e}")

def exportar_dados_json(dados):
    """Converte os dados para JSON para download."""
    return json.dumps(dados, ensure_ascii=False, indent=2)

# Título da aplicação
st.markdown("""
    <style>
        body { background-color: #F2F0E4; }
        .main { background-color: #F2F0E4; }
        h1 { color: #4E2C1C; text-align: center; }
        h2 { color: #4E2C1C; }
    </style>
""", unsafe_allow_html=True)

st.title("🎯 Avaliação por Pilares - Clareza, Impacto, Visão, Conexão")
st.markdown("---")

# Sidebar para instruções e gerenciamento de dados
with st.sidebar:
    st.header("📋 Como Usar")
    st.markdown("""
    1. **Adicione um Aluno:** Digite o nome do aluno.
    2. **Insira um Texto:** Dê um nome ao texto/apresentação.
    3. **Avalie os Pilares:** Atribua notas (0-5) para cada pilar.
    4. **Interatividade:** 
       - Passe o mouse sobre os pontos para ver as notas.
       - Clique na legenda para ocultar/mostrar avaliações.
       - Clique duas vezes na legenda para isolar uma avaliação.
    
    ---
    
    **💾 Gerenciamento de Dados:**
    """)
    
    # Opções de gerenciamento de dados
    if st.button("📥 Baixar Backup (JSON)"):
        dados = st.session_state.get('alunos_pilares', {})
        json_str = exportar_dados_json(dados)
        st.download_button(
            label="📥 Clique aqui para baixar",
            data=json_str,
            file_name=f"backup_pilares_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
            mime="application/json"
        )
    
    if st.button("🗑️ Limpar Todos os Dados"):
        st.session_state.alunos_pilares = {}
        salvar_dados({})
        st.success("✅ Todos os dados foram removidos!")
        st.rerun()

# Inicializar session state com dados persistentes
if 'alunos_pilares' not in st.session_state:
    st.session_state.alunos_pilares = carregar_dados()

# Seção de entrada de dados
col1, col2 = st.columns([2, 1])

with col1:
    novo_aluno = st.text_input("Nome do Aluno:", placeholder="Ex: Leandro Souza")

with col2:
    if st.button("➕ Adicionar Aluno"):
        if novo_aluno and novo_aluno not in st.session_state.alunos_pilares:
            st.session_state.alunos_pilares[novo_aluno] = []
            salvar_dados(st.session_state.alunos_pilares)
            st.success(f"Aluno '{novo_aluno}' adicionado!")
            st.rerun()
        elif novo_aluno in st.session_state.alunos_pilares:
            st.warning(f"Aluno '{novo_aluno}' já existe!")

st.markdown("---")

# Exibir alunos e permitir entrada de dados
if st.session_state.alunos_pilares:
    st.subheader("📝 Avaliação de Textos por Pilares")
    
    for aluno in st.session_state.alunos_pilares:
        with st.expander(f"👤 {aluno}", expanded=False):
            # Mostrar e permitir edição de textos já avaliados
            if st.session_state.alunos_pilares[aluno]:
                st.write("**Textos Avaliados (Clique para Editar):**")
                
                # Criar colunas para edição
                cols = st.columns([2, 1, 1, 1, 1, 1])
                with cols[0]: st.write("**Nome do Texto**")
                with cols[1]: st.write("**Clareza**")
                with cols[2]: st.write("**Impacto**")
                with cols[3]: st.write("**Visão**")
                with cols[4]: st.write("**Conexão**")
                with cols[5]: st.write("**Ação**")
                
                # Exibir e permitir edição de cada avaliação
                for i, (nome_texto, clareza, impacto, visao, conexao) in enumerate(st.session_state.alunos_pilares[aluno]):
                    cols = st.columns([2, 1, 1, 1, 1, 1])
                    with cols[0]:
                        novo_nome = st.text_input(f"Nome T{i+1}", value=nome_texto, key=f"nome_edit_{aluno}_{i}", label_visibility="collapsed")
                    with cols[1]:
                        nova_clareza = st.number_input(f"Clareza T{i+1}", min_value=0.0, max_value=5.0, value=float(clareza), step=0.5, key=f"clareza_edit_{aluno}_{i}", label_visibility="collapsed")
                    with cols[2]:
                        novo_impacto = st.number_input(f"Impacto T{i+1}", min_value=0.0, max_value=5.0, value=float(impacto), step=0.5, key=f"impacto_edit_{aluno}_{i}", label_visibility="collapsed")
                    with cols[3]:
                        nova_visao = st.number_input(f"Visão T{i+1}", min_value=0.0, max_value=5.0, value=float(visao), step=0.5, key=f"visao_edit_{aluno}_{i}", label_visibility="collapsed")
                    with cols[4]:
                        nova_conexao = st.number_input(f"Conexão T{i+1}", min_value=0.0, max_value=5.0, value=float(conexao), step=0.5, key=f"conexao_edit_{aluno}_{i}", label_visibility="collapsed")
                    with cols[5]:
                        if st.button(f"🗑️", key=f"remove_{aluno}_{i}"):
                            st.session_state.alunos_pilares[aluno].pop(i)
                            salvar_dados(st.session_state.alunos_pilares)
                            st.rerun()
                    
                    if novo_nome != nome_texto or nova_clareza != clareza or novo_impacto != impacto or nova_visao != visao or nova_conexao != conexao:
                        st.session_state.alunos_pilares[aluno][i] = (novo_nome, nova_clareza, novo_impacto, nova_visao, nova_conexao)
                        salvar_dados(st.session_state.alunos_pilares)
                st.divider()
            
            # Adicionar novo texto
            st.write(f"**Adicionar Novo Texto para {aluno}**")
            col1, col2, col3, col4, col5, col6 = st.columns([2, 1, 1, 1, 1, 1])
            with col1:
                nome_novo_texto = st.text_input("Nome do Texto", placeholder="Ex: Discurso Empresa", key=f"nome_new_{aluno}")
            with col2: clareza = st.slider(f"Clareza", 0.0, 5.0, 2.5, 0.5, key=f"clareza_new_{aluno}")
            with col3: impacto = st.slider(f"Impacto", 0.0, 5.0, 2.5, 0.5, key=f"impacto_new_{aluno}")
            with col4: visao = st.slider(f"Visão", 0.0, 5.0, 2.5, 0.5, key=f"visao_new_{aluno}")
            with col5: conexao = st.slider(f"Conexão", 0.0, 5.0, 2.5, 0.5, key=f"conexao_new_{aluno}")
            with col6:
                if st.button(f"✅", key=f"add_{aluno}"):
                    nome_final = nome_novo_texto if nome_novo_texto else f"Texto {len(st.session_state.alunos_pilares[aluno]) + 1}"
                    st.session_state.alunos_pilares[aluno].append((nome_final, clareza, impacto, visao, conexao))
                    salvar_dados(st.session_state.alunos_pilares)
                    st.rerun()
            
            if st.button(f"🗑️ Remover Todos", key=f"del_all_{aluno}"):
                st.session_state.alunos_pilares[aluno] = []
                salvar_dados(st.session_state.alunos_pilares)
                st.rerun()

st.markdown("---")

# Gerar gráfico de radar interativo com Plotly
if st.session_state.alunos_pilares and any(st.session_state.alunos_pilares.values()):
    st.subheader("🎯 Gráfico de Radar Interativo - Evolução por Pilares")
    
    alunos_com_dados = [(aluno, pontos) for aluno, pontos in st.session_state.alunos_pilares.items() if pontos]
    
    if alunos_com_dados:
        for aluno, pontos in alunos_com_dados:
            st.write(f"### 👤 {aluno}")
            
            fig = go.Figure()
            pilares = ['Clareza', 'Impacto', 'Visão', 'Conexão']
            
            for i, (nome_texto, clareza, impacto, visao, conexao) in enumerate(pontos):
                color = CORES_CALOR_REFINADA[i % len(CORES_CALOR_REFINADA)]
                
                fig.add_trace(go.Scatterpolar(
                    r=[clareza, impacto, visao, conexao, clareza],
                    theta=pilares + [pilares[0]],
                    fill='toself',
                    name=nome_texto[:26],
                    line=dict(color=color, width=3),
                    marker=dict(size=8),
                    fillcolor=f"rgba{tuple(list(int(color.lstrip('#')[i:i+2], 16) for i in (0, 2, 4)) + [0.1])}"
                ))
            
            fig.update_layout(
                polar=dict(
                    bgcolor=BG_COLOR,
                    radialaxis=dict(
                        visible=True,
                        range=[0, 5.5],
                        tickvals=[1, 2, 3, 4, 5],
                        tickfont=dict(color=TEXT_COLOR, size=11),
                        gridcolor="rgba(78, 44, 28, 0.2)"
                    ),
                    angularaxis=dict(
                        tickfont=dict(color=TEXT_COLOR, size=18, family="Arial Black"), # Aumentado para 18 e Arial Black
                        gridcolor="rgba(78, 44, 28, 0.2)",
                        rotation=90, # Ajuste de rotação para melhor leitura
                        direction="clockwise"
                    )
                ),
                showlegend=True,
                paper_bgcolor=BG_COLOR,
                plot_bgcolor=BG_COLOR,
                margin=dict(l=100, r=100, t=80, b=80), # Aumentado as margens para acomodar fontes maiores
                legend=dict(font=dict(color=TEXT_COLOR, size=12)),
                hovermode="closest"
            )
            
            st.plotly_chart(fig, use_container_width=True)

else:
    st.info("👉 Adicione um aluno e insira suas avaliações para visualizar o gráfico de radar.")

st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #4E2C1C; font-size: 12px;">
    <p>🎓 Ferramenta de Avaliação por Pilares - Movimento Calor | Clareza, Impacto, Visão, Conexão</p>
    <p style="font-size: 10px; opacity: 0.7;">💾 Seus dados são salvos automaticamente e persistem entre as sessões.</p>
</div>
""", unsafe_allow_html=True)
