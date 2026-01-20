import streamlit as st
from streamlit_ace import st_ace
import sys
import threading
import queue
import os
import re

from APP_Chats_IA import gerar_codigo, CODOLLAMA_CHAT
from APP_Menus import Apagar_Arq
from APP_SUB_Funcitons import Anotations_Editor, Marcadores_Editor, wrap_text, chec_se_arq_do_projeto, \
    Identificar_linguagem, Button_Nao_Fecha
from APP_SUB_Janela_Explorer import Abrir_Arquivo_Select_Tabs
from Banco_dados import ler_CUSTOMIZATION_coluna
from APP_SUB_Controle_Driretorios import _DIRETORIO_PROJETO_ATUAL_
from streamlit_monaco_editor import st_monaco
from code_editor import code_editor

from SUB_Traduz_terminal import traduzir_saida


# Funções auxiliares (Certifique-se que estão acessíveis ou no mesmo arquivo)
def smart_paste_format(code):
    if not code: return code
    lines = code.split('\n')
    formatted = [line.rstrip().replace('\t', '    ') for line in lines]
    result = '\n'.join(formatted)
    return re.sub(r'\n{3,}', '\n\n', result)




# Função auxiliar para verificar arquivos (assumindo que já existe no seu código)
# from sua_lib import chec_se_arq_do_projeto, Identificar_linguagem, Abrir_Arquivo_Select_Tabs, Button_Nao_Fecha, Apagar_Arq




def Terminal_Completo(THEMA_PREVIEW, PREVIEW_TAM_MENU):
    """Terminal inteligente - toda a mágica aqui"""
    _ = st.session_state

    # ✅ LÊ A ABA EXECUTADA PELO ID (NÃO pelo nome genérico)
    if 'aba_executando_id' in _ and _.aba_executando_id is not None:
        aba_id = _.aba_executando_id
        aba_nome = _.aba_executando
        st.success(f"⬆️ ID {aba_id} - Aba {aba_nome} recebida do editor!")

    # Inicialização (igual seu código original)
    defaults = {
        'code_committed': "",
        'output': "",
        'input_queue': queue.Queue(),
        'output_queue': queue.Queue(),
        'thread_running': False,
    }
    for key, value in defaults.items():
        if key not in _:
            _[key] = value

    class CustomStdout:
        def __init__(self, output_q): self.output_q = output_q

        def write(self, s):
            if s and s.strip(): self.output_q.put(s.rstrip('\n'))

        def flush(self): pass

    def run_code_thread(code, input_q, output_q):
        def custom_input(prompt=""):
            if prompt: output_q.put(prompt)
            return input_q.get()

        stdout_redirect = CustomStdout(output_q)
        old_stdout = sys.stdout
        sys.stdout = stdout_redirect

        try:
            exec(code, {'input': custom_input, '__name__': '__main__'})
            output_q.put("\n✓ Programa finalizado com sucesso!")
        except Exception as e:
            output_q.put(f"\n❌ Erro: {str(e)}")
        finally:
            sys.stdout = old_stdout
            output_q.put("PROGRAM_FINISHED")

    # ✅ EXECUTA quando recebe código da aba
    if 'codigo_para_executar' in _ and _.codigo_para_executar and not _.thread_running:
        _.code_committed = _.codigo_para_executar
        _.output = f"🚀 Executando código da Aba {_.get('aba_executando', '?')}...\n"
        _.input_queue = queue.Queue()
        _.output_queue = queue.Queue()
        _.thread_running = True

        thread = threading.Thread(
            target=run_code_thread,
            args=(_.code_committed, _.input_queue, _.output_queue),
            daemon=True
        )
        thread.start()

    # Processa output da thread
    try:
        while True:
            msg = _.output_queue.get_nowait()
            if msg == "PROGRAM_FINISHED":
                _.thread_running = False
                break
            _.output += msg + '\n'
    except queue.Empty:
        pass
    st.warning('Arquivo não Reconhecido GmeOver!')

    st.markdown(f'''

    ''', unsafe_allow_html=True)
    with st.container(border=True, key='Terminal_preview', width=900):
        with st.expander('**:material/directions_bike: :material/code:**'):
            preview = st_ace(
                value=_.output,
                language='kotlin',  #"abap", "css", "kotlin", "less", "markdown", "python"
                height=450,
                font_size=PREVIEW_TAM_MENU,
                theme=THEMA_PREVIEW,
                auto_update=True,
                show_gutter=False,
                show_print_margin=False,
                wrap=True,
                key=_.output,
                placeholder="Clique EXECUTAR em qualquer aba para ver o resultado aqui!"
            )

    # Input handling
    if _.output and _.thread_running:
        if len(preview) > len(_.output):
            delta = preview[len(_.output):]
            if delta.endswith("\n"):
                clean_input = delta.rstrip("\n").strip()
                if clean_input:
                    _.input_queue.put(clean_input)
                    _.output = preview
                    st.rerun()

    # ✅ RESETA se não tem código ou aba válida
    if ('codigo_para_executar' not in _ or
            not _.codigo_para_executar or
            'aba_executando_id' not in _):
        _.output = ""
        st.info("Pronto para receber código de qualquer aba!")
        return
