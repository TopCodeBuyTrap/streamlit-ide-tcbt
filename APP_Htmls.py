from APP_SUB_Controle_Driretorios import _DIRETORIO_EXECUTAVEL_, _DIRETORIO_PROJETOS_, _DIRETORIO_PROJETO_ATUAL_
from APP_SUB_Funcitons import saudacao_por_hora_sistema
from Banco_dados import ler_CUSTOMIZATION_coluna, ler_B_ARQUIVOS_RECENTES
import base64
import streamlit as st
import os


def Carregamento_BancoDados_Temas(st):
	# ✅ CORREÇÃO 1: Chama funções ANTES de usar variáveis
	Pasta_Isntal_exec = _DIRETORIO_EXECUTAVEL_()
	Pasta_RAIZ_projeto = _DIRETORIO_PROJETOS_()
	Pasta_Projeto_Atual = _DIRETORIO_PROJETO_ATUAL_()
	Estrutura_projeto = ler_B_ARQUIVOS_RECENTES()[0][1]
	# --------------------------------------------------------------------- CARREGAMENTO DE CUSTOMIZAÇÃO
	NOME_CUSTOM = ler_CUSTOMIZATION_coluna('NOME_CUSTOM')
	NOME_USUARIO = ler_CUSTOMIZATION_coluna('NOME_USUARIO')
	CAMINHO_DOWNLOAD = ler_CUSTOMIZATION_coluna('CAMINHO_DOWNLOAD')
	IMAGEM_LOGO = ler_CUSTOMIZATION_coluna('IMAGEM_LOGO')

	THEMA_EDITOR = ler_CUSTOMIZATION_coluna('THEMA_EDITOR')
	EDITOR_TAM_MENU = ler_CUSTOMIZATION_coluna('EDITOR_TAM_MENU')

	THEMA_PREVIEW = ler_CUSTOMIZATION_coluna('THEMA_PREVIEW')
	PREVIEW_TAM_MENU = ler_CUSTOMIZATION_coluna('PREVIEW_TAM_MENU')

	TERMINAL_TAM_MENU = ler_CUSTOMIZATION_coluna('TERMINAL_TAM_MENU')
	THEMA_TERMINAL = ler_CUSTOMIZATION_coluna('THEMA_TERMINAL')

	THEMA_APP1 = ler_CUSTOMIZATION_coluna('THEMA_APP1')
	THEMA_APP2 = ler_CUSTOMIZATION_coluna('THEMA_APP2')
	FONTE_MENU = ler_CUSTOMIZATION_coluna('FONTE_MENU')
	TAM_MENU = ler_CUSTOMIZATION_coluna('FONTE_TAM_MENU')
	COR_MENU = ler_CUSTOMIZATION_coluna('FONTE_COR_MENU')
	FONTE_CAMPO = ler_CUSTOMIZATION_coluna('FONTE_CAMPO')
	TAM_CAMPO = ler_CUSTOMIZATION_coluna('FONTE_TAM_CAMPO')
	COR_CAMPO = ler_CUSTOMIZATION_coluna('FONTE_COR_CAMPO')


	RADIO = ler_CUSTOMIZATION_coluna('RADIAL')
	BORDA = ler_CUSTOMIZATION_coluna('BORDA')
	DECORA = ler_CUSTOMIZATION_coluna('DECORA')
	OPC1 = ler_CUSTOMIZATION_coluna('OPC1')
	OPC2 = ler_CUSTOMIZATION_coluna('OPC2')
	OPC3 = ler_CUSTOMIZATION_coluna('OPC3') # COLOQUEI AQUI IMAGEM CONFIG
	OBS = ler_CUSTOMIZATION_coluna('OBS')

	# ✅ FUNÇÕES AUXILIARES (antes do CSS)
	def img_to_base64(img_path):
		try:
			with open(img_path, 'rb') as f:
				return base64.b64encode(f.read()).decode()
		except:
			return ""  # Fallback se imagem não existir
	def hex_to_rgba_inverso(hex_color: str, intensidade):
		try:
			intensidade = float(intensidade) / 100  # 0–1
		except:
			intensidade = 0.3

		# INVERTE A OPACIDADE
		alpha = 1.0 - intensidade
		alpha = max(0.0, min(alpha, 1.0))

		hex_color = hex_color.lstrip("#")
		r = int(hex_color[0:2], 16)
		g = int(hex_color[2:4], 16)
		b = int(hex_color[4:6], 16)

		return f"rgba({r},{g},{b},{alpha})"
	LOGO_BASE64 = img_to_base64(IMAGEM_LOGO)

	# cor base + opacidade vinda do OPC3
	try:
		COR_OVERLAY = hex_to_rgba_inverso(THEMA_APP2, float(OPC3))

		if OPC3 != "":
			BG_STYLE = f'''
		    background:
		        linear-gradient({COR_OVERLAY}, {COR_OVERLAY}),
		        url("data:image/png;base64,{LOGO_BASE64}") !important;
		        background-repeat: no-repeat !important;
			    background-position: center center !important;
			    background-size: cover !important;
		    '''
		else:
			BG_STYLE = f'''
		    background-color: {THEMA_APP2} !important;
		    '''
	except ValueError :
		BG_STYLE = f'''
				    background-color: {THEMA_APP2} !important;
				    '''

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


	/* CONTEÚDO CENTRAL */
	section[data-testid="stMain6"] {{ /* REMOVER SCROLL */
	    overflow: hidden !important;
	}}


    /* GRUPO B — FONTE_CAMPO */
    [data-testid="stTextInput"] p,
    [data-testid="stSidebar"] p,
    [data-testid="stColorPicker"] p {{
        font-family: '{FONTE_CAMPO}' !important;
        font-size: {TAM_CAMPO}px !important;
    }}

    
    div[data-testid="stButton"] button {{                               /* Botões */
        background-color: {THEMA_APP1} !important;
        color: {COR_MENU} !important;
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

    
    header.stAppHeader {{                                               /* HEADER */
        padding-left: 0% !important;
        margin-top: 15px !important;
        left:auto !important;
        width: 15% !important;
         /* BACKGROUND TRANSPARENTE */
	    background: transparent !important;
	    background-color: transparent !important;
	    
	    /* Borda transparente também */
	    border: none !important;
	    box-shadow: none !important;
    }}

    
    .block-container {{                                             /* BLOCO PRINCIPAL BODY*/
        margin-top: -7% !important;
        margin-left: 0px !important;
        padding-left: 3% !important;
        margin-right: 0px !important;
        width: 105% !important;
        max-width: none !important;
        {BG_STYLE}
    

    }}
	
   
    section[data-testid="stSidebar"] {{                              /* SIDEBAR */
        background-color: {THEMA_APP1} !important;
        margin-left: 0 !important;
        height: 110% !important;
        margin-top: 3% !important;
        
        
        
    }}

    [data-testid="stSidebarCollapseButton"] {{                                  /* BOTÃO DO SIDEBAR DE CIMA >> */
	    position: fixed !important;
	    background-color: {COR_CAMPO} !important;
        border-radius: {RADIO}px !important;
        border: {BORDA}px  !important;
		}}

    [data-testid="stExpandSidebarButton"] {{                                /* BOTÃO DO SIDEBAR DE BAIXO << */            
        position: fixed !important;
        top: 4% !important;
        left: 3px !important;
        width: 60px !important;
        height: 11px !important;
        opacity: 1 !important;
        z-index: 9999 !important;
    }}

    div[data-testid="stVerticalBlock"][class*="st-key-Bra-o_Sidebar"] {{ /* MENU de botao POUPAP - AO LADO DO SIDEBAR */
        background-color: {THEMA_APP1} !important;
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

    /* CONTAINERS   stElementContainer 
    div[data-testid="stLayoutWrapper"]{{
        background-color: {THEMA_APP1} !important;
         border-radius: {RADIO}px !important;
        border: {BORDA}px solid {COR_CAMPO} !important; 

    }}  */
	
	    
    [data-testid="stBaseButton-pills"] {{                               /* ST.PILLS BOTAO */
        background-color: transparent !important;
        border: 0px solid {COR_CAMPO} !important; 
        margin-bottom: -8% !important;
        
	}}
	
	[data-testid="stBaseButton-pillsActive"] {{
        border: 0px solid {COR_CAMPO} !important; 
		padding: 2px 8px !important;            /* mesma altura */
		margin-bottom: 2px !important;  
		border-radius: 0 !important;
		margin-bottom: -4% !important;
	    padding-left: -100% !important;
    }}
    
      [data-testid="stBaseButton-secondary"]:has(kbd[aria-label="Shortcut Ctrl + Entereeeeeee "]){{/* BOTAO RUN */
        margin-top: -11.05% !important;
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
    div[data-testid="stVerticalBlock"][class*="st-key-Terminal_preview st-emotion-cache-1gz5zxc e12zf7d53"] {{  /* PREVIEWS  */
        background-color: {THEMA_APP2} !important;
        position: fixed !important;
        bottom: 10% !important;
        padding-left:0% !important;
        right: 0% !important;
        z-index: 9999 !important;
        display: flex !important;
        justify-content: space-between !important;
        padding: 0px !important;
        width:50% !important; 
		
    }}
	div[class*="st-key-Terminal_preview"] summary.st-emotion-cache-11ofl8m {{ /* PREVIEWS CABECALHO */
	    background-color: {THEMA_APP1} !important;
	    heigth:50% !important; 
	}}



    div[data-testid="stColumn"][class*="stColumn st-emotion-cache-de7oey e12zf7d52"] {{          /*  TERMINAL  */
        background-color: {THEMA_APP2} !important;
        position: fixed !important;
        bottom: 1% !important;
        padding-left:0% !important;
        right: 0% !important;
        z-index: 9999 !important;
        display: flex !important;
        justify-content: space-between !important;
        padding: 0px !important;
        width:100% !important;
        
    }}

                                                                                /* CHECKBOX */
    [data-testid="stCheckbox"] div {{
        color:  !important;
        text-decoration: underline !important;
        
        padding: 1px !important;
    }}

    </style>


    """

	st.markdown(page_bg, unsafe_allow_html=True)


	def resumo_dict_para_html(dados_str: str) -> str:
		import ast
		import os
		from datetime import datetime
		dados = ast.literal_eval(dados_str)

		pastas = dados.get("pastas", 0)
		arquivos = dados.get("arquivos", 0)

		extensoes = dados.get("extensao", {})
		extensoes_str = " / ".join(f"{v}{k}" for k, v in extensoes.items())

		datas = dados.get("datas", [])
		if datas:
			criado_raw = datas[0].get("criado", "-")
			modificado_raw = datas[0].get("modificado", "-")

			try:
				criado = datetime.strptime(criado_raw[:19], "%Y-%m-%d %H:%M:%S").strftime("%d/%m/%Y")
			except:
				criado = criado_raw  # se não der pra converter, mantém o valor original

			try:
				modificado = datetime.strptime(modificado_raw[:19], "%Y-%m-%d %H:%M:%S").strftime("%d/%m/%Y")
			except:
				modificado = modificado_raw
		else:
			criado = "-"
			modificado = "-"

		try:
			versoes = dados.get("versoes", [])
			versoes_str = " / ".join(
				", ".join(v) if isinstance(v, (set, list, tuple)) else str(v)
				for v in versoes
			)
		except TypeError:
			versoes = ''
			versoes_str = ''
		return f"""
	<span style="color:{COR_CAMPO}; margin-left:8px;">{versoes_str}</span>
	<span style="opacity:0.1;">&nbsp;&nbsp; | &nbsp;&nbsp;</span>
	<span style="color:{COR_MENU}; font-weight:700; opacity:0.85;">📚{saudacao_por_hora_sistema()} </span>
	<span>{NOME_USUARIO} !</span>
	<span style="opacity:0.1;">&nbsp;&nbsp; | &nbsp;&nbsp;</span>
	<span style="color:{COR_MENU}; font-weight:700; opacity:0.85;">Custom atual:</span>
	<span style="font-weight:500;"> {NOME_CUSTOM} </span>
	<span style="opacity:0.1;">&nbsp;&nbsp; | &nbsp;&nbsp;</span>
	<span style="color:{COR_MENU}; font-weight:700; opacity:0.85;">Projeto :material/content_paste:</span>
	<span style="font-weight:500;"> {os.path.basename(Pasta_Projeto_Atual)} </span>
	<span style="opacity:0.1;">&nbsp;&nbsp; | &nbsp;&nbsp;</span>
	<span style="color:{COR_MENU}; font-weight:700; opacity:0.85;">Criado:</span>
	<span>{criado}</span>
	<span style="opacity:0.1;">&nbsp;&nbsp; | &nbsp;&nbsp;</span>
	<span style="color:{COR_MENU}; font-weight:700; opacity:0.85;">Modificado:</span>
	<span>{modificado}</span>
	<span style="opacity:0.1;">&nbsp;&nbsp; | &nbsp;&nbsp;</span>
	<span style="color:{COR_MENU}; font-weight:700; opacity:0.85;"> Projeto Com:&nbsp;&nbsp;</span>
	<span style="color:{COR_MENU}; font-weight:700; opacity:0.85;">:material/folder:</span>
	<span >{pastas}</span>
	<span style="opacity:0.1;">&nbsp;&nbsp; | &nbsp;&nbsp;</span>
	<span style="color:{COR_MENU}; font-weight:700; opacity:0.85;">:material/insert_drive_file:</span>
	<span >{arquivos}</span>
	<span style="opacity:0.1;">&nbsp;&nbsp; | &nbsp;&nbsp;</span>
	<span style="color:{COR_MENU}; font-weight:700; opacity:0.85;">:material/dynamic_feed:&nbsp;</span>
	<span>{extensoes_str.lower().replace('/','&nbsp;')}</span>


	"""

	TOP_CAB = f"""
	<style>
	.footer {{
	    position: fixed !important;
	    bottom: -2% !important;
	    left: 0 !important;
	    right: 0 !important;
	    height: 20px !important;
	    background: {THEMA_APP1} !important;
	    z-index: 99999999 !important;
	    display: flex !important;
	    align-items: center !important;
	    gap: 14px !important;
	    padding: 20px !important;
	    color: white !important;
	    font-size: 13px !important;
	    white-space: nowrap !important;
	    
	}}
	</style>

	<div class="footer">
	{resumo_dict_para_html(Estrutura_projeto)}
	</div>
	"""

	import streamlit as st

	# Injeta CSS para mudar o fundo do Ace Editor


	# Agora seu editor Ace (exemplo com componente)
	# content = st_ace()  # ou st.components.v1.html(...)

	def criar_estilos_botao():  # ainda noa usei
		"""Estilos CSS personalizados"""
		return f"""		         
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

	st.markdown(TOP_CAB, unsafe_allow_html=True)
	return (IMAGEM_LOGO, NOME_CUSTOM, NOME_USUARIO, COR_CAMPO, COR_MENU, THEMA_EDITOR,EDITOR_TAM_MENU,THEMA_PREVIEW,
	        PREVIEW_TAM_MENU,THEMA_TERMINAL,TERMINAL_TAM_MENU,TOP_CAB,FONTE_MENU,FONTE_CAMPO)

# ✅ IMPORTS NO TOPO (CORRIGIDO)
