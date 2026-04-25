import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
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
    3. **Avalie os Pilares:** Atribua notas (0-5) para cada pilar:
       - 🔹 **Clareza:** Facilidade de compreensão
       - 🔹 **Impacto:** Memorabilidade e engajamento
       - 🔹 **Visão:** Ponto de vista único e filosofia
       - 🔹 **Conexão:** Argumentos e chamada para ação
    4. **Visualize o Radar:** O gráfico mostra a evolução em cada pilar.
    5. **Baixe o Gráfico:** Salve a imagem para análise.
    
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
                with cols[0]:
                    st.write("**Nome do Texto**")
                with cols[1]:
                    st.write("**Clareza**")
                with cols[2]:
                    st.write("**Impacto**")
                with cols[3]:
                    st.write("**Visão**")
                with cols[4]:
                    st.write("**Conexão**")
                with cols[5]:
                    st.write("**Ação**")
                
                # Exibir e permitir edição de cada avaliação
                for i, (nome_texto, clareza, impacto, visao, conexao) in enumerate(st.session_state.alunos_pilares[aluno]):
                    cols = st.columns([2, 1, 1, 1, 1, 1])
                    
                    with cols[0]:
                        novo_nome = st.text_input(
                            f"Nome T{i+1}",
                            value=nome_texto,
                            key=f"nome_edit_{aluno}_{i}",
                            label_visibility="collapsed"
                        )
                    
                    with cols[1]:
                        nova_clareza = st.number_input(
                            f"Clareza T{i+1}",
                            min_value=0.0,
                            max_value=5.0,
                            value=float(clareza),
                            step=0.5,
                            key=f"clareza_edit_{aluno}_{i}",
                            label_visibility="collapsed"
                        )
                    
                    with cols[2]:
                        novo_impacto = st.number_input(
                            f"Impacto T{i+1}",
                            min_value=0.0,
                            max_value=5.0,
                            value=float(impacto),
                            step=0.5,
                            key=f"impacto_edit_{aluno}_{i}",
                            label_visibility="collapsed"
                        )
                    
                    with cols[3]:
                        nova_visao = st.number_input(
                            f"Visão T{i+1}",
                            min_value=0.0,
                            max_value=5.0,
                            value=float(visao),
                            step=0.5,
                            key=f"visao_edit_{aluno}_{i}",
                            label_visibility="collapsed"
                        )
                    
                    with cols[4]:
                        nova_conexao = st.number_input(
                            f"Conexão T{i+1}",
                            min_value=0.0,
                            max_value=5.0,
                            value=float(conexao),
                            step=0.5,
                            key=f"conexao_edit_{aluno}_{i}",
                            label_visibility="collapsed"
                        )
                    
                    with cols[5]:
                        if st.button(f"🗑️", key=f"remove_{aluno}_{i}"):
                            st.session_state.alunos_pilares[aluno].pop(i)
                            salvar_dados(st.session_state.alunos_pilares)
                            st.rerun()
                    
                    # Atualizar os valores se foram alterados
                    if novo_nome != nome_texto or nova_clareza != clareza or novo_impacto != impacto or nova_visao != visao or nova_conexao != conexao:
                        st.session_state.alunos_pilares[aluno][i] = (novo_nome, nova_clareza, novo_impacto, nova_visao, nova_conexao)
                        salvar_dados(st.session_state.alunos_pilares)
                
                st.divider()
            
            # Adicionar novo texto
            st.write(f"**Adicionar Novo Texto para {aluno}**")
            col1, col2, col3, col4, col5, col6 = st.columns([2, 1, 1, 1, 1, 1])
            
            with col1:
                nome_novo_texto = st.text_input(
                    "Nome do Texto",
                    placeholder="Ex: Discurso Empresa, Entrevista",
                    key=f"nome_new_{aluno}"
                )
            
            with col2:
                clareza = st.slider(f"Clareza", 0.0, 5.0, 2.5, 0.5, key=f"clareza_new_{aluno}")
            
            with col3:
                impacto = st.slider(f"Impacto", 0.0, 5.0, 2.5, 0.5, key=f"impacto_new_{aluno}")
            
            with col4:
                visao = st.slider(f"Visão", 0.0, 5.0, 2.5, 0.5, key=f"visao_new_{aluno}")
            
            with col5:
                conexao = st.slider(f"Conexão", 0.0, 5.0, 2.5, 0.5, key=f"conexao_new_{aluno}")
            
            with col6:
                if st.button(f"✅", key=f"add_{aluno}"):
                    nome_final = nome_novo_texto if nome_novo_texto else f"Texto {len(st.session_state.alunos_pilares[aluno]) + 1}"
                    st.session_state.alunos_pilares[aluno].append((nome_final, clareza, impacto, visao, conexao))
                    salvar_dados(st.session_state.alunos_pilares)
                    st.success(f"Avaliação adicionada para {aluno}!")
                    st.rerun()
            
            st.divider()
            
            if st.button(f"🗑️ Remover Todos", key=f"del_all_{aluno}"):
                st.session_state.alunos_pilares[aluno] = []
                salvar_dados(st.session_state.alunos_pilares)
                st.info(f"Todas as avaliações de {aluno} foram removidas!")
                st.rerun()

