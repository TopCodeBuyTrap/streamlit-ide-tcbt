

import os


# Pega a pasta Downloads do usuário
default_download = os.path.join(os.path.expanduser("~"), "Downloads")

# Lista de fontes para campos (inputs, selects, botões) - fontes de programação
FONTES_TEXTO = ["Helvetica", "Arial", "Verdana", "Tahoma", "Times New Roman", "Georgia", "Comic Sans MS",
                "Fira Code", "JetBrains Mono", "Source Code Pro", "Source Sans Pro", "Pixelify Sans", "Silkscreen",
                "Share Tech Mono", "Inconsolata", "Consolas", "Courier New", "Monospace"]
# Temas Ace Editor - SEPARADOS CORRETAMENTE por claro e escuro
TEMAS_CLAROS = [
    "chrome",  # Claro padrão/neutro
    "crimson_editor",  # Claro (você confirmou)
    #"dawn",             # Claro suave/bege
    "dreamweaver",  # Claro (você confirmou)
    "eclipse",  # Claro clássico
    "github",  # Claro GitHub
    "iplastic",  # Claro (você confirmou)
    #"katzenmilch",      # Claro creme (você confirmou)
    #"kuroir",           # Claro (você confirmou)
    "solarized_light",  # Solarized claro oficial
    "sqlserver",  # Claro SQL Server (você confirmou)
    #"textmate",         # Claro TextMate

    "xcode"  # Claro Xcode
]

LANGUAGES = [
    "powershell", "abap", "apex", "css", "kotlin", "less", "markdown", "python"]

TEMAS_ESCUROS = [
    "ambiance",  # Escuro clássico
    "chaos",  # Escuro vibrante
    #"clouds_midnight",      # Escuro (você confirmou)
    "cobalt",  # Escuro azul
    "dracula",  # Escuro roxo popular
    "gob",  # Escuro gob
    #"gruvbox",              # Escuro Gruvbox
    "idle_fingers",  # Escuro Idle Fingers
    #"kr_theme",             # Escuro KR
    "merbivore",  # Escuro Merbivore
    "merbivore_soft",  # Escuro suave
    "mono_industrial",  # Escuro industrial
    "monokai",  # Escuro Monokai clássico
    #"nord_dark",            # Escuro Nord
    "pastel_on_dark",  # Escuro (você confirmou)
    "solarized_dark",  # Solarized escuro oficial
    "terminal",  # Escuro terminal
    "tomorrow_night",  # Tomorrow Night escuro
    #"tomorrow_night_blue",  # Tomorrow azul escuro
    "tomorrow_night_bright",  # Tomorrow bright escuro
    #"tomorrow_night_eighties", # Tomorrow 80s escuro
    "twilight",  # Escuro Twilight
    "vibrant_ink",  # Claro vibrante (você confirmou)
]

TEMAS_MONACO = ["vs-dark", "vs-light", "hc-black", "hc-light", "Sistema"]


