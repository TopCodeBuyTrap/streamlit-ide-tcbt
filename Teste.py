import json

import streamlit as st
import os
import queue
import sys
import threading

from code_editor import code_editor
from streamlit_ace import st_ace

from APP_SUB_Funcitons import Button_Nao_Fecha
from APP_SUB_Janela_Explorer import Abrir_Arquivo_Select_Tabs

option_map = {
    0: ":material/add:",
    1: ":material/zoom_in:",
    2: ":material/zoom_out:",
    3: ":material/zoom_out_map:",
    4: ":material/remove:",
    5: ":material/edit:",
    6: ":material/delete:",
    7: ":material/save:",
    9: ":material/refresh:",
    10: ":material/settings:",
    11: ":material/home:",
    12: ":material/arrow_back:",
    13: ":material/arrow_forward:",
    14: ":material/center_focus_strong:",
    15: ":material/fullscreen:",
    16: ":material/fullscreen_exit:",
    17: ":material/visibility:",
    18: ":material/visibility_off:",
    19: ":material/info:",
    20: ":material/bug_report:",
    22: ":material/code_off:",
    23: ":material/data_object:",
    24: ":material/terminal:",
    25: ":material/terminal_output:",
    26: ":material/terminal_help:",
    27: ":material/adb:",
    28: ":material/blur_linear:",
    29: ":material/build:",
    30: ":material/calculate:",
    31: ":material/camera_roll:",
    32: ":material/clean_hands:",
    33: ":material/cleaning_services:",
    34: ":material/commit:",
    35: ":material/dashboard_customize:",
    36: ":material/data_array:",
    37: ":material/data_saver_on:",
    38: ":material/discover_tune:",
    40: ":material/file_copy:",
    41: ":material/file_open:",
    42: ":material/filter_alt:",
    43: ":material/find_in_page:",
    44: ":material/format_bold:",
    45: ":material/format_indent_increase:",
    46: ":material/format_list_numbered:",
    47: ":material/forward_to_inbox:",
    48: ":material/grid_view:",

    50: ":material/integration_instructions:",
    51: ":material/language:",
    52: ":material/loop:",
    53: ":material/memory:",
    54: ":material/monitor_heart:",
    55: ":material/moving:",
    56: ":material/open_in_browser:",
    57: ":material/open_in_new:",
    58: ":material/pending_actions:",
    59: ":material/play_circle:",
    60: ":material/print:",
    61: ":material/qr_code:",
    62: ":material/queue_play_next:",
    63: ":material/remove_red_eye:",
    64: ":material/report_problem:",
    65: ":material/rocket_launch:",
    66: ":material/save_alt:",
    67: ":material/security:",
    68: ":material/shopping_bag:",
    69: ":material/sim_card_download:",
    70: ":material/source:",
    71: ":material/stacked_line_chart:",
    72: ":material/start:",
    73: ":material/stop_circle:",
    74: ":material/sync_alt:",
    75: ":material/tag:",
    76: ":material/task_alt:",
    77: ":material/tune:",
    78: ":material/play_arrow:",
    79: ":material/pause:",
    80: ":material/stop:",
    81: ":material/skip_next:",
    82: ":material/skip_previous:",
    83: ":material/fast_forward:",
    84: ":material/fast_rewind:",
    85: ":material/replay:",
    86: ":material/replay_10:",
    87: ":material/replay_30:",
    88: ":material/forward_10:",
    89: ":material/forward_30:",
    90: ":material/shuffle:",
    91: ":material/repeat:",
    92: ":material/repeat_one:",
    93: ":material/volume_up:",
    94: ":material/volume_down:",
    95: ":material/volume_off:",
    96: ":material/mic:",
    97: ":material/mic_off:",
    98: ":material/headset:",
    99: ":material/headset_mic:",
    100: ":material/surround_sound:",
    101: ":material/speaker:",
    102: ":material/speaker_group:",
    103: ":material/music_note:",
    104: ":material/library_music:",
    105: ":material/library_add:",
    106: ":material/library_books:",
    107: ":material/library_add_check:",
    108: ":material/camera:",
    109: ":material/photo:",
    110: ":material/portrait:",
    111: ":material/landscape:",
    112: ":material/photo_camera:",
    113: ":material/videocam:",
    114: ":material/videocam_off:",
    115: ":material/image:",

    117: ":material/image_search:",
    118: ":material/file_upload:",
    119: ":material/file_download:",

    124: ":material/content_copy:",
    125: ":material/content_cut:",
    126: ":material/content_paste:",
    127: ":material/select_all:",
    128: ":material/text_format:",
    129: ":material/format_italic:",
    130: ":material/format_underlined:",
    131: ":material/format_strikethrough:",
    132: ":material/format_align_left:",
    133: ":material/format_align_center:",
    134: ":material/format_align_right:",
    135: ":material/format_align_justify:",
    136: ":material/format_list_bulleted:",
    137: ":material/format_indent_decrease:",
    138: ":material/format_quote:",
    139: ":material/insert_emoticon:",
    140: ":material/insert_link:",
    141: ":material/insert_photo:",
    142: ":material/emoji_emotions:",
    143: ":material/emoji_events:",
    144: ":material/emoji_flags:",
    145: ":material/emoji_food_beverage:",
    146: ":material/emoji_nature:",
    147: ":material/emoji_objects:",
    148: ":material/emoji_people:",
    149: ":material/emoji_symbols:",
    150: ":material/emoji_transportation:",
    151: ":material/thumb_up:",
    152: ":material/thumb_down:",
    153: ":material/thumbs_up_down:",
    154: ":material/star_rate:",
    155: ":material/star_border:",
    156: ":material/star_half:",
    157: ":material/favorite:",
    158: ":material/favorite_border:",
    161: ":material/trending_up:",
    162: ":material/trending_down:",
    165: ":material/notifications_active:",
    166: ":material/notifications_none:",
    167: ":material/notifications_off:",
    168: ":material/calendar_today:",
    169: ":material/calendar_view_month:",
    170: ":material/event:",
    171: ":material/alarm:",
    172: ":material/query_builder:",
    173: ":material/access_time:",
    174: ":material/watch_later:",
    175: ":material/timer:",
    176: ":material/timer_off:",
    177: ":material/flight:",
    178: ":material/flight_takeoff:",
    179: ":material/flight_land:",
    180: ":material/directions_car:",


    182: ":material/directions_bus:",
    183: ":material/directions_railway:",
    184: ":material/train:",
    185: ":material/directions_walk:",
    186: ":material/place:",
    187: ":material/maps_ugc:",
    188: ":material/navigation:",
    189: ":material/near_me:",
    190: ":material/location_on:",
    191: ":material/location_off:",
    192: ":material/room:",
    193: ":material/storefront:",
    194: ":material/shopping_cart:",
    195: ":material/add_shopping_cart:",
    196: ":material/credit_card:",
    197: ":material/payments:",
    198: ":material/account_circle:",
    199: ":material/people:",
    200: ":material/group_add:",
    201: ":material/person_add:",
    202: ":material/person_remove:",
    203: ":material/person_outline:",
    204: ":material/lock:",
    205: ":material/lock_open:",
    206: ":material/verified_user:",
    207: ":material/public:",
    208: ":material/g_translate:",
    209: ":material/lightbulb:"
}

