from Banco_Predefinitions import carregar_config_atual, salvar_config_atual


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

def select_arquivo_recente(col2):
    st.sidebar.image('.arquivos/logo_.png',width=100)


    registros = ler_A_CONTROLE_PROJETOS()
    if not registros:
        return None, None, None

    # registros =
    # (DIRETORIO_TRABALHANDO, VERSION, DATA, DIRETORIOS, ARQUIVOS, OBS)
    ordenar_por = st.selectbox(
        "Ordenar por:",
        ["Último usado", "Data", "Versão", "Ordem alfabética (agrupado)"],
        key="ordenacao_recente",label_visibility='collapsed'
    )

    dados = []
    for r in registros:
        caminho, versao, data = r[0], r[1], r[2]
        dados.append({
            "caminho": caminho,
            "nome": os.path.basename(caminho),
            "versao": versao,
            "data": data
        })

    if ordenar_por == "Último usado":
        dados = sorted(
            dados,
            key=lambda x: x["data"] or "",
            reverse=True
        )

    elif ordenar_por == "Data":
        dados = sorted(
            dados,
            key=lambda x: datetime.fromisoformat(x["data"]) if x["data"] else datetime.min,
            reverse=True
        )

    elif ordenar_por == "Versão":
        dados = sorted(
            dados,
            key=lambda x: (x["versao"] or "").lower()
        )

    elif ordenar_por == "Ordem alfabética (agrupado)":
        grupos = {}
        for d in dados:
            grupos.setdefault(d["nome"], []).append(d)

        dados = []
        for nome in sorted(grupos.keys(), key=str.lower):
            grupo = sorted(
                grupos[nome],
                key=lambda x: datetime.fromisoformat(x["data"]) if x["data"] else datetime.min
            )
            dados.extend(grupo)

    if "projeto_idx" not in st.session_state:
        st.session_state.projeto_idx = 0
        col2.write("LOG: seleção inicial definida")

    selecionado = st.selectbox(
        "Projetos recentes",
        options=range(len(dados)),
        format_func=lambda i: dados[i]["nome"],
        key="projeto_idx",label_visibility='collapsed'
    )

    if "ultimo_idx" not in st.session_state:
        st.session_state.ultimo_idx = selecionado

    if selecionado != st.session_state.ultimo_idx:
        col2.write("LOG: projeto trocado")
        st.session_state.ultimo_idx = selecionado

    item = dados[selecionado]
    if st.button(f'Acesar',use_container_width=True):
        data = contar_estrutura(item["caminho"])
        versao_set = data["versoes"][0]
        esc_A_CONTROLE_PROJETOS(str(item["caminho"]), list(versao_set)[0], data_sistema(), data["pastas"], data["arquivos"] , '')


