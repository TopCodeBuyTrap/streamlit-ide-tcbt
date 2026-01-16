from textwrap import shorten

from APP_Editor_Run_Preview import Editor_Previews
from APP_Menus import Apagar_Arq
from APP_SUB_Customizar import Customization
from APP_SUB_Funcitons import Identificar_linguagem
from APP_SUB_Janela_Explorer import listar_arquivos_e_pastas, Open_Explorer
from APP_Sidebar import Sidebar

from Banco_dados import ler_B_ARQUIVOS_RECENTES
from APP_SUB_Controle_Driretorios import _DIRETORIO_EXECUTAVEL_, _DIRETORIO_PROJETOS_, _DIRETORIO_PROJETO_ATUAL_

import os
from pathlib import Path
from APP_Terminal import Terminal

def Testar_Fluxo_Run(col):

    import time
    agora = time.time()

    if "trafego" not in st.session_state:
        st.session_state.trafego = {}

    t = st.session_state.trafego

    if "reruns" not in t:
        t["reruns"] = 0
    if "inicio" not in t:
        t["inicio"] = agora
    if "ultimo" not in t:
        t["ultimo"] = None
    if "intervalos" not in t:
        t["intervalos"] = []

    t["reruns"] += 1

    if t["ultimo"] is not None:
        t["intervalos"].append(agora - t["ultimo"])

    t["ultimo"] = agora

    tempo_total = agora - t["inicio"]

    col.write(f"Fluxo passou: {t['reruns']}\tTempo: {tempo_total:.3f}")