selection = st.pills("Tool", options=option_map.keys(),
                       format_func=lambda option: option_map[option],
                       selection_mode="single", label_visibility='collapsed', )
if selection:
    st.write(selection, option_map[selection])


st.title("Exemplo real de uso")



mode_list = ["abap", "abc", "actionscript", "ada", "alda", "apache_conf", "apex", "applescript", "aql", "asciidoc",
             "asl", "assembly_x86", "autohotkey", "batchfile", "bibtex", "c9search", "c_cpp", "cirru", "clojure",
             "cobol", "coffee", "coldfusion", "crystal", "csharp", "csound_document", "csound_orchestra",
             "csound_score", "csp", "css", "curly", "d", "dart", "diff", "django", "dockerfile", "dot",
             "drools", "edifact", "eiffel", "ejs", "elixir", "elm", "erlang", "forth", "fortran", "fsharp",
             "fsl", "ftl", "gcode", "gherkin", "gitignore", "glsl", "gobstones", "golang", "graphqlschema",
             "groovy", "haml", "handlebars", "haskell", "haskell_cabal", "haxe", "hjson", "html", "html_elixir",
             "html_ruby", "ini", "io", "ion", "jack", "jade", "java", "javascript", "jexl", "json", "json5",
             "jsoniq", "jsp", "jssm", "jsx", "julia", "kotlin", "latex", "latte", "less", "liquid", "lisp",
             "livescript", "logiql", "logtalk", "lsl", "lua", "luapage", "lucene", "makefile", "markdown",
             "mask", "matlab", "maze", "mediawiki", "mel", "mips", "mixal", "mushcode", "mysql", "nginx",
             "nim", "nix", "nsis", "nunjucks", "objectivec", "ocaml", "partiql", "pascal", "perl", "pgsql",
             "php", "php_laravel_blade", "pig", "plain_text", "powershell", "praat", "prisma", "prolog",
             "properties", "protobuf", "puppet", "python", "qml", "r", "raku", "razor", "rdoc", "red",
             "redshift", "rhtml", "robot", "rst", "ruby", "rust", "sac", "sass", "scad", "scala", "scheme",
             "scrypt", "scss", "sh", "sjs", "slim", "smarty", "smithy", "snippets", "soy_template", "space",
             "sparql", "sql", "sqlserver", "stylus", "svg", "swift", "tcl", "terraform", "tex", "text", "textile",
             "toml", "tsx", "turtle", "twig", "typescript", "vala", "vbscript", "velocity", "verilog", "vhdl",
             "visualforce", "wollok", "xml", "xquery", "yaml", "zeek"]

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