def Customization(st):
	from Banco_dados import (
		ler_CUSTOMIZATION,
		ler_CUSTOMIZATION_coluna_por_usuario,
		ATUAL_CUSTOM_agora
	)


	# ---------------- USUÁRIOS EXISTENTES
	usuarios_raw = ler_CUSTOMIZATION()

	st1, st2 = st.columns([1, 9])
	usuarios = [row[0] for row in usuarios_raw if row[0] != "Padrão"]  # Remove Padrão
	usuarios =  usuarios  # Coloca Padrão primeiro mas NÃO mostra

	# Começa com "Padrão" selecionado (index=0)
	usuario = st1.selectbox("👤 Usuário:", usuarios, index=0, key='usuario_select')

	# Remove o st.stop() - deixa continuar sempre
	st1.success(f"✏️ Editando: **{usuario}**")

	# Resto do código continua normalmente...

	# ---------------- LEITURA CONFIGURAÇÕES DO USUÁRIO
	TAM_EDITOR = int(ler_CUSTOMIZATION_coluna_por_usuario(usuario, 'EDITOR_TAM_MENU') or 14)
	TAM_TERM = int(ler_CUSTOMIZATION_coluna_por_usuario(usuario, 'TERMINAL_TAM_MENU') or 14)
	TAM_PREV = int(ler_CUSTOMIZATION_coluna_por_usuario(usuario, 'PREVIEW_TAM_MENU') or 14)
	RADIO = int(ler_CUSTOMIZATION_coluna_por_usuario(usuario, 'RADIAL') or 10)
	BORDA = int(ler_CUSTOMIZATION_coluna_por_usuario(usuario, 'BORDA') or 1)

	THEMA_EDITOR = ler_CUSTOMIZATION_coluna_por_usuario(usuario, 'THEMA_EDITOR') or 'dracula'
	THEMA_PREVIEW = ler_CUSTOMIZATION_coluna_por_usuario(usuario, 'THEMA_PREVIEW') or 'chaos'
	THEMA_TERMINAL = ler_CUSTOMIZATION_coluna_por_usuario(usuario, 'THEMA_TERMINAL') or 'terminal'

	FONTE_MENU = ler_CUSTOMIZATION_coluna_por_usuario(usuario, 'FONTE_MENU') or 'JetBrains Mono'
	FONTE_TAM_MENU = int(ler_CUSTOMIZATION_coluna_por_usuario(usuario, 'FONTE_TAM_MENU') or 13)
	FONTE_COR_MENU = ler_CUSTOMIZATION_coluna_por_usuario(usuario, 'FONTE_COR_MENU') or '#0022ff'

	FONTE_CAMPO = ler_CUSTOMIZATION_coluna_por_usuario(usuario, 'FONTE_CAMPO') or 'Fira Code'
	FONTE_TAM_CAMPO = int(ler_CUSTOMIZATION_coluna_por_usuario(usuario, 'FONTE_TAM_CAMPO') or 13)
	FONTE_COR_CAMPO = ler_CUSTOMIZATION_coluna_por_usuario(usuario, 'FONTE_COR_CAMPO') or '#A86E04'

	THEMA_APP1 = ler_CUSTOMIZATION_coluna_por_usuario(usuario, 'THEMA_APP1') or '#04061a'
	THEMA_APP2 = ler_CUSTOMIZATION_coluna_por_usuario(usuario, 'THEMA_APP2') or '#24283b'

	# ---------------- ABAS ORGANIZADAS
	tab1, tab2, tab3, tab4 = st2.tabs(["📏 Tamanhos de Fontes e Bordas", "✏️ Fontes Menus / Campos", "🎨 Temas dos Editores", "🎨 Temas da TcbT IDE"])

	# ---------------- TAB 1: LAYOUT
	with tab1:
		c1, c2, c3, c4, c5 = st.columns(5)
		Tam_Font = c1.number_input("Editor", 5, 40, TAM_EDITOR, key=f'tam_editor_{usuario}')
		Tam_Run = c2.number_input("Preview", 5, 40, TAM_PREV, key=f'tam_preview_{usuario}')
		Tam_Term = c3.number_input("Terminal", 5, 40, TAM_TERM, key=f'tam_term_{usuario}')
		Radio = c4.number_input("Raio", 0, 80, RADIO, key=f'radial_{usuario}')
		Borda = c5.number_input("Borda", 0, 2, BORDA, key=f'borda_{usuario}')

	# ---------------- TAB 2: FONTES
	with tab2:
		col1, col2 = st.columns(2)
		with col1:
			fm1, fm2, fm3 = st.columns(3)
			Fonte_Menu = fm1.selectbox("Fonte", FONTES_TEXTO,
			                           index=FONTES_TEXTO.index(FONTE_MENU) if FONTE_MENU in FONTES_TEXTO else 0,
			                           key=f'fonte_menu_{usuario}')
			Fonte_Tam_Menu = fm2.number_input("Tamanho", 6, 40, FONTE_TAM_MENU, key=f'tam_menu_{usuario}')
			Fonte_Cor_Menu = fm3.color_picker("Cor", FONTE_COR_MENU, key=f'cor_menu_{usuario}')

		with col2:
			fc1, fc2, fc3 = st.columns(3)
			Fonte_Campo = fc1.selectbox("Fonte", FONTES_TEXTO,
			                            index=FONTES_TEXTO.index(FONTE_CAMPO) if FONTE_CAMPO in FONTES_TEXTO else 0,
			                            key=f'fonte_campo_{usuario}')
			Fonte_Tam_Campo = fc2.number_input("Tamanho", 6, 40, FONTE_TAM_CAMPO, key=f'tam_campo_{usuario}')
			Fonte_Cor_Campo = fc3.color_picker("Cor", FONTE_COR_CAMPO, key=f'cor_campo_{usuario}')

	# ---------------- TAB 3: TEMAS ACE
	with tab3:
		col1, col2 = st.columns(2)
		with col1:
			modo_editor = col1.selectbox("Modo", ["Claro", "Escuro"], key=f'modo_ed_{usuario}')
			temas_editor = TEMAS_CLAROS if modo_editor == "Claro" else TEMAS_ESCUROS

			Tema_Editor = st.selectbox("Editor de Código", temas_editor,
		                           index=temas_editor.index(THEMA_EDITOR) if THEMA_EDITOR in temas_editor else 0,key=f'tema_editor_{usuario}')
		with col2:

			Tema_Preview = st.selectbox("Preview Run", TEMAS_ESCUROS,
			                              index=TEMAS_ESCUROS.index(
				                              THEMA_PREVIEW) if THEMA_PREVIEW in TEMAS_ESCUROS else 0,
			                              key=f'tema_preview_{usuario}')
			Tema_Terminal = st.selectbox("Terminal CMD", TEMAS_ESCUROS,
			                               index=TEMAS_ESCUROS.index(
				                               THEMA_TERMINAL) if THEMA_TERMINAL in TEMAS_ESCUROS else 0,
			                               key=f'tema_terminal_{usuario}')

	# ---------------- TAB 4: CORES APP
	with tab4:
		col_app1, col_app2 = st.columns(2)
		THEMA_APP1 = col_app1.color_picker("Sidebar / Foot", THEMA_APP1, key=f'app1_{usuario}')
		THEMA_APP2 = col_app2.color_picker("Corpo", THEMA_APP2, key=f'app2_{usuario}')

	# ---------------- BOTÃO APLICAR (final das tabs)
	col_btn1, col_btn2 = st.columns([3, 1])
	with col_btn1:
		if st.button("💾 SALVAR TUDO", type="primary", use_container_width=True):
			# Layout
			ATUAL_CUSTOM_agora(st, usuario, 'EDITOR_TAM_MENU', Tam_Font)
			ATUAL_CUSTOM_agora(st, usuario, 'PREVIEW_TAM_MENU', Tam_Run)
			ATUAL_CUSTOM_agora(st, usuario, 'TERMINAL_TAM_MENU', Tam_Term)
			ATUAL_CUSTOM_agora(st, usuario, 'RADIAL', Radio)
			ATUAL_CUSTOM_agora(st, usuario, 'BORDA', Borda)

			# Fontes Menu
			ATUAL_CUSTOM_agora(st, usuario, 'FONTE_MENU', Fonte_Menu)
			ATUAL_CUSTOM_agora(st, usuario, 'FONTE_TAM_MENU', Fonte_Tam_Menu)
			ATUAL_CUSTOM_agora(st, usuario, 'FONTE_COR_MENU', Fonte_Cor_Menu)

			# Fontes Campo
			ATUAL_CUSTOM_agora(st, usuario, 'FONTE_CAMPO', Fonte_Campo)
			ATUAL_CUSTOM_agora(st, usuario, 'FONTE_TAM_CAMPO', Fonte_Tam_Campo)
			ATUAL_CUSTOM_agora(st, usuario, 'FONTE_COR_CAMPO', Fonte_Cor_Campo)

			# Temas
			ATUAL_CUSTOM_agora(st, usuario, 'THEMA_EDITOR', Tema_Editor)
			ATUAL_CUSTOM_agora(st, usuario, 'THEMA_PREVIEW', Tema_Preview)
			ATUAL_CUSTOM_agora(st, usuario, 'THEMA_TERMINAL', Tema_Terminal)
			ATUAL_CUSTOM_agora(st, usuario, 'THEMA_APP1', THEMA_APP1)
			ATUAL_CUSTOM_agora(st, usuario, 'THEMA_APP2', THEMA_APP2)

			st.success("✅ **TODAS** configs salvas!")
			st.balloons()
			st.rerun()

	with col_btn2:
		if st.button("🔄 Recarregar", type="secondary"):
			st.rerun()