def app(col1,col2 ):

    # Executando a página selecionada

    if len(ler_B_ARQUIVOS_RECENTES()) == 0:
        st.button('Entar')
        from APP_Menus import Cria_Projeto
        footer_container = st.container(border=True)
        with footer_container:
            st.write('Seja Bem Vindo Ordinario/a !')
            st.image(IMAGEM_LOGO)
        Cria_Projeto(st)

    else:
        with col1:
            from APP_Menus import Abrir_Menu
            Abrir_Menu(st)
        # ============================================================= MENU SUPERIOR
        with col2.expander("⚙️ Configuração de Layot"):
            m1, m2, m3, m4 = st.columns([3, 4, 3, 3])
            # --------------------------------------------------------- 1️⃣ MULTISELECT
            with m1:
                containers_order = st.multiselect(
                    "Painéis",
                    options=["Editor", "Preview", "ChatOllama"],
                    default=["Editor", "Preview", "ChatOllama"], label_visibility="collapsed"
                )
            # --------------------------------------------------------- 2️⃣ LAYOUT
            with m2:
                layout = st.pills(
                    "Layout",
                    options=[1, 2, 3, 4],
                    format_func=lambda x: {
                        1: "Horizontal",
                        2: "Grande + Dois",
                        3: "Dois + Grande",
                        4: "Vertical"
                    }[x],
                    selection_mode="single", label_visibility="collapsed"
                ) or 1
            # --------------------------------------------------------- 3️⃣ ALTURA
            with m3:
                height_mode = st.pills(
                    "Altura",
                    options=["pequeno", "medio", "grande", "extra"],
                    format_func=lambda x: {
                        "pequeno": "Pequeno",
                        "medio": "Médio",
                        "grande": "Grande",
                        "extra": "Extra"

                    }[x],
                    selection_mode="single", label_visibility="collapsed"
                ) or "medio"
            # --------------------------------------------------------- 4️⃣ AJUSTE DE COLUNAS
            with m4:
                col_weights = None

                # ===== Layout 1: 3 colunas → 3 sliders horizontais
                if layout == 1:
                    s1, s2, s3 = st.columns(3)
                    with s1:
                        c1 = st.slider("C1", 1, 10, 4, label_visibility="collapsed")
                    with s2:
                        c2 = st.slider("C2", 1, 10, 3, label_visibility="collapsed")
                    with s3:
                        c3 = st.slider("C3", 1, 10, 3, label_visibility="collapsed")

                    col_weights = [c1, c2, c3]

                # ===== Layout 2: 2 colunas → 2 sliders horizontais
                elif layout == 2:
                    s1, s2 = st.columns(2)
                    with s1:
                        c1 = st.slider("Esq", 1, 10, 6, label_visibility="collapsed")
                    with s2:
                        c2 = st.slider("Dir", 1, 10, 4, label_visibility="collapsed")

                    col_weights = [c1, c2]

                # ===== Layout 3: 2 colunas superiores → 2 sliders horizontais
                elif layout == 3:
                    s1, s2 = st.columns(2)
                    with s1:
                        c1 = st.slider("Sup1", 1, 10, 5, label_visibility="collapsed")
                    with s2:
                        c2 = st.slider("Sup2", 1, 10, 5, label_visibility="collapsed")

                    col_weights = [c1, c2]

                # ===== Layout 4: vertical → sem sliders
                else:
                    col_weights = None
            Customization(st, NOME_CUSTOM)
        #--------------------------------------------------------------------- MENUS DE EDIÇÃO E CRIAÇÃO DE ARQUIVOS
        from  APP_Menus import  Abrir_Menu,Custom
        Pasta_Executavel = _DIRETORIO_EXECUTAVEL_()

        Pasta_Todos_Projetos = _DIRETORIO_PROJETOS_()
        Pasta_Projeto_Atual = _DIRETORIO_PROJETO_ATUAL_()
        Meus_Arquivos = listar_arquivos_e_pastas(Pasta_Projeto_Atual)
        T1, T2 = st.columns([.4, 9])


        #------------------z--------------------------------------------------- SIDIBAR LATERAL
        with st.sidebar:
            st.image(IMAGEM_LOGO)

            caminho_completo = Pasta_Projeto_Atual  # Ex: "C:\\Users\\henri\\PycharmProjects\\IDE_TOP"
            unidade = os.path.splitdrive(caminho_completo)[0]  # Ex: "C:"
            nome_pasta = os.path.basename(caminho_completo)
            if st.button(f'🗂️ {os.path.join(nome_pasta)}',type="tertiary",key='Diretorio',use_container_width=True,):
                Open_Explorer(Pasta_Projeto_Atual)

            RUN_ = col1.button(f'▶️', icon=':material/directions_bike:', shortcut="Ctrl+Enter")
            RUN = col1.button(f'▶️',  key="btn_central_real")

            if RUN_ or RUN:
                RUN_ = True
            #Arq_Selec = Sidebar(st,RUN_,Tab2,Meus_Arquivos,height_mode,containers_order,layout,col_weights,)
            Arq_Selec_Nomes ,Arq_Selec_Diretorios = Sidebar(st,col2,Meus_Arquivos,7)

        Arq_Selec = ''
        if len(Arq_Selec_Diretorios) > 0:
            nomes_abas = [Path(arquivo).name for arquivo in Arq_Selec_Diretorios]  # Só nome final
            tabs = col2.tabs(nomes_abas)

            for i, tab in enumerate(tabs):
                with tab:
                    arquivo = Arq_Selec_Diretorios[i]
                    Editor_Previews(RUN_, arquivo, Identificar_linguagem(arquivo),
                                    height_mode, containers_order, layout, col_weights, i)

                Arq_Selec = arquivo

        #
        Tab1, Tab2 = st.columns([.4, 9])
        val = ''
        with Tab2.expander(f"{val}:material/terminal_output:",  expanded=False):
            # Chamada principal
            Terminal()

        st.write(Arq_Selec)


        caminho = Path(Arq_Selec)  # transforma em Path
        nome_sem_extensao = caminho.stem
        extensao_arquivo = caminho.suffix  # pega a extensão, ex: ".py"
        nome_arquivo = os.path.basename(Arq_Selec)
        if col1.pills(f'Run', ":material/delete:", label_visibility='collapsed'):
            Apagar_Arq(st, Arq_Selec,nome_arquivo)

            #--------------------------------------------------------------------- BUSSCAR ARQUIVOS SELECIONADO
        if Arq_Selec:
            if Arq_Selec.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp', '.webp')):
                footer_container = Tab2.container(border=True,key="meu_container_unico")
                with footer_container:
                    st.image(Arq_Selec, caption=f"🖼️ {os.path.basename(Arq_Selec)}")


#---------------------------
if __name__ == "__main__":
    import streamlit as st

    from Banco_dados import ler_A_CONTROLE_ABSOLUTO, Del_A_CONTROLE_ABSOLUTO,Del_CUSTOMIZATION

    st.set_page_config(page_title="IDE Python Streamlit", layout="wide")

    if 'config_absoluta_ok' not in st.session_state:
        st.session_state.config_absoluta_ok = False

    # 🔹 SE JÁ TEM CONFIG → ENTRA DIRETO NA IDE
    if len(ler_A_CONTROLE_ABSOLUTO()) > 0 or st.session_state.config_absoluta_ok:
        from APP_Htmls import Main_App
        IMAGEM_LOGO ,NOME_CUSTOM, COR_CAMPO,COR_MENU = Main_App(st)
        col1,col2 = st.columns([.3,9])
        app(col1,col2 )

    # 🔹 SENÃO → MOSTRA ABERTURA
    else:
        from Abertura_TCBT import Abertura
        Del_CUSTOMIZATION()

        if Abertura() == True:
            st.rerun()