height = [19, 22]
language = "python"
theme = "default"
shortcuts = "vscode"
focus = False
wrap = True
btns = 'custom_buttons_alt'


st.write("")
with st.expander("Settings", expanded=True):
    col_a, col_b, col_c, col_cb = st.columns([6, 11, 3, 3])
    col_c.markdown('<div style="height: 2.5rem;"><br/></div>', unsafe_allow_html=True)
    col_cb.markdown('<div style="height: 2.5rem;"><br/></div>', unsafe_allow_html=True)

    height_type = col_a.selectbox("height format:", ["css", "max lines", "min-max lines"], index=2)
    if height_type == "css":
        height = col_b.text_input("height (CSS):", "400px")
    elif height_type == "max lines":
        height = col_b.slider("max lines:", 1, 40, 22)
    elif height_type == "min-max lines":
        height = col_b.slider("min-max lines:", 1, 40, (19, 22))

    col_d, col_e, col_f = st.columns([1, 1, 1])
    language = col_d.selectbox("lang:", mode_list, index=mode_list.index("python"))
    theme = col_e.selectbox("theme:", ["default", "light", "dark", "contrast"])
    shortcuts = col_f.selectbox("shortcuts:", ["emacs", "vim", "vscode", "sublime"], index=2)
    focus = col_c.checkbox("focus", False)
    wrap = col_cb.checkbox("wrap", True)

with st.expander("Components"):
    c_buttons = st.checkbox("custom buttons (JSON)", False)
    if c_buttons:
        response_dict_btns = code_editor(json.dumps(custom_buttons_alt, indent=2), lang="json", height=8,
                                         buttons=btn_settings_editor_btns)

        if response_dict_btns['type'] == "submit" and len(response_dict_btns['text']) != 0:
            btns = json.loads(response_dict_btns['text'])
    else:
        btns = []

    i_bar = st.checkbox("info bar (JSON)", False)
    if i_bar:
        response_dict_info = code_editor(json.dumps(info_bar, indent=2), lang="json", height=8,
                                         buttons=btn_settings_editor_btns)

        if response_dict_info['type'] == "submit" and len(response_dict_info['text']) != 0:
            info_bar = json.loads(response_dict_info['text'])
    else:
        info_bar = {}