def app():


    LOG = []
    # USO

    pjt = ler_A_CONTROLE_PROJETOS()[-1]
    caminho = pjt[0]
    versao =  pjt[1]
    data =   pjt[2]

    if se_B_ARQUIVOS_RECENTES(caminho) == False:
        Del_B_ARQUIVOS_RECENTES()
        esc_B_ARQUIVOS_RECENTES(Path(caminho), str(contar_estrutura(caminho)))
        LOG.append(f'Escaneando a Estrutura da Pasta e Arquivos!')

    #st.code()
    if len(ler_B_ARQUIVOS_RECENTES()) == 0:
        st.button('Entar')
        from APP_Menus import Cria_Projeto
        footer_container = st.container(border=True)
        with footer_container:
            st.write('Seja Bem Vindo Ordinario/a !')
            st.image(IMAGEM_LOGO)
        Cria_Projeto(st)

    else:

        Top1,Top2 ,Top3 ,Top4,Top5,Top6,Top7,Top8,Top9= st.columns([.4,.4,.4,.4,.4,.4,3,1,1])
        Linha_Sep(COR_MENU,.7)
        from APP_Menus import Abrir_Menu
        #Abrir_Menu(st)
        # ============================================================= MENU SUPERIOR
        if Top2.button(":material/refresh:",icon='♻️',help='limpar os caches do app'.title()):
            limpar_CASH()
        with Top3:
            btnt = Button_Nao_Fecha(':material/settings:'+":material/keyboard_double_arrow_left:",
            ':material/settings:' + ':material/keyboard_double_arrow_right:', key="botao_layout")

        if btnt:
            m1, m2, m3, m4 , m5 = Top4.columns([4, 5, 4, 3,1])

            # 🔄 CARREGA CONFIGURAÇÃO ANTERIOR
            config_salva = carregar_config_atual()
            containers_order = config_salva['containers_order'] if config_salva else ["Editor", "Preview",
                                                                                      "CodChat"]
            layout = config_salva['layout'] if config_salva else 1
            height_mode = config_salva['height_mode'] if config_salva else "medio"
            col_weights = config_salva['col_weights'] if config_salva else None

            # --------------------------------------------------------- 1️⃣ MULTISELECT
            with m1:
                containers_order = st.multiselect(
                    "Painéis",
                    options=["Editor", "Preview", "CodChat"],
                    default=containers_order,
                    label_visibility="collapsed"
                )

            # --------------------------------------------------------- 2️⃣ LAYOUT
            with m2:
                layout = st.radio(
                    "Layout",
                    options=[1, 2, 3, 4],
                    index=[1, 2, 3, 4].index(layout) if layout in [1, 2, 3, 4] else 0,
                    format_func=lambda x: {1: "Horizontal", 2: "Um Dois", 3: "Dois Um", 4: "Vertical"}[
                        x],
                    horizontal=True,
                    label_visibility="collapsed"
                ) or 1

            # --------------------------------------------------------- 3️⃣ ALTURA
            with m3:
                height_mode = st.radio(
                    "Altura",
                    options=["pequeno", "medio", "grande", "extra"],
                    index=["pequeno", "medio", "grande", "extra"].index(height_mode) if height_mode in ["pequeno",
                                                                                                        "medio",
                                                                                                        "grande",
                                                                                                        "extra"] else 1,
                    format_func=lambda x: {"pequeno": "P", "medio": "M", "grande": "G", "extra": "E"}[x],
                    horizontal=True,
                    label_visibility="collapsed"
                ) or "medio"

            # --------------------------------------------------------- 4️⃣ AJUSTE DE COLUNAS
            with m4:
                total_peso = 10
                if layout == 1:
                    s1, s2 = st.columns(2)
                    c1 = s1.slider("C1", 1, total_peso - 2, 4, key="c1_l1",label_visibility='collapsed')
                    c2 = s2.slider("C2", 1, total_peso - 2, 3, key="c2_l1",label_visibility='collapsed')
                    c3 = total_peso - c1 - c2
                    col_weights = [c1, c2, c3]
                elif layout == 2:
                    c1 = st.slider("Esq", 1, total_peso - 1, 6, key="c1_l2",label_visibility='collapsed')
                    c2 = total_peso - c1
                    col_weights = [c1, c2]
                elif layout == 3:
                    c1 = st.slider("Sup1", 1, total_peso - 1, 5, key="c1_l3",label_visibility='collapsed')
                    c2 = total_peso - c1
                    col_weights = [c1, c2]

            # 💾 SALVA AUTOMATICAMENTE toda vez que muda
            if m5.button('Salvar'):
                salvar_config_atual(containers_order, layout, height_mode, col_weights)
            #Customization(st, NOME_CUSTOM)

        else:

            # Se o botão não está ativo, devolve as variáveis padrão
            config_salva = carregar_config_atual()
            containers_order = config_salva['containers_order'] if config_salva else ["Editor", "Preview", "CodChat"]
            layout = config_salva['layout'] if config_salva else 1
            height_mode = config_salva['height_mode'] if config_salva else "medio"
            col_weights = config_salva['col_weights'] if config_salva else None

        #--------------------------------------------------------------------- MENUS DE EDIÇÃO E CRIAÇÃO DE ARQUIVOS
        from  APP_Menus import  Abrir_Menu,Custom
        Pasta_Executavel = _DIRETORIO_EXECUTAVEL_()
        Pasta_Todos_Projetos = _DIRETORIO_PROJETOS_()
        Pasta_Projeto_Atual = caminho
        Meus_Arquivos = listar_arquivos_e_pastas(Pasta_Projeto_Atual)

        # Exemplo de uso
        with Top1:
            btnt = Button_Nao_Fecha(':material/folder_open:'+":material/keyboard_double_arrow_left:",
            ':material/folder:' + ':material/keyboard_double_arrow_right:', key="botao_diretorio")
        if btnt:
            col1, col2 = st.columns([1.2, 7])
            vl = 400
            with col1.container(border=True, width=vl,height=500):
                Abrir_Menu(st)
                select_arquivo_recente(st)

                # Arq_Selec_Nomes ,Arq_Selec_Diretorios = Sidebar(st,Pasta_Projeto_Atual)
        else:
            col1, col2 = st.columns([.2, 9])

        #------------------z--------------------------------------------------- SIDIBAR LATERAL
        with st.sidebar:
            caminho_completo = Pasta_Projeto_Atual  # Ex: "C:\\Users\\henri\\PycharmProjects\\IDE_TOP"
            unidade = os.path.splitdrive(caminho_completo)[0]  # Ex: "C:"
            nome_pasta = os.path.basename(caminho_completo)
            Arq_Selec_Nomes, Arq_Selec_Diretorios = Sidebar_Diretorios(st, Meus_Arquivos, 7)

        if Top8.button(f':material/search: {os.path.join(nome_pasta)}',use_container_width=True, type="secondary"):
            Open_Explorer(Pasta_Projeto_Atual)

        if len(Arq_Selec_Diretorios) > 0:
            try:
                nome_arquivo, Arq_Selec = Editor_Simples(col2,Top7,Arq_Selec_Diretorios,THEMA_EDITOR, EDITOR_TAM_MENU,FONTE_MENU)
            except UnicodeDecodeError:
                st.warning('Arquivo não Reconhecido GmeOver!')

            Terminal_Completo(THEMA_PREVIEW, PREVIEW_TAM_MENU)




            Tab1, Tab2 = st.columns([.4, 9])

            val = ''
            with Tab2.expander(f"{val}:material/terminal_output:",  expanded=False):
                # Chamada principal
                Terminal(THEMA_TERMINAL,TERMINAL_TAM_MENU)


            if Arq_Selec:
                caminho = Path(Arq_Selec)  # transforma em Path
                nome_sem_extensao = caminho.stem
                extensao_arquivo = caminho.suffix  # pega a extensão, ex: ".py"
                nome_arquivo = os.path.basename(Arq_Selec)

                #--------------------------------------------------------------------- BUSSCAR ARQUIVOS SELECIONADO
                if Arq_Selec.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp', '.webp')):
                    footer_container = Tab2.container(border=True,key="meu_container_unico")
                    with footer_container:
                        st.image(Arq_Selec, caption=f"🖼️ {os.path.basename(Arq_Selec)}")