def Editor_Simples(Coluna, ColunaRun, Caminho, THEMA_EDITOR, EDITOR_TAM_MENU,FONTE):
    _ = st.session_state
    ab = []

    # -------------------------------------------------------------------- LEITURA DAS ABAS
    nomes_abas = [arquivo for arquivo in chec_se_arq_do_projeto(Caminho)]
    tabs = Coluna.tabs(nomes_abas)

    for IDES, tab in enumerate(tabs):
        with tab:
            _.tab_atual = IDES

            Diretorio = Caminho[IDES]
            Aba_Atual = os.path.basename(Diretorio)
            linguagem = Identificar_linguagem(Diretorio)

            content_key = f"conteudo_arquivo_{IDES}"
            if content_key not in _:
                _[content_key] = (
                    Abrir_Arquivo_Select_Tabs(st, Diretorio)
                    if os.path.isfile(Diretorio)
                    else ""
                )

            code = st_ace(
                value=_[content_key],
                language=linguagem,
                theme=THEMA_EDITOR,  # Tema fixo como solicitado
                font_size=EDITOR_TAM_MENU,
                height=850,
                auto_update=True,
                wrap=True,
                annotations=Anotations_Editor(_[content_key]),
                markers=Marcadores_Editor(_[content_key]),
                show_print_margin=True,
                key=f"editor_{IDES}",
            )

            _[content_key] = code

            if Diretorio:
                with open(Diretorio, "w", encoding="utf-8") as f:
                    f.write(code)

            ab.append(Aba_Atual)
            ab.append(Diretorio)

    # -------------------------------------------------------------------- RUN ÚNICO (FORA DO LOOP)
    with ColunaRun:
        _.setdefault("aba_executando_id", None)
        _.setdefault("aba_executando", None)
        _.setdefault("thread_running", False)

        col_btn_apag,col_sel, col_btn_run, col_btn_stop = st.columns([1,4, 1.3, 1.3])

        with col_btn_apag:
            if Button_Nao_Fecha('🖕', ":material/delete:",key="botao_apagar_arquivos"):
                with st.container(border=True, key='Braço_Sidebar', width=900):


                    Apagar_Arq(st, Aba_Atual,Diretorio)



        with col_sel:
            aba_escolhida = st.selectbox(
                "Arquivo",
                nomes_abas,
                key="select_run_unico",
                label_visibility="collapsed",
            )

        with col_btn_run:
            executar = st.button(':material/directions_bike:', shortcut="Ctrl+Enter", key="btn_run_unico")

        with col_btn_stop:
            parar = st.button(':material/stop:', shortcut="Ctrl+Space", key="btn_stop_unico")

        if executar:
            IDES = nomes_abas.index(aba_escolhida)
            Diretorio = Caminho[IDES]
            content_key = f"conteudo_arquivo_{IDES}"

            if _.get("thread_running"):
                _.thread_running = False
                if "output_queue" in _:
                    _.output_queue.put("PROGRAM_FINISHED")

            _.codigo_para_executar = _.get(content_key, "")
            _.aba_executando = aba_escolhida
            _.aba_executando_id = IDES
            _.nova_execucao_solicitada = True

            st.toast(f"⬆️ ID {_.aba_executando_id} - Aba {_.aba_executando} enviada pro terminal!")
            st.rerun()

        # No seu código da função Editor_Simples, procure por esse bloco:

        if parar:
            if _.get("thread_running"):
                _.thread_running = False
                # ADICIONE A LINHA ABAIXO:
                _.output_queue.put("PROGRAM_FINISHED")

                st.toast("🛑 Execução interrompida!")
            else:
                st.toast("ℹ️ Nenhuma execução em andamento")
            st.rerun()

    return ab[0], ab[1]