st.write("### Output:")
# construct props dictionary (->Ace Editor)
ace_props = {"style": {"borderRadius": "0px 0px 8px 8px"}}

input = st.text_area("Input:", 'demo_sample_python_code', height=200)
response_dict = code_editor(input, height=height, lang=language, theme=theme, shortcuts=shortcuts, completions=[
    {"caption": "AAA", "value": "BBB", "meta": "CCC", "name": "DDD", "score": 400}], focus=focus, buttons=btns,
                            info=info_bar, props=ace_props, options={"wrap": wrap}, allow_reset=True,
                            response_mode=["debounce", "blur"], key="code_editor_demo")

st.write(response_dict)

if response_dict['type'] == "submit" and len(response_dict['text']) != 0:
    st.write("Response type: ", response_dict['type'])
    st.code(response_dict['text'], language=response_dict['lang'])
st.write("### Code Editor:")
st.code(input, language=language)
# st.write("You can find more examples in the [docs]()")

new_response = code_editor("print('Hello World!')", lang="python", height=22, buttons=btn_settings_editor_btns,
                           options={"wrap": wrap}, allow_reset=True, key="code_editor3",
                           ghost_text="Type your code here...", response_mode="debounce")
st.write(new_response)

# SEUS ARQUIVOS JÁ CRIADOS: codigo_1.py, codigo_2.py, codigo_3.py

def Editor_Simples(Run, Diretorio, linguagem, THEMA_EDITOR, EDITOR_TAM_MENU, IDES):
    """Editor burro - só ace + botão"""
    ESTADO_ = st.session_state

    # Carrega arquivo
    content_key = f'conteudo_arquivo_{IDES}'
    if content_key not in ESTADO_:
        ESTADO_[content_key] = Abrir_Arquivo_Select_Tabs(st, Diretorio) if os.path.isfile(Diretorio) else ""

    code = st_ace(
        value=ESTADO_[content_key],
        language=linguagem,
        theme=THEMA_EDITOR,
        font_size=EDITOR_TAM_MENU,
        height=450,
        auto_update=True,
        wrap=True,
        key=f"editor_{IDES}"
    )

    # ✅ QUANDO CLICAR EXECUTAR → MANDA PRO TERMINAL
    if Run:
        ESTADO_.codigo_para_executar = code
        ESTADO_.aba_executando = IDES
        st.success(f"🚀 Aba {IDES} enviada pro terminal!")

    # Salva arquivo automaticamente
    if Diretorio:
        with open(Diretorio, "w", encoding="utf-8") as f:
            f.write(code)


def Terminal_Completo(THEMA_PREVIEW, PREVIEW_TAM_MENU):
    """Terminal inteligente - toda a mágica aqui"""
    ESTADO_ = st.session_state

    # Inicialização (igual seu código original)
    defaults = {
        'code_committed': "",
        'output': "",
        'input_queue': queue.Queue(),
        'output_queue': queue.Queue(),
        'thread_running': False,
    }
    for key, value in defaults.items():
        if key not in ESTADO_:
            ESTADO_[key] = value

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
    if 'codigo_para_executar' in ESTADO_ and ESTADO_.codigo_para_executar and not ESTADO_.thread_running:
        ESTADO_.code_committed = ESTADO_.codigo_para_executar
        ESTADO_.output = f"🚀 Executando código da Aba {ESTADO_.get('aba_executando', '?')}...\n"
        ESTADO_.input_queue = queue.Queue()
        ESTADO_.output_queue = queue.Queue()
        ESTADO_.thread_running = True

        thread = threading.Thread(
            target=run_code_thread,
            args=(ESTADO_.code_committed, ESTADO_.input_queue, ESTADO_.output_queue),
            daemon=True
        )
        thread.start()


    # Processa output da thread
    try:
        while True:
            msg = ESTADO_.output_queue.get_nowait()
            if msg == "PROGRAM_FINISHED":
                ESTADO_.thread_running = False
                break
            ESTADO_.output += msg + '\n'
    except queue.Empty:
        pass

    preview = st_ace(
        value=ESTADO_.output,
        language="text",
        height=450,
        font_size=PREVIEW_TAM_MENU,
        theme=THEMA_PREVIEW,
        auto_update=True,
        show_gutter=False,
        show_print_margin=False,
        wrap=True,
        key=ESTADO_.output,
        placeholder="Clique EXECUTAR em qualquer aba para ver o resultado aqui!"
    )

    # Input handling
    if ESTADO_.output and ESTADO_.thread_running:
        if len(preview) > len(ESTADO_.output):
            delta = preview[len(ESTADO_.output):]
            if delta.endswith("\n"):
                clean_input = delta.rstrip("\n").strip()
                if clean_input:
                    ESTADO_.input_queue.put(clean_input)
                    ESTADO_.output = preview
                    st.rerun()


