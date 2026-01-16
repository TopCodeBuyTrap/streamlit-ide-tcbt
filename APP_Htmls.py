from APP_SUB_Controle_Driretorios import _DIRETORIO_EXECUTAVEL_, _DIRETORIO_PROJETOS_
from Banco_dados import ler_CUSTOMIZATION_coluna
import base64
import streamlit as st
import os


def Main_App(st):
	# ✅ CORREÇÃO 1: Chama funções ANTES de usar variáveis
	Pasta_Isntal_exec = _DIRETORIO_EXECUTAVEL_()
	Pasta_RAIZ_projeto = _DIRETORIO_PROJETOS_()

	# --------------------------------------------------------------------- CARREGAMENTO DE CUSTOMIZAÇÃO
	NOME_CUSTOM = ler_CUSTOMIZATION_coluna('NOME_CUSTOM')
	NOME_USUARIO = ler_CUSTOMIZATION_coluna('NOME_USUARIO')
	CAMINHO_DOWNLOAD = ler_CUSTOMIZATION_coluna('CAMINHO_DOWNLOAD')
	IMAGEM_LOGO = ler_CUSTOMIZATION_coluna('IMAGEM_LOGO')

	EDITOR_TAM_MENU = ler_CUSTOMIZATION_coluna('EDITOR_TAM_MENU')
	THEMA_APP1 = ler_CUSTOMIZATION_coluna('THEMA_APP1')
	THEMA_APP2 = ler_CUSTOMIZATION_coluna('THEMA_APP2')
	FONTE_MENU = ler_CUSTOMIZATION_coluna('FONTE_MENU')
	TAM_MENU = ler_CUSTOMIZATION_coluna('FONTE_TAM_MENU')
	COR_MENU = ler_CUSTOMIZATION_coluna('FONTE_COR_MENU')
	FONTE_CAMPO = ler_CUSTOMIZATION_coluna('FONTE_CAMPO')
	TAM_CAMPO = ler_CUSTOMIZATION_coluna('FONTE_TAM_CAMPO')
	COR_CAMPO = ler_CUSTOMIZATION_coluna('FONTE_COR_CAMPO')
	THEMA_PREVIEW = ler_CUSTOMIZATION_coluna('THEMA_PREVIEW')
	PREVIEW_TAM_MENU = ler_CUSTOMIZATION_coluna('PREVIEW_TAM_MENU')

	RADIO = ler_CUSTOMIZATION_coluna('RADIAL')
	BORDA = ler_CUSTOMIZATION_coluna('BORDA')
	DECORA = ler_CUSTOMIZATION_coluna('DECORA')
	OPC1 = ler_CUSTOMIZATION_coluna('OPC1')
	OPC2 = ler_CUSTOMIZATION_coluna('OPC2')
	OPC3 = ler_CUSTOMIZATION_coluna('OPC3')
	OBS = ler_CUSTOMIZATION_coluna('OBS')

	SIDEBAR_COR = THEMA_APP1

	# ✅ FUNÇÕES AUXILIARES (antes do CSS)
	def img_to_base64(img_path):
		try:
			with open(img_path, 'rb') as f:
				return base64.b64encode(f.read()).decode()
		except:
			return ""  # Fallback se imagem não existir

	def hex_to_rgba(hex_color, alpha=0.25):
		try:
			hex_color = hex_color.lstrip("#")
			r = int(hex_color[0:2], 16)
			g = int(hex_color[2:4], 16)
			b = int(hex_color[4:6], 16)
			return f"rgba({r}, {g}, {b}, {alpha})"
		except:
			return "rgba(0,0,0,0.25)"

	LOGO_BASE64 = img_to_base64(IMAGEM_LOGO)

	# ✅ CSS CORRIGIDO (sintaxe válida)
	page_bg = f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Fira+Code:wght@400;700&display=swap');
    @import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:ital,wght@0,400;0,700;1,400;1,700&display=swap');
    @import url('https://fonts.googleapis.com/css2?family=Source+Code+Pro:ital,wght@0,400;1,400&display=swap');
    @import url('https://fonts.googleapis.com/css2?family=Press+Start+2P&display=swap');
    @import url('https://fonts.googleapis.com/css2?family=Pixelify+Sans:wght@400;700&display=swap');
    @import url('https://fonts.googleapis.com/css2?family=Silkscreen:wght@400;700&display=swap');
    @import url('https://fonts.googleapis.com/css2?family=Share+Tech+Mono&display=swap');




    /* GRUPO B — FONTE_CAMPO */
    [data-testid="stTextInput"] p,
    [data-testid="stSidebar"] p,
    [data-testid="stColorPicker"] p {{
        font-family: '{FONTE_CAMPO}' !important;
        font-size: {TAM_CAMPO}px !important;
    }}

    
    div[data-testid="stButton"] button {{                               /* Botões */
        background-color: {THEMA_APP1} !important;
        color: {COR_CAMPO} !important;
        font-size: {TAM_MENU}px !important;
        height: 30px !important;
        padding: 4px 8px !important;
        line-height: 20px !important;
        min-height: 24px !important;
        border-radius: {RADIO}px !important;
    }}

    /* Radio e Slider */
    [data-testid="stRadio"] p,
    [data-testid="stSlider"] p {{
        color: {COR_MENU} !important;
        font-family: '{FONTE_MENU}' !important;
        font-size: {TAM_MENU}px !important;
    }}

    /* NumberInput e Selectbox */
    [data-testid="stNumberInput"] div,
    [data-testid="stSelectbox"] div {{
        color: {COR_MENU} !important;
        font-family: '{FONTE_MENU}' !important;
        font-size: {TAM_MENU}px !important;
    }}
    [data-testid="stSelectbox"] div > div {{
        color: {COR_CAMPO} !important;
        font-family: '{FONTE_CAMPO}' !important;
        font-size: {TAM_CAMPO}px !important;
    }}
    [data-testid="stTextInput"] p {{
        color: {COR_MENU} !important;
        font-family: '{FONTE_MENU}' !important;
        font-size: {TAM_MENU}px !important;
    }}

    /* Expander */
    [data-testid="stExpander"] {{
        color: {COR_MENU} !important;
        border-radius: {RADIO}px !important;
        border: {BORDA}px solid {COR_CAMPO} !important;
    }}

    
    header.stAppHeader {{                                       /* HEADER */
        padding-left: 0% !important;
        margin-top: -10px !important;
        left:auto !important;
        width: 15% !important;
         /* BACKGROUND TRANSPARENTE */
    background: transparent !important;
    background-color: transparent !important;
    
    /* Borda transparente também */
    border: none !important;
    box-shadow: none !important;
    }}

    /* BLOCO PRINCIPAL */
    .block-container {{
        background-color: {THEMA_APP2} !important;
        margin-top: -99px !important;
        margin-left: 0px !important;
        padding-left: 3% !important;
        margin-right: 0px !important;
        width: 105% !important;
        max-width: none !important;
    }}

   
    section[data-testid="stSidebar"] {{                              /* SIDEBAR */
        background-color: {SIDEBAR_COR} !important;
        padding-top: -50px !important;
        margin-left: 0 !important;
        height: 95% !important;
    }}

    div[data-testid="stVerticalBlock"][class*="st-key-Bra-o_Sidebar"] {{ /* MENU LATERAL DIREITO - AO LADO DO SIDEBAR */
        background-color: {SIDEBAR_COR} !important;
	    position: absolute !important;
	    top: 5% !important;  /* Alinha no topo do sidebar */
		left: 10% !important;
	    border-radius: {RADIO}px !important;
	    border: {BORDA}px solid {COR_CAMPO} !important;
	    z-index: 999999 !important;
	    width: 600px; /* Largura fixa do seu bloco */
	    transition: transform .001s ease !important; /* Animação suave */
	}}



	/* Container principal para posicionamento correto */
	section[data-testid="stAppViewContainer"] {{
	    position: relative !important;
	}}

    
    [data-testid="stExpandSidebarButton"] {{                                   
        background-color: {COR_MENU} !important;
        margin-top: 0% !important;
        position: fixed !important;
        left: 3px !important;
        width: 60px !important;
        height: 10px !important;
        
        z-index: 9999 !important;
    }}

    /* CONTAINERS   stElementContainer 
    div[data-testid="stLayoutWrapper"]{{
        background-color: {THEMA_APP1} !important;
         border-radius: {RADIO}px !important;
        border: {BORDA}px solid {COR_CAMPO} !important; 

    }}  */
	
	    
    [data-testid="stBaseButton-pills"] {{                               /* ST.PILLS BOTAO */
        background-color: {THEMA_APP1} !important;
        border: {BORDA}px solid {COR_CAMPO} !important; 

    }}
      [data-testid="stBaseButton-secondary"]:has(kbd[aria-label="Shortcut Ctrl + Enter"]){{/* BOTAO RUN */
        margin-top: -10% !important;
        background-color: {COR_CAMPO} !important;
        color: {COR_MENU} !important;
        position: fixed !important;
        width: 10% !important;
        right: 45% !important;
        z-index: 9999 !important;
        
         /* ✅ SCROLL HABILITADO */
	    overflow: visible !important;  /* Permite conteúdo maior */
	    max-height: none !important;   /* Remove limitação de altura */
	    height: auto !important;       /* Altura dinâmica */
	    
	    
    }}
    
    [data-testid="stCustomComponentV1"] {{                                      /* EDITORES DE CODIGOS */
        background-color: {THEMA_APP1} !important;
         border-radius: {RADIO}px !important;
        
        border: {BORDA}px solid {COR_CAMPO} !important; 

    }}


	    div[data-testid="stButton"][class*="st-key-nome_da_sua_key"] {{             /* CONTAINERS */
        background-color: {THEMA_APP1} !important;
        padding: 0 !important;
        height: 5% !important;

    }}

	[data-testid="stElementContainer"][class*="st-key-rolandia12 st-emotion-cache-zh2fnc e12zf7d51"] {{  /* nao  ta usando */
		border-radius: {RADIO+8}px !important;
		border: {BORDA}px solid {COR_CAMPO} !important;
		
		
    }}
    


    div[data-testid="stColumn"][class*="stColumn st-emotion-cache-de7oey e12zf7d52"] {{          /*  TERMINAL  */
        background-color: {THEMA_APP2} !important;
        position: fixed !important;
        bottom: 4.7% !important;
        padding-left: 20% !important;
        right: 0% !important;
        z-index: 9999 !important;
        display: flex !important;
        justify-content: space-between !important;
        padding: 0px !important;
        width: 89.5% !important;
        
    }}

    /* CHECKBOX */
    [data-testid="stCheckbox"] div {{
        color:  !important;
        text-decoration: underline !important;
        background: {SIDEBAR_COR} !important;
        
        padding: 1px !important;
    }}

    /* FOOTER */
    .footer {{
        position: fixed !important;
        bottom: 0 !important;
        left: 0 !important;
        right: 0 !important;
        height: 50px !important;
        background: {SIDEBAR_COR} !important;
        z-index: 99999999 !important;
        display: flex !important;
        align-items: center !important;
        justify-content: space-between !important;
        padding: 20px !important;
        color: white !important;
    }}
    </style>


    """

	st.markdown(page_bg, unsafe_allow_html=True)

	def criar_estilos_botao():  # ainda noa usei
		"""Estilos CSS personalizados"""
		return f"""
		
		    <div class="footer">
        <div style="display:flex; align-items:center; gap:16px; font-family:Arial, sans-serif;">
            <span style="font-weight:600;">📚 {NOME_CUSTOM}</span>
            <span style="opacity:0.5;"> | </span>
            <span>🪪 {NOME_USUARIO}</span>{Pasta_Isntal_exec}
        </div>
    </div>
    
    
	    <style>
	    @import url('https://fonts.googleapis.com/css2?family=Fira+Code:wght@400;700&family=JetBrains+Mono:wght@400;700&display=swap');

	    .main-title {{ font-family: 'Fira Code', monospace; font-size: 3rem; 
	        background: linear-gradient(45deg, #00d4ff, #ff6b6b, #4ecdc4);
	        -webkit-background-clip: text; -webkit-text-fill-color: transparent; 
	        text-align: center; margin-bottom: 2rem; font-weight: 700; }}

	    .stButton > button {{ background: linear-gradient(45deg, #667eea 0%, #764ba2 100%);
	        border: none; color: white; font-family: 'JetBrains Mono', monospace;
	        font-weight: 600; border-radius: 12px; padding: 12px 24px; 
	        transition: all 0.3s ease; box-shadow: 0 4px 15px rgba(102, 126, 234, 0.4); }}

	    .stButton > button:hover {{ transform: translateY(-2px); 
	        box-shadow: 0 8px 25px rgba(102, 126, 234, 0.6); }}

	    .config-section, .sobre-section {{ background: rgba(15, 15, 25, 0.95); padding: 2rem;
	        border-radius: 20px; border: 1px solid rgba(255, 255, 255, 0.1); 
	        backdrop-filter: blur(10px); margin-bottom: 1rem; }}

	    .path-section {{ background: linear-gradient(135deg, rgba(0, 170, 255, 0.1), rgba(0, 255, 127, 0.1));
	        border-left: 5px solid #00aaff; padding: 1.5rem; margin: 1rem 0; border-radius: 10px; }}
	    </style>
	    """

	return IMAGEM_LOGO, NOME_CUSTOM, COR_CAMPO, COR_MENU

# ✅ IMPORTS NO TOPO (CORRIGIDO)
