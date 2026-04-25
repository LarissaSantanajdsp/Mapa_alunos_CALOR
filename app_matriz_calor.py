import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from io import BytesIO
import json
import os
from datetime import datetime

# Configuração da página
st.set_page_config(page_title="Matriz Calor vs. Competência", layout="wide", initial_sidebar_state="expanded")

# Estilos do Movimento Calor
BG_COLOR = '#F2F0E4'
TEXT_COLOR = '#4E2C1C'
ACCENT_COLOR = '#E65100'
SECONDARY_COLOR = '#8B4513'

# Arquivo de armazenamento de dados
DATA_FILE = "/tmp/matriz_calor_data.json"

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

st.title("📊 Matriz Calor vs. Competência - Evolução de Alunos")
st.markdown("---")

# Sidebar para instruções e gerenciamento de dados
with st.sidebar:
    st.header("📋 Como Usar")
    st.markdown("""
    1. **Adicione um Aluno:** Digite o nome do aluno no campo abaixo.
    2. **Insira as Notas:** Para cada texto, atribua uma nota de Calor (0-100) e Competência (0-100).
    3. **Edite se Necessário:** Clique na tabela para alterar qualquer valor já inserido, incluindo o nome do texto.
    4. **Visualize a Evolução:** O gráfico se atualiza automaticamente.
    5. **Baixe o Gráfico:** Clique no botão para salvar a imagem.
    
    **Legenda dos Quadrantes:**
    - 🟠 **Admiração:** Alto Calor + Alta Competência (Objetivo!)
    - 🟤 **Inveja:** Baixo Calor + Alta Competência
    - 🟤 **Dó:** Alto Calor + Baixa Competência
    - ⚫ **Desprezo:** Baixo Calor + Baixa Competência
    
    ---
    
    **💾 Gerenciamento de Dados:**
    """)
    
    # Opções de gerenciamento de dados
    if st.button("📥 Baixar Backup (JSON)"):
        dados = st.session_state.get('alunos', {})
        json_str = exportar_dados_json(dados)
        st.download_button(
            label="📥 Clique aqui para baixar",
            data=json_str,
            file_name=f"backup_matriz_calor_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
            mime="application/json"
        )
    
    if st.button("🗑️ Limpar Todos os Dados"):
        st.session_state.alunos = {}
        salvar_dados({})
        st.success("✅ Todos os dados foram removidos!")
        st.rerun()

# Inicializar session state com dados persistentes
if 'alunos' not in st.session_state:
    st.session_state.alunos = carregar_dados()

# Seção de entrada de dados
col1, col2 = st.columns([2, 1])

with col1:
    novo_aluno = st.text_input("Nome do Aluno:", placeholder="Ex: João Silva")

with col2:
    if st.button("➕ Adicionar Aluno"):
        if novo_aluno and novo_aluno not in st.session_state.alunos:
            st.session_state.alunos[novo_aluno] = []
            salvar_dados(st.session_state.alunos)
            st.success(f"Aluno '{novo_aluno}' adicionado!")
            st.rerun()
        elif novo_aluno in st.session_state.alunos:
            st.warning(f"Aluno '{novo_aluno}' já existe!")

st.markdown("---")