#---------------------------
if __name__ == "__main__":
    import streamlit as st
    from datetime import datetime
    from APP_Editor_Run_Preview import Editor_Simples, Terminal_Completo
    from APP_Menus import Apagar_Arq
    from APP_SUB_Customizar import Customization
    from APP_SUB_Funcitons import Identificar_linguagem, escreve, chec_se_arq_do_projeto, contar_estrutura, \
    Button_Nao_Fecha, data_sistema, resumo_pasta, limpar_CASH, Linha_Sep
    from APP_SUB_Janela_Explorer import listar_arquivos_e_pastas, Open_Explorer, Abrir_Arquivo_Select_Tabs
    from APP_Sidebar import  Sidebar_Diretorios
    from Banco_dados import ler_A_CONTROLE_PROJETOS, ler_B_ARQUIVOS_RECENTES, ATUAL_B_ARQUIVOS_RECENTES, \
    se_B_ARQUIVOS_RECENTES, esc_B_ARQUIVOS_RECENTES, Del_B_ARQUIVOS_RECENTES, ler_A_CONTROLE_ABSOLUTO, \
    Del_A_CONTROLE_ABSOLUTO, Del_CUSTOMIZATION, esc_A_CONTROLE_PROJETOS
    from APP_SUB_Controle_Driretorios import _DIRETORIO_EXECUTAVEL_, _DIRETORIO_PROJETOS_, _DIRETORIO_PROJETO_ATUAL_

    import os
    from pathlib import Path
    from APP_Terminal import Terminal

    st.set_page_config(page_title="IDE Python Streamlit", layout="wide")

    if 'config_absoluta_ok' not in st.session_state:
        st.session_state.config_absoluta_ok = False

    # 🔹 SE JÁ TEM CONFIG → ENTRA DIRETO NA IDE
    if len(ler_A_CONTROLE_ABSOLUTO()) > 0 or st.session_state.config_absoluta_ok:
        from APP_Htmls import Carregamento_BancoDados_Temas
        (IMAGEM_LOGO, NOME_CUSTOM, NOME_USUARIO, COR_CAMPO, COR_MENU, THEMA_EDITOR, EDITOR_TAM_MENU,THEMA_PREVIEW,PREVIEW_TAM_MENU,
         THEMA_TERMINAL,TERMINAL_TAM_MENU,TOP_CAB,FONTE_MENU,FONTE_CAMPO) = Carregamento_BancoDados_Temas(st)
        app( )

    # 🔹 SENÃO → MOSTRA ABERTURA
    else:
        from Abertura_TCBT import Abertura
        Del_CUSTOMIZATION()

        if Abertura() == True:
            st.rerun()