def Editor_Simples_ed(Coluna, ColunaRun, Caminho, THEMA_EDITOR, EDITOR_TAM_MENU, FONTE):
    _ = st.session_state
    ab = []

    # 1. Gerencia estado da aba ativa
    if "aba_ativa_index" not in _:
        _.aba_ativa_index = 0

    nomes_abas = [arquivo for arquivo in chec_se_arq_do_projeto(Caminho)]

    # Validação do índice
    if _.aba_ativa_index >= len(nomes_abas):
        _.aba_ativa_index = 0

    # -------------------------------------------------------------------- SELETOR DE ARQUIVOS
    with Coluna:
        # Usamos radio horizontal para simular abas (Muito mais leve que st.tabs)
        # Se quiser botões tipo "Pills", use st.pills se sua versão do Streamlit suportar
        aba_selecionada = st.radio(
            "📍 Arquivos do Projeto",
            options=nomes_abas,
            index=_.aba_ativa_index,
            horizontal=True,
            label_visibility="collapsed",
            key="nav_abas_editor_simples"
        )
        st.divider()

        # Atualiza índice
        if aba_selecionada in nomes_abas:
            IDES = nomes_abas.index(aba_selecionada)
            _.aba_ativa_index = IDES
        else:
            IDES = 0

        # -------------------------------------------------------------------- EDITOR MASTER
        Diretorio = Caminho[IDES]
        Aba_Atual = os.path.basename(Diretorio)
        linguagem = Identificar_linguagem(Diretorio)  # Ex: "python", "javascript"
        st.write(linguagem)
        content_key = f"conteudo_arquivo_{Diretorio}"

        # Carrega do disco se não estiver na memória
        if content_key not in _:
            _[content_key] = (
                Abrir_Arquivo_Select_Tabs(st, Diretorio)
                if os.path.isfile(Diretorio)
                else ""
            )

        # CONFIGURAÇÃO DO NOVO EDITOR
        # theme="contrast" é similar ao merbivore/escuro de alto contraste
        # Você pode usar "dark", "light", "github", "xcode", etc.

        # Opções personalizadas para parecer profissional
        opcoes_editor = {
            # VISUAL
            "wrap": True ,
            "fontSize": EDITOR_TAM_MENU,  # Tamanho da fonte
            "fontFamily": FONTE,  # Fonte (use 'Fira Code', 'JetBrains Mono', etc.)
            "showLineNumbers": True,  # Mostrar números de linha
            "highlightActiveLine": True,  # Destacar linha atual
            "showGutter": True,  # Mostrar gutter (margem esquerda)
            "showPrintMargin": True,  # Mostrar margem de impressão
            "printMarginColumn": -.1,  # Coluna da margem de impressão

            # CURSOR E SELEÇÃO
            "highlightSelectedWord": True,  # Destacar todas ocorrências da palavra selecionada
            "readOnly": False,  # Apenas leitura
            "showInvisibles": False,  # Mostrar caracteres invisíveis
            "fadeFoldWidgets": True,  # Fade nos widgets de fold

            # COMPORTAMENTO
            "tabSize": 4,  # Tamanho da tabulação
            "useSoftTabs": True,  # Usar spaces em vez de tabs
            "enableBasicAutocompletion": True,  # Autocompletar básico
            "enableLiveAutocompletion": True,  # Autocompletar em tempo real
            "enableSnippets": True,  # Suporte a snippets
            "maxLines": 20,  # Máximo de linhas

        }

        btn_settings_editor_btns = [{
            "name": "copy",
            "feather": "Copy",
            "hasText": True,
            "alwaysOn": True,
            "commands": ["copyAll"],
            "style": {"top": "0rem", "right": "0.4rem"}
        }, {
            "name": "update",
            "feather": "RefreshCw",
            "primary": True,
            "hasText": True,
            "showWithIcon": True,
            "commands": ["submit"],
            "style": {"bottom": "0rem", "right": "0.4rem"}
        }]

        # RENDERIZAÇÃO
        # O code_editor retorna um dicionário: {'text': "...", 'type': "..."} 'dark'
        response_dict = code_editor(
            _[content_key],
            lang='python',
            theme = THEMA_EDITOR,  # TEMA ESTÁVEL! Não some no rerun.
            height=f'200px',  # Altura dinâmica (min, max linhas) ou fixa "850px"
            options=opcoes_editor,
            shortcuts= 'vscode',
            editor_props={
                "annotations": Anotations_Editor(_[content_key]),
                "markers": Marcadores_Editor(_[content_key]),
                "style": {"borderRadius": "1px 2px 8px 8px"}  # Estilo customizado
            },
            buttons=btn_settings_editor_btns,
            # Key baseada no arquivo garante que ao trocar de aba, o editor recarregue corretamente

        )

        # Lógica de Salvamento: Só salva se houve alteração de texto
        if response_dict['type'] == "submit" or (
                response_dict['text'] != "" and response_dict['text'] != _[content_key]):
            novo_codigo = response_dict['text']

            # Atualiza estado e disco
            if novo_codigo != _[content_key]:
                _[content_key] = novo_codigo
                if Diretorio:
                    with open(Diretorio, "w", encoding="utf-8") as f:
                        f.write(novo_codigo)
                # st.toast("💾 Salvo!") # Opcional

        ab.append(Aba_Atual)
        ab.append(Diretorio)

    # -------------------------------------------------------------------- PAINEL LATERAL (MANTIDO)
    with ColunaRun:
        _.setdefault("aba_executando_id", None)
        _.setdefault("aba_executando", None)
        _.setdefault("thread_running", False)

        col_btn_apag, col_sel, col_btn_run, col_btn_stop = st.columns([1, 4, 1.3, 1.3])

        with col_btn_apag:
            if Button_Nao_Fecha('🖕', ":material/delete:", key="botao_apagar_arquivos"):
                with st.container(border=True, key='Braço_Sidebar', width=900):
                    Apagar_Arq(st, Aba_Atual, Diretorio)

        with col_sel:
            aba_escolhida = st.selectbox(
                "Arquivo para Rodar",
                nomes_abas,
                index=IDES,
                key="select_run_unico",
                label_visibility="collapsed",
            )

        with col_btn_run:
            executar = st.button(':material/directions_bike:', shortcut="Ctrl+Enter", key="btn_run_unico")

        with col_btn_stop:
            parar = st.button(':material/stop:', shortcut="Ctrl+Space", key="btn_stop_unico")

        if executar:
            idx_exec = nomes_abas.index(aba_escolhida)
            dir_exec = Caminho[idx_exec]
            ck_exec = f"conteudo_arquivo_{dir_exec}"

            if _.get("thread_running"):
                _.thread_running = False
                if "output_queue" in _:
                    _.output_queue.put("PROGRAM_FINISHED")

            # Garante conteúdo atualizado para execução
            if ck_exec not in _:
                if os.path.isfile(dir_exec):
                    _[ck_exec] = Abrir_Arquivo_Select_Tabs(st, dir_exec)

            _.codigo_para_executar = _.get(ck_exec, "")
            _.aba_executando = aba_escolhida
            _.aba_executando_id = idx_exec
            _.nova_execucao_solicitada = True

            st.toast(f"⬆️ ID {_.aba_executando_id} - Aba {_.aba_executando} enviada pro terminal!")
            st.rerun()

        if parar:
            if _.get("thread_running"):
                _.thread_running = False
                if "output_queue" in _:
                    _.output_queue.put("PROGRAM_FINISHED")
                st.toast("🛑 Execução interrompida!")
            else:
                st.toast("ℹ️ Nenhuma execução em andamento")
            st.rerun()

    return ab[0], ab[1]