if __name__ == "__main__":
    st.set_page_config(layout="wide")
    st.title("🖥️ IDE Multi-Aba")

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("👨‍💻 Editores")

        abas = ["Aba 1", "Aba 2", "Aba 3"]
        arquivos = ["./codigo_1.py", "./codigo_2.py", "./codigo_3.py"]

        tabs = st.tabs(abas)

        for i, tab in enumerate(tabs):
            with tab:
                Run = st.button(f"▶ EXECUTAR {abas[i]}", key=f"run_{i}")
                Editor_Simples(
                    Run=Run,
                    Diretorio=arquivos[i],
                    linguagem="python",
                    THEMA_EDITOR="merbivore",
                    EDITOR_TAM_MENU=15,
                    IDES=i + 1
                )

    with col2:
        st.subheader("📱 Terminal Único")
        Terminal_Completo(
            THEMA_PREVIEW="terminal",
            PREVIEW_TAM_MENU=13
        )



def Editor_Previews_(Rodar_Codigo, Diretorio, linguagem,THEMA_EDITOR,EDITOR_TAM_MENU,THEMA_PREVIEW,PREVIEW_TAM_MENU,IDES):
    st.success(f"📁 {Diretorio}")
    COL1, COL2 = st.columns(2)
    ESTADO_ = st.session_state


    suffix = f"_{IDES}"
    ESTADO_ = st.session_state

    # -------------------------------------------------------------------------
    # 1. INICIALIZAÇÃO DO ARQUIVO (Carrega conteúdo se necessário)
    # -------------------------------------------------------------------------
    current_file_key = f'arquivo_atual{suffix}'
    content_key = f'conteudo_arquivo{suffix}'


    # ✅ INICIALIZAÇÃO MELHORADA
    if current_file_key not in ESTADO_:
        ESTADO_.arquivo_atual = Diretorio
        ESTADO_.conteudo_arquivo = content_key
        if Diretorio and os.path.isfile(Diretorio):
            ESTADO_.conteudo_arquivo = Abrir_Arquivo_Select_Tabs(st, Diretorio)

    # 🚨 SÓ recarrega se ARQUIVO MUDOU (não no primeiro run)
    if Diretorio != ESTADO_.arquivo_atual and Diretorio and os.path.isfile(Diretorio):
        ESTADO_.arquivo_atual = Diretorio
        ESTADO_.conteudo_arquivo = Abrir_Arquivo_Select_Tabs(st, Diretorio)

    # ✅ SESSION STATE PERSISTENTE
    defaults = {
        'code_buffer': ESTADO_.conteudo_arquivo,  # ← O QUE VOCÊ DIGITA
        'code_committed': ESTADO_.conteudo_arquivo,  # ← O QUE VAI EXECUTAR
        'output': "",
        'input_queue': queue.Queue(),
        'output_queue': queue.Queue(),
        'thread_running': False,
    }
    for key, value in defaults.items():
        if key not in ESTADO_:
            ESTADO_[key] = value

    class CustomStdout:
        def __init__(self, output_q): self.output_q = output_q

        def write(self, s):
            if s and s.strip(): self.output_q.put(s.rstrip('\n'))

        def flush(self): pass

    def run_code_thread(code, input_q, output_q):
        def safe_log(msg):
            print(f"LOG: {msg}")

        safe_log("Thread iniciada")

        def custom_input(prompt=""):
            if prompt: output_q.put(prompt)
            return input_q.get()

        stdout_redirect = CustomStdout(output_q)
        old_stdout = sys.stdout
        sys.stdout = stdout_redirect

        try:
            exec(code, {'input': custom_input, '__name__': '__main__'})
            output_q.put("\n✓ Programa finalizado com sucesso")
        except Exception as e:
            output_q.put(f"\n❌ Erro: {str(e)}")
        finally:
            sys.stdout = old_stdout
            output_q.put("PROGRAM_FINISHED")

    with COL1:
        st.subheader("📝 Editor")
        # ✅ EDITOR SEMPRE USA BUFFER (não apaga o que você digitou!)
        code = st_ace(
            value=ESTADO_.code_buffer,
            language=linguagem,
            theme= THEMA_EDITOR,
            font_size=EDITOR_TAM_MENU,
            height=450,
            auto_update=True,
            wrap=True,
            key=f"editor_{IDES}"
        )

        # ✅ ATUALIZA BUFFER em tempo real
        if not ESTADO_.thread_running:
            ESTADO_.code_buffer = code

        # ✅ EXECUTA SÓ QUANDO CLICAR
        if Rodar_Codigo and not ESTADO_.thread_running:
            ESTADO_.code_committed = ESTADO_.code_buffer
            ESTADO_.output = ""
            ESTADO_.input_queue = queue.Queue()
            ESTADO_.output_queue = queue.Queue()
            ESTADO_.thread_running = True

            thread = threading.Thread(
                target=run_code_thread,
                args=(ESTADO_.code_committed, ESTADO_.input_queue, ESTADO_.output_queue),
                daemon=True
            )
            thread.start()

    with COL2:
        st.subheader(F"📤 Terminal {ESTADO_.output}")

        # Processa output
        try:
            while True:
                msg = ESTADO_.output_queue.get_nowait()
                if msg == "PROGRAM_FINISHED":
                    ESTADO_.thread_running = False
                    break
                ESTADO_.output += '\n' + msg
        except queue.Empty:
            pass

        preview = st_ace(
            value=ESTADO_.output,
            language="text",
            height=450,
            font_size=PREVIEW_TAM_MENU,
            theme=THEMA_PREVIEW,
            auto_update=True,
            show_gutter=False,
            show_print_margin=False,
            wrap=True,

            key=f"preview_{ESTADO_.output}",
            placeholder= Diretorio
        )

        # Input automático
        if ESTADO_.output:
            if ESTADO_.thread_running and len(preview) > len(ESTADO_.output):
                delta = preview[len(ESTADO_.output):]
                if delta.endswith("\n"):
                    clean_input = delta.rstrip("\n").strip()
                    if clean_input:
                        ESTADO_.input_queue.put(clean_input)
                        ESTADO_.output = preview
                        st.rerun()
        else:
            st.warning(ESTADO_.output)

    if Diretorio and ESTADO_.code_buffer != ESTADO_.code_committed:
        with open(Diretorio, "w", encoding="utf-8") as f:
            f.write(ESTADO_.code_buffer)
        ESTADO_.code_committed = ESTADO_.code_buffer


''' 
# Exemplo de uso
if __name__ == "__main__":
    col1 = st.columns(1)[0]
    Run = False
    if st.button("▶️ EXECUTAR", use_container_width=True):
        Run = True
    Editor_Previews(Run, "./meu_codigo.py", 'python', 'merbivore', 15,
                    'terminal', 13, 0)
'''