# Exibir alunos e permitir entrada de dados
if st.session_state.alunos:
    st.subheader("📝 Avaliação de Textos")
    
    for aluno in st.session_state.alunos:
        with st.expander(f"👤 {aluno}", expanded=False):
            # Mostrar e permitir edição de textos já avaliados
            if st.session_state.alunos[aluno]:
                st.write("**Textos Avaliados (Clique para Editar):**")
                
                # Criar colunas para edição
                cols = st.columns([2, 1, 1, 1])
                with cols[0]:
                    st.write("**Nome do Texto**")
                with cols[1]:
                    st.write("**Calor**")
                with cols[2]:
                    st.write("**Competência**")
                with cols[3]:
                    st.write("**Ação**")
                
                # Exibir e permitir edição de cada avaliação
                for i, (nome_texto, calor, competencia) in enumerate(st.session_state.alunos[aluno]):
                    cols = st.columns([2, 1, 1, 1])
                    
                    with cols[0]:
                        novo_nome = st.text_input(
                            f"Nome T{i+1}",
                            value=nome_texto,
                            key=f"nome_edit_{aluno}_{i}",
                            label_visibility="collapsed"
                        )
                    
                    with cols[1]:
                        novo_calor = st.number_input(
                            f"Calor T{i+1}",
                            min_value=0,
                            max_value=100,
                            value=calor,
                            step=1,
                            key=f"calor_edit_{aluno}_{i}",
                            label_visibility="collapsed"
                        )
                    
                    with cols[2]:
                        nova_competencia = st.number_input(
                            f"Competência T{i+1}",
                            min_value=0,
                            max_value=100,
                            value=competencia,
                            step=1,
                            key=f"comp_edit_{aluno}_{i}",
                            label_visibility="collapsed"
                        )
                    
                    with cols[3]:
                        if st.button(f"🗑️ Remover", key=f"remove_{aluno}_{i}"):
                            st.session_state.alunos[aluno].pop(i)
                            salvar_dados(st.session_state.alunos)
                            st.rerun()
                    
                    # Atualizar os valores se foram alterados
                    if novo_nome != nome_texto or novo_calor != calor or nova_competencia != competencia:
                        st.session_state.alunos[aluno][i] = (novo_nome, novo_calor, nova_competencia)
                        salvar_dados(st.session_state.alunos)
                
                st.divider()
            
            # Adicionar novo texto
            st.write(f"**Adicionar Novo Texto para {aluno}**")
            col1, col2, col3, col4 = st.columns([2, 1, 1, 1])
            
            with col1:
                nome_novo_texto = st.text_input(
                    "Nome do Texto",
                    placeholder="Ex: E-mail, Apresentação, Conversa",
                    key=f"nome_new_{aluno}"
                )
            
            with col2:
                calor = st.slider(f"Calor", 0, 100, 50, key=f"calor_new_{aluno}")
            
            with col3:
                competencia = st.slider(f"Competência", 0, 100, 50, key=f"comp_new_{aluno}")
            
            with col4:
                if st.button(f"✅ Adicionar", key=f"add_{aluno}"):
                    nome_final = nome_novo_texto if nome_novo_texto else f"Texto {len(st.session_state.alunos[aluno]) + 1}"
                    st.session_state.alunos[aluno].append((nome_final, calor, competencia))
                    salvar_dados(st.session_state.alunos)
                    st.success(f"Avaliação adicionada para {aluno}!")
                    st.rerun()
            
            st.divider()
            
            if st.button(f"🗑️ Remover Todos", key=f"del_all_{aluno}"):
                st.session_state.alunos[aluno] = []
                salvar_dados(st.session_state.alunos)
                st.info(f"Todas as avaliações de {aluno} foram removidas!")
                st.rerun()

st.markdown("---")