def Editor_Simples_radio(Coluna, ColunaRun, Caminho, THEMA_EDITOR, EDITOR_TAM_MENU,p):
    _ = st.session_state
    ab = []

    # -------------------------------------------------------------------- LEITURA DAS ABAS
    nomes_abas = [arquivo for arquivo in chec_se_arq_do_projeto(Caminho)]

    # MUDANÇA: Em vez de tabs nativas que renderizam tudo e bugam o st_ace,
    # usamos um seletor para renderizar APENAS UM editor por vez (o que funciona bem).
    with Coluna:
        # Simulando abas com radio horizontal ou pills (se disponível na versão)
        # Usando radio horizontal como fallback robusto
        aba_selecionada = st.radio(
            "Arquivos abertos:",
            options=nomes_abas,
            horizontal=True,
            label_visibility="collapsed",
            key="navegacao_abas_editor"
        )

    # Identifica o índice da aba selecionada
    if aba_selecionada in nomes_abas:
        IDES = nomes_abas.index(aba_selecionada)
    else:
        IDES = 0  # Fallback

    # Lógica para renderizar SOMENTE O EDITOR ATIVO (Fora de loop de tabs!)
    _.tab_atual = IDES
    Diretorio = Caminho[IDES]
    Aba_Atual = os.path.basename(Diretorio)
    linguagem = Identificar_linguagem(Diretorio)

    content_key = f"conteudo_arquivo_{IDES}"

    # Inicializa conteúdo se não existir
    if content_key not in _:
        _[content_key] = (
            Abrir_Arquivo_Select_Tabs(st, Diretorio)
            if os.path.isfile(Diretorio)
            else ""
        )

    with Coluna:
        # Renderiza o editor único - isso garante estabilidade do tema
        code = st_ace(
            value=_[content_key],
            language=linguagem,
            theme=THEMA_EDITOR,  # Tema fixo como solicitado
            font_size=EDITOR_TAM_MENU,
            height=850,
            auto_update=True,
            wrap=True,
            annotations = Anotations_Editor(_[content_key]),
            markers  = Marcadores_Editor(_[content_key]),
            show_print_margin=True
            # Key única baseada no diretório para garantir que o Streamlit não reutilize o estado errado
        )

        # Atualiza sessão
        _[content_key] = code

        # Salva no disco
        if Diretorio:
            with open(Diretorio, "w", encoding="utf-8") as f:
                f.write(code)

        ab.append(Aba_Atual)
        ab.append(Diretorio)

    # -------------------------------------------------------------------- RUN ÚNICO
    # (Mantive a lógica original do usuário aqui, apenas ajustando indentação se necessário)
    with ColunaRun:
        _.setdefault("aba_executando_id", None)
        _.setdefault("aba_executando", None)
        _.setdefault("thread_running", False)

        col_btn_apag, col_sel, col_btn_run, col_btn_stop = st.columns([1, 4, 1.3, 1.3])

        with col_btn_apag:
            if Button_Nao_Fecha('🖕', ":material/delete:", key="botao_apagar_arquivos"):
                with st.container(border=True, key='Braço_Sidebar', width=900):
                    Apagar_Arq(st, Aba_Atual, Diretorio)

        with col_sel:
            # Sincroniza o selectbox com a aba atual para UX melhor
            aba_escolhida = st.selectbox(
                "Arquivo",
                nomes_abas,
                index=IDES if IDES < len(nomes_abas) else 0,
                key="select_run_unico",
                label_visibility="collapsed",
            )

        with col_btn_run:
            executar = st.button(':material/directions_bike:', shortcut="Ctrl+Enter", key="btn_run_unico")

        with col_btn_stop:
            parar = st.button(':material/stop:', shortcut="Ctrl+Space", key="btn_stop_unico")

        if executar:
            # Lógica de execução mantida...
            idx_exec = nomes_abas.index(aba_escolhida)
            dir_exec = Caminho[idx_exec]
            ck_exec = f"conteudo_arquivo_{idx_exec}"

            if _.get("thread_running"):
                _.thread_running = False
                if "output_queue" in _:
                    _.output_queue.put("PROGRAM_FINISHED")

            _.codigo_para_executar = _.get(ck_exec, "")
            _.aba_executando = aba_escolhida
            _.aba_executando_id = idx_exec
            _.nova_execucao_solicitada = True

            st.toast(f"⬆️ ID {_.aba_executando_id} - Aba {_.aba_executando} enviada pro terminal!")
            st.rerun()

        if parar:
            if _.get("thread_running"):
                _.thread_running = False
                if "output_queue" in _:
                    _.output_queue.put("PROGRAM_FINISHED")
                st.toast("🛑 Execução interrompida!")
            else:
                st.toast("ℹ️ Nenhuma execução em andamento")
            st.rerun()

    return ab[0], ab[1]