st.markdown("---")

# Gerar gráfico de radar
if st.session_state.alunos_pilares and any(st.session_state.alunos_pilares.values()):
    st.subheader("🎯 Gráfico de Radar - Evolução por Pilares")
    
    # Criar figura com subplots para cada aluno
    num_alunos = len([a for a in st.session_state.alunos_pilares.values() if a])
    
    if num_alunos > 0:
        # Criar uma figura com um gráfico de radar para cada aluno
        cols_display = st.columns(min(2, num_alunos))
        
        alunos_com_dados = [(aluno, pontos) for aluno, pontos in st.session_state.alunos_pilares.items() if pontos]
        
        # Paleta de cores do Movimento Calor
        cores_calor = ['#E65100', '#8B4513', '#D4A574', '#C85A17', '#A0522D']
        
        for idx, (aluno, pontos) in enumerate(alunos_com_dados):
            with cols_display[idx % len(cols_display)]:
                # Criar figura de radar
                fig, ax = plt.subplots(figsize=(8, 8), subplot_kw=dict(projection='polar'), facecolor=BG_COLOR)
                ax.set_facecolor(BG_COLOR)
                
                # Pilares
                pilares = ['Clareza', 'Impacto', 'Visão', 'Conexão']
                num_pilares = len(pilares)
                
                # Ângulos para cada pilar
                angles = np.linspace(0, 2 * np.pi, num_pilares, endpoint=False).tolist()
                angles += angles[:1]  # Fechar o polígono
                
                # Cores para os textos
                colors = [cores_calor[i % len(cores_calor)] for i in range(len(pontos))]
                
                # Plotar cada texto
                for (nome_texto, clareza, impacto, visao, conexao), color in zip(pontos, colors):
                    valores = [clareza, impacto, visao, conexao]
                    valores += valores[:1]  # Fechar o polígono
                    
                    ax.plot(angles, valores, 'o-', linewidth=2, label=nome_texto[:26], color=color)
                    ax.fill(angles, valores, alpha=0.15, color=color)
                
                # Configurações do gráfico
                ax.set_xticks(angles[:-1])
                
                # Ajuste fino dos rótulos para evitar sobreposição
                # Aumentamos o padding e ajustamos o alinhamento
                ax.set_xticklabels(pilares, size=12, fontweight='bold', color=TEXT_COLOR)
                
                # Afastar os rótulos do centro de forma segura usando padding
                ax.tick_params(axis='x', pad=25)
                
                ax.set_ylim(0, 5.5) # Aumentado para dar mais espaço no topo
                ax.set_yticks([1, 2, 3, 4, 5])
                ax.set_yticklabels(['1', '2', '3', '4', '5'], size=9, color=TEXT_COLOR, alpha=0.7)
                ax.grid(True, color=TEXT_COLOR, alpha=0.3)
                
                # Título
                ax.set_title(f"{aluno}", size=16, fontweight='bold', color=TEXT_COLOR, pad=40)
                
                # Legenda
                ax.legend(loc='upper right', bbox_to_anchor=(1.3, 1.1), fontsize=9)
                
                plt.tight_layout()
                st.pyplot(fig)
                plt.close()
        
        # Botão para baixar todos os gráficos
        st.markdown("---")
        st.write("**Exportar Gráficos:**")
        
        # Gerar um gráfico grande com todos os alunos para download
        if len(alunos_com_dados) > 0:
            fig, axes = plt.subplots(1, len(alunos_com_dados), figsize=(7*len(alunos_com_dados), 7), subplot_kw=dict(projection='polar'), facecolor=BG_COLOR)
            
            if len(alunos_com_dados) == 1:
                axes = [axes]
            
            pilares = ['Clareza', 'Impacto', 'Visão', 'Conexão']
            num_pilares = len(pilares)
            angles = np.linspace(0, 2 * np.pi, num_pilares, endpoint=False).tolist()
            angles += angles[:1]
            
            # Paleta de cores do Movimento Calor
            cores_calor = ['#E65100', '#8B4513', '#D4A574', '#C85A17', '#A0522D']
            
            for ax, (aluno, pontos) in zip(axes, alunos_com_dados):
                ax.set_facecolor(BG_COLOR)
                # Usar cores da paleta Movimento Calor
                colors = [cores_calor[i % len(cores_calor)] for i in range(len(pontos))]
                
                for (nome_texto, clareza, impacto, visao, conexao), color in zip(pontos, colors):
                    valores = [clareza, impacto, visao, conexao]
                    valores += valores[:1]
                    
                    ax.plot(angles, valores, 'o-', linewidth=2, label=nome_texto[:26], color=color)
                    ax.fill(angles, valores, alpha=0.15, color=color)
                
                ax.set_xticks(angles[:-1])
                ax.set_xticklabels(pilares, size=11, fontweight='bold', color=TEXT_COLOR)
                
                # Afastar os rótulos do centro de forma segura usando padding
                ax.tick_params(axis='x', pad=20)
                
                ax.set_ylim(0, 5.5)
                ax.set_yticks([1, 2, 3, 4, 5])
                ax.set_yticklabels(['1', '2', '3', '4', '5'], size=8, color=TEXT_COLOR, alpha=0.7)
                ax.grid(True, color=TEXT_COLOR, alpha=0.3)
                ax.set_title(f"{aluno}", size=14, fontweight='bold', color=TEXT_COLOR, pad=35)
                ax.legend(loc='upper right', bbox_to_anchor=(1.2, 1.1), fontsize=8)
            
            plt.tight_layout()
            
            buffer = BytesIO()
            fig.savefig(buffer, format='png', dpi=300, bbox_inches='tight')
            buffer.seek(0)
            
            st.download_button(
                label="📥 Baixar Todos os Gráficos (PNG)",
                data=buffer,
                file_name="graficos_pilares.png",
                mime="image/png"
            )
            
            plt.close()

else:
    st.info("👉 Adicione um aluno e insira suas avaliações para visualizar o gráfico de radar.")

st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #4E2C1C; font-size: 12px;">
    <p>🎓 Ferramenta de Avaliação por Pilares - Movimento Calor | Clareza, Impacto, Visão, Conexão</p>
    <p style="font-size: 10px; opacity: 0.7;">💾 Seus dados são salvos automaticamente e persistem entre as sessões.</p>
</div>
""", unsafe_allow_html=True)
