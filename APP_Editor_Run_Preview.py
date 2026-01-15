import time
from pathlib import Path

import streamlit as st
from streamlit_ace import st_ace
import sys
import threading
import queue
import os
import re

from APP_Chats_IA import gerar_codigo, CODOLLAMA_CHAT
from APP_SUB_Funcitons import Anotations_Editor, Marcadores_Editor, wrap_text
from Banco_dados import ler_CUSTOMIZATION_coluna
from SUB_Controle_Driretorios import _DIRETORIO_PROJETO_ATUAL_


# Funções auxiliares (Certifique-se que estão acessíveis ou no mesmo arquivo)
def smart_paste_format(code):
    if not code: return code
    lines = code.split('\n')
    formatted = [line.rstrip().replace('\t', '    ') for line in lines]
    result = '\n'.join(formatted)
    return re.sub(r'\n{3,}', '\n\n', result)

def Editor_Previews(RUN_, Arq_Selec, linguagem, height_mode, containers_order, layout, col_weights, cont):
    arquivo_id = "__default__"

    # ============================================================= ALTURAS
    HEIGHTS = {
        "pequeno": 300,
        "medio": 500,
        "grande": 800,
        "extra": 1200
    }
    BASE_HEIGHT = HEIGHTS[height_mode]

    # ============================================================= COMPONENTES
    def render_container(name, height, key):
        """
        Versão otimizada para rodar dentro de TABS ou FOR RANGE.
        Usa Arq_Selec como chave única para isolar os estados.
        """
        # 🔧 TRATAMENTO ESPECIAL PARA TERMINAL - NÃO USA LOOP DE ARQUIVOS
        if name == "ChatOllama":
            with st.container(border=True):

                key_prefix = f"state_{Arq_Selec}"
                state = st.session_state.get(key_prefix)

                if state is None:
                    st.warning("Editor ainda não inicializado")
                    return

                # Estado interno do Chat (isolado)
                chat_key = f"chat_{Arq_Selec}"
                if chat_key not in st.session_state:
                    st.session_state[chat_key] = {
                        "resultado": ""
                    }

                chat_state = st.session_state[chat_key]


                prompt_extra = st.text_area(
                    "Instrução adicional (opcional)",
                    placeholder="Ex: Otimize, explique, refatore...",
                    height=70
                )

                col1, col2, col3 = st.columns(3)

                with col1:
                    criar = st.button("Criar", use_container_width=True)

                with col2:
                    ajustar = st.button("Ajustar", use_container_width=True)

                with col3:
                    explicar = st.button("Explicar", use_container_width=True)

                # ---------------- AÇÕES ----------------
                if criar or ajustar or explicar:

                    codigo_base = state["code"]

                    if criar:
                        acao = "Crie código novo"
                        prompt = prompt_extra or "Crie um código Python"

                    elif ajustar:
                        acao = "Refatore e melhore este código"
                        prompt = codigo_base

                    elif explicar:
                        acao = "Explique este código com comentários"
                        prompt = codigo_base

                    try:
                        resultado = CODOLLAMA_CHAT(prompt, acao)
                        chat_state["resultado"] = resultado
                    except Exception as e:
                        chat_state["resultado"] = f"# Erro ao gerar código\n# {str(e)}"

                resp = str(wrap_text(chat_state["resultado"], width=80))
                st.code(resp, language="python")

            return


        # 1. ISOLAMENTO DE ESTADO POR ARQUIVO (SÓ PARA Editor/Preview)
        key_prefix = f"state_{Arq_Selec}"

        if key_prefix not in st.session_state:
            # Tenta carregar o conteúdo inicial se não existir no estado
            initial_code = ""
            if os.path.exists(Arq_Selec):
                with open(Arq_Selec, "r", encoding="utf-8") as f:
                    initial_code = f.read()

            st.session_state[key_prefix] = {
                'output': "",
                'input_queue': queue.Queue(),
                'output_queue': queue.Queue(),
                'thread_running': False,
                'code': initial_code,
                'last_save': time.time()
            }

        state = st.session_state[key_prefix]

        # Garante que a chave existe caso o estado tenha sido criado por uma versão anterior sem ela
        if 'last_save' not in state:
            state['last_save'] = time.time()

        # Classes para capturar a saída (Stdout)
        class CustomStdout:
            def __init__(self, output_q):
                self.output_q = output_q

            def write(self, s):
                if s: self.output_q.put(s)

            def flush(self):
                pass

        # Função que roda o código em background (mantida igual)
        def run_code_thread(code, input_q, output_q):
            def custom_input(prompt=""):
                if prompt:
                    output_q.put(prompt)
                return input_q.get()

            stdout_redirect = CustomStdout(output_q)
            old_stdout = sys.stdout
            sys.stdout = stdout_redirect

            try:
                # 1️⃣ Descobre pasta do projeto atual
                Pasta_RAIZ_projeto = _DIRETORIO_PROJETO_ATUAL_()
                Pasta_RAIZ_projeto = Path(Pasta_RAIZ_projeto)

                # 2️⃣ Caminho do python da venv do projeto
                venv_python = Pasta_RAIZ_projeto / ".virtual_tcbt" / "Scripts" / "python.exe"

                # 3️⃣ Define globals que o exec vai usar
                exec_globals = {
                    'input': custom_input,
                    'print': print,
                    '__name__': '__main__',
                    '__file__': str(Pasta_RAIZ_projeto / "main.py"),
                }

                # 4️⃣ Executa com globals corretos
                exec(code, exec_globals)
                output_q.put("\n✓ Programa finalizado")

            except Exception as e:
                output_q.put(f"\n❌ Erro: {str(e)}")
            finally:
                sys.stdout = old_stdout
                output_q.put("PROGRAM_FINISHED")

        # --------------------------------------------------------------------- EDITOR
        if name == "Editor":
            THEMA_EDITOR = ler_CUSTOMIZATION_coluna('THEMA_EDITOR')
            EDITOR_TAM_MENU = ler_CUSTOMIZATION_coluna('EDITOR_TAM_MENU')
            Editor_Codigo = st_ace(
                value=state['code'],
                theme=THEMA_EDITOR,
                language=linguagem,
                height=height,
                font_size=EDITOR_TAM_MENU,
                auto_update=False,
                wrap=True,
                annotations=Anotations_Editor(state['code']),
                markers=Marcadores_Editor(state['code']),
                key=f"editor_{Arq_Selec}_{arquivo_id}",
            )

            # Lógica de Smart Paste
            if Editor_Codigo != state['code']:
                if abs(len(Editor_Codigo) - len(state['code'])) > 10:
                    state['code'] = smart_paste_format(Editor_Codigo)
                    st.rerun()
                else:
                    state['code'] = Editor_Codigo

            # Botão de Execução
            if RUN_ == True:
                if not state['thread_running']:
                    state['output'] = ""
                    state['thread_running'] = True
                    state['input_queue'] = queue.Queue()
                    state['output_queue'] = queue.Queue()

                    thread = threading.Thread(
                        target=run_code_thread,
                        args=(state['code'], state['input_queue'], state['output_queue'])
                    )
                    thread.daemon = True
                    thread.start()
                    st.rerun()

        # --------------------------------------------------------------------- PREVIEW
        elif name == "Preview":
            # PROCESSAMENTO DE OUTPUT
            new_data = False
            try:
                while True:
                    msg = state['output_queue'].get_nowait()
                    if msg == "PROGRAM_FINISHED":
                        state['thread_running'] = False
                        break
                    state['output'] += msg
                    new_data = True
            except queue.Empty:
                pass

            # TERMINAL ACE (SAÍDA/ENTRADA)
            THEMA_PREVIEW = ler_CUSTOMIZATION_coluna('THEMA_PREVIEW')
            PREVIEW_TAM_MENU = ler_CUSTOMIZATION_coluna('PREVIEW_TAM_MENU')
            Terminal_Input = st_ace(
                value=state['output'],
                font_size=PREVIEW_TAM_MENU,
                theme=THEMA_PREVIEW,
                language=linguagem,
                height=height,
                auto_update=False,
                show_gutter=False,
                placeholder="Saída do console...",
                wrap=True,
                key=f"terminal_{Arq_Selec}_{len(state['output'])}",
            )

            # Lógica de Input pelo Terminal
            if state['thread_running'] and len(Terminal_Input) > len(state['output']):
                delta = Terminal_Input[len(state['output']):]
                if delta.strip():
                    state['input_queue'].put(delta.strip())
                    state['output'] += delta
                    st.rerun()

            # SALVAMENTO AUTOMÁTICO
            if time.time() - state['last_save'] > 2:
                try:
                    with open(Arq_Selec, "w", encoding="utf-8") as f:
                        f.write(state['code'])
                    state['last_save'] = time.time()
                except:
                    pass

            # Manter UI atualizada
            if state['thread_running'] or new_data:
                time.sleep(0.1)
                st.rerun()

    # ============================================================= RENDERIZAÇÃO (Layouts - Terminal participa aqui!)
    if not containers_order:
        st.info("Nenhum painel selecionado")
    else:
        n = len(containers_order)

        if layout == 1:
            cols = st.columns(col_weights if col_weights else n)
            for col, name in zip(cols, containers_order):
                with col:
                    render_container(name, BASE_HEIGHT, f"{name}_l1")

        elif layout == 2:
            if n == 1:
                render_container(containers_order[0], BASE_HEIGHT * 2, "single_l2")
            else:
                left, right = st.columns(col_weights)
                with left:
                    render_container(containers_order[0], BASE_HEIGHT * 2 + 180, "left_l2")
                with right:
                    for name in containers_order[1:]:
                        render_container(name, BASE_HEIGHT, f"{name}_right_l2")

        elif layout == 3:
            if n == 1:
                render_container(containers_order[0], BASE_HEIGHT * 2, "single_l3")
            else:
                top = st.columns(col_weights)
                for col, name in zip(top, containers_order[:2]):
                    with col:
                        render_container(name, BASE_HEIGHT, f"{name}_top_l3")
                for name in containers_order[2:]:
                    render_container(name, int(BASE_HEIGHT * 1.5), f"{name}_bottom_l3")

        elif layout == 4:
            for name in containers_order:
                render_container(name, BASE_HEIGHT, f"{name}_vertical")