#----------ANTIGA
def Editor_Simples___(Coluna,Run, Caminho, THEMA_EDITOR, EDITOR_TAM_MENU):
    ab= []
    # --------------------------------------------------------------------LEITURA DA TABS  ABAS
    nomes_abas = [arquivo for arquivo in chec_se_arq_do_projeto(Caminho)]
    tabs = Coluna.tabs(nomes_abas)

    for IDES, tab in enumerate(tabs):
        with tab:
            # ✅ QUANDO ENTRA NA ABA, MARCA ELA COMO ATIVA!
            st.session_state.tab_atual = IDES

            Diretorio = Caminho[IDES]
            Aba_Atual = os.path.basename(Diretorio)
            linguagem= Identificar_linguagem(Diretorio)

            """Editor burro - só ace + botão"""

            _ = st.session_state

            # Carrega arquivo
            content_key = f'conteudo_arquivo_{IDES}'
            if content_key not in _:
                _.content_key = Abrir_Arquivo_Select_Tabs(st, Diretorio) if os.path.isfile(Diretorio) else ""

            code = st_ace(
                value=_[content_key],
                language=linguagem,
                theme=THEMA_EDITOR,
                font_size=EDITOR_TAM_MENU,
                height=450,
                auto_update=True,
                wrap=True,
                key=f"editor_{IDES}"
            )
            # ✅ QUANDO CLICAR EXECUTAR → MANDA PRO TERMINAL
            if "aba_executando_id" not in st.session_state:
                st.session_state.aba_executando_id = None

            if "aba_executando" not in st.session_state:
                st.session_state.aba_executando = None

            if Run:
                _.codigo_para_executar = code
                _.aba_executando = Aba_Atual
                _.aba_executando_id = IDES
                st.success(f"⬆️ ID {_.aba_executando_id } - Aba {_.aba_executando } enviada pro terminal!")

            # Salva arquivo automaticamente
            if Diretorio:
                with open(Diretorio, "w", encoding="utf-8") as f:
                    f.write(code)
            ab.append(Aba_Atual)
            ab.append(Diretorio)
    return ab[0], ab[1]