# Gerar gráfico
if st.session_state.alunos and any(st.session_state.alunos.values()):
    st.subheader("📈 Gráfico de Evolução")
    
    # Criar figura
    fig, ax = plt.subplots(figsize=(12, 9), facecolor=BG_COLOR)
    ax.set_facecolor(BG_COLOR)
    
    # Limites dos eixos
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 100)
    
    # Linhas centrais (Quadrantes)
    ax.axhline(50, color=TEXT_COLOR, linestyle='--', alpha=0.3, linewidth=1.5)
    ax.axvline(50, color=TEXT_COLOR, linestyle='--', alpha=0.3, linewidth=1.5)
    
    # Preenchimento dos quadrantes
    ax.fill_between([0, 50], 50, 100, color=SECONDARY_COLOR, alpha=0.05)
    ax.fill_between([50, 100], 50, 100, color=ACCENT_COLOR, alpha=0.05)
    ax.fill_between([0, 50], 0, 50, color=TEXT_COLOR, alpha=0.05)
    ax.fill_between([50, 100], 0, 50, color=SECONDARY_COLOR, alpha=0.05)
    
    # Rótulos dos quadrantes
    ax.text(25, 75, 'INVEJA', ha='center', va='center', color=TEXT_COLOR, alpha=0.4, fontsize=14, fontweight='bold')
    ax.text(75, 75, 'ADMIRAÇÃO', ha='center', va='center', color=ACCENT_COLOR, alpha=0.4, fontsize=14, fontweight='bold')
    ax.text(25, 25, 'DESPREZO', ha='center', va='center', color=TEXT_COLOR, alpha=0.4, fontsize=14, fontweight='bold')
    ax.text(75, 25, 'DÓ', ha='center', va='center', color=TEXT_COLOR, alpha=0.4, fontsize=14, fontweight='bold')
    
    # Plotar os dados dos alunos
    colors = plt.cm.tab10(np.linspace(0, 1, len(st.session_state.alunos)))
    
    for (aluno, pontos), color in zip(st.session_state.alunos.items(), colors):
        if pontos:  # Se há dados para este aluno
            calor = [p[1] for p in pontos]
            competencia = [p[2] for p in pontos]
            nomes = [p[0] for p in pontos]
            
            # Plotar a linha de evolução
            ax.plot(calor, competencia, marker='o', linestyle='-', linewidth=2.5, markersize=10, label=aluno, color=color)
            
            # Adicionar nomes dos textos aos pontos
            for i, (c, comp, nome) in enumerate(zip(calor, competencia, nomes)):
                # Limitar o nome a 20 caracteres para o gráfico
                label = nome[:20] + '...' if len(nome) > 20 else nome
                ax.annotate(label, (c, comp), textcoords="offset points", xytext=(8, 8), ha='left', fontsize=9, color=color, fontweight='bold')
            
            # Destacar o último ponto
            ax.plot(calor[-1], competencia[-1], marker='*', markersize=20, color=color, markeredgecolor='white', markeredgewidth=1.5)
    
    # Configurações dos eixos
    ax.set_xlabel('Calor (Warmth) - Empatia e Conexão', fontsize=13, fontweight='bold', color=TEXT_COLOR)
    ax.set_ylabel('Competência - Habilidade e Eficácia', fontsize=13, fontweight='bold', color=TEXT_COLOR)
    ax.set_title('Evolução da Comunicação: Matriz Calor vs. Competência', fontsize=16, fontweight='bold', color=TEXT_COLOR, pad=20)
    
    # Remover bordas
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['bottom'].set_color(TEXT_COLOR)
    ax.spines['left'].set_color(TEXT_COLOR)
    
    # Legenda
    ax.legend(loc='upper left', bbox_to_anchor=(1.02, 1), borderaxespad=0., frameon=False, fontsize=11)
    
    plt.tight_layout()
    
    # Exibir gráfico
    st.pyplot(fig)
    
    # Botão para baixar
    buffer = BytesIO()
    fig.savefig(buffer, format='png', dpi=300, bbox_inches='tight')
    buffer.seek(0)
    
    st.download_button(
        label="📥 Baixar Gráfico (PNG)",
        data=buffer,
        file_name="evolucao_alunos.png",
        mime="image/png"
    )
    
    plt.close()

else:
    st.info("👉 Adicione um aluno e insira suas avaliações para visualizar o gráfico.")

st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #4E2C1C; font-size: 12px;">
    <p>🎓 Ferramenta de Avaliação - Movimento Calor | Desenvolvido para acompanhar a evolução de comunicação dos alunos</p>
    <p style="font-size: 10px; opacity: 0.7;">💾 Seus dados são salvos automaticamente e persistem entre as sessões.</p>
</div>
""", unsafe_allow_html=True)