def Terminal_Completo___(Coluna,THEMA_PREVIEW, PREVIEW_TAM_MENU):
    """Terminal inteligente - toda a mágica aqui"""
    _ = st.session_state

    # ✅ LÊ A ABA EXECUTADA PELO ID (NÃO pelo nome genérico)
    if 'aba_executando_id' in _ and _.aba_executando_id is not None:
        aba_id = _.aba_executando_id
        aba_nome = _.get('nomes_abas', ['?'])[aba_id] if 'nomes_abas' in _ else f"Aba {aba_id}"
        st.success(f"🚀 Aba ID:{aba_id} - {aba_nome} recebida do editor!")
        st.success(f"⬆️ Aba {_.aba_executando} recebida do editor!\n ️ ID {_.aba_executando_id} recebida do editor!")


    # Inicialização (igual seu código original)
    defaults = {
        'code_committed': "",
        'output': "",
        'input_queue': queue.Queue(),
        'output_queue': queue.Queue(),
        'thread_running': False,
    }
    for key, value in defaults.items():
        if key not in _:
            _[key] = value

    class CustomStdout:
        def __init__(self, output_q): self.output_q = output_q

        def write(self, s):
            if s and s.strip(): self.output_q.put(s.rstrip('\n'))

        def flush(self): pass

    def run_code_thread(code, input_q, output_q):
        def custom_input(prompt=""):
            if prompt: output_q.put(prompt)
            return input_q.get()

        stdout_redirect = CustomStdout(output_q)
        old_stdout = sys.stdout
        sys.stdout = stdout_redirect

        try:
            exec(code, {'input': custom_input, '__name__': '__main__'})
            output_q.put("\n✓ Programa finalizado com sucesso!")
        except Exception as e:
            output_q.put(f"\n❌ Erro: {str(e)}")
        finally:
            sys.stdout = old_stdout
            output_q.put("PROGRAM_FINISHED")

    # ✅ EXECUTA quando recebe código da aba
    if 'codigo_para_executar' in _ and _.codigo_para_executar and not _.thread_running:
        _.code_committed = _.codigo_para_executar
        _.output = f"🚀 Executando código da Aba {_.get('aba_executando', '?')}...\n"
        _.input_queue = queue.Queue()
        _.output_queue = queue.Queue()
        _.thread_running = True

        thread = threading.Thread(
            target=run_code_thread,
            args=(_.code_committed, _.input_queue, _.output_queue),
            daemon=True
        )
        thread.start()

    # Processa output da thread
    try:
        while True:
            msg = _.output_queue.get_nowait()
            if msg == "PROGRAM_FINISHED":
                _.thread_running = False
                break
            _.output += msg + '\n'
    except queue.Empty:
        pass
    with Coluna:
        preview = st_ace(
            value=_.output,
            language="text",
            height=450,
            font_size=PREVIEW_TAM_MENU,
            theme=THEMA_PREVIEW,
            auto_update=True,
            show_gutter=False,
            show_print_margin=False,
            wrap=True,
            key=_.output,
            placeholder="Clique EXECUTAR em qualquer aba para ver o resultado aqui!"
        )

    # Input handling
    if _.output and _.thread_running:
        if len(preview) > len(_.output):
            delta = preview[len(_.output):]
            if delta.endswith("\n"):
                clean_input = delta.rstrip("\n").strip()
                if clean_input:
                    _.input_queue.put(clean_input)
                    _.output = preview
                    st.rerun()

    # ✅ RESETA se não tem código ou aba válida
    if ('codigo_para_executar' not in _ or
            not _.codigo_para_executar or
            'aba_executando_id' not in _):
        _.output = ""
        st.info("Pronto para receber código de qualquer aba!")
        return

