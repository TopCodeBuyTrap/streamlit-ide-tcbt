import os

from APP_Editor_Run_Preview import Editor_Previews
from APP_SUB_Funcitons import Identificar_linguagem
from APP_SUB_Janela_Explorer import listar_arquivos_e_pastas
from Banco_dados import ler_CONTROLE_ARQUIVOS, Del_CONTROLE_ARQUIVOS, se_CONTROLE_ARQUIVOS



def Sidebar(st, col2, lista_projeto, qt_col):

	"""Sidebar: Projeto + Banco NUM MESMO LUGAR - VERSÃO CORRIGIDA SEM DUPLICAÇÃO"""

	# Inicializa estados específicos da sidebar (CORRIGIDO)
	if 'file_status_sidebar' not in st.session_state:
		st.session_state.file_status_sidebar = {}
	if 'editor_ativo_sidebar' not in st.session_state:
		st.session_state.editor_ativo_sidebar = None
	if 'expanders_abertos_sidebar' not in st.session_state:
		st.session_state.expanders_abertos_sidebar = set()

	todos_abertos = []

	# 1. PROCESSA PROJETO
	def processar_projeto(nome_item, caminho_item, nivel=0):
		abertos_locais = []
		if os.path.isdir(caminho_item):
			pasta_id = f"exp_sidebar_{caminho_item.replace('/', '_').replace('\\', '_')}"
			mostrar_conteudo = st.checkbox(
				f"{nome_item} 📁",
				key=pasta_id,
				value=pasta_id in st.session_state.expanders_abertos_sidebar
			)
			if mostrar_conteudo:
				st.session_state.expanders_abertos_sidebar.add(pasta_id)
				l, Container_Sidebar = st.columns([0.5, 9])
				with Container_Sidebar:
					if caminho_item not in st.session_state:
						st.session_state[caminho_item] = listar_arquivos_e_pastas(caminho_item)
					for nome_sub, caminho_sub in st.session_state[caminho_item]:
						sub_abertos = processar_projeto(nome_sub, caminho_sub, nivel + 1)
						abertos_locais.extend(sub_abertos)
			else:
				st.session_state.expanders_abertos_sidebar.discard(pasta_id)
		else:
			if nome_item not in st.session_state.file_status_sidebar:
				st.session_state.file_status_sidebar[nome_item] = True

			status = st.checkbox(nome_item, key=f"chk_sidebar_{caminho_item.replace('/', '_').replace('\\', '_')}")
			st.session_state.file_status_sidebar[nome_item] = status
			if status:
				abertos_locais.append((nome_item, caminho_item, "projeto"))
		return abertos_locais

	# Processa PROJETO
	lista_projeto = [item for item in lista_projeto if item is not None and len(item) == 2]
	for nome_item, caminho_item in lista_projeto:
		abertos_item = processar_projeto(nome_item, caminho_item)
		todos_abertos.extend(abertos_item)

	# 2. ADICIONA BANCO (SEM DUPLICAR)
	banco_arquivos = ler_CONTROLE_ARQUIVOS()
	for nome_arq, caminho, conteudo, ext in banco_arquivos:
		if se_CONTROLE_ARQUIVOS(caminho, None):
			# VERIFICA SE JÁ NÃO EXISTE NO PROJETO
			if not any(nome == nome_arq for nome, _, _ in todos_abertos):
				todos_abertos.append((nome_arq, caminho, "banco"))

	# Remove duplicatas mantendo último (MELHORADO)
	vistos = set()
	todos_abertos_unicos = []
	for item in reversed(todos_abertos):
		if item[0] not in vistos:
			todos_abertos_unicos.append(item)
			vistos.add(item[0])
	todos_abertos = todos_abertos_unicos[::-1]

	# 3. LOOP PRINCIPAL - PROJETO + BANCO
	Arquivo_Selecionado_Completo = []
	Arquivo_Selecionado_Nomes = []
	if todos_abertos:
		for im in range(0, len(todos_abertos), qt_col):

			linha = st.columns(qt_col)
			for j, (arquivo, diretorio, origem) in enumerate(todos_abertos[im:im + qt_col]):
					# Determina estado ativo
				editor_ativo = st.session_state.editor_ativo_sidebar
				emj = '▶️' if editor_ativo == arquivo else ''
				if origem == "banco":
					if st.button(f"{emj}{arquivo} X",key=f"btn_banco_{arquivo}_{j}",use_container_width=True,type='tertiary'):
						Del_CONTROLE_ARQUIVOS(arquivo)
						st.rerun()
					Arquivo_Selecionado_Completo.append(diretorio)
					Arquivo_Selecionado_Nomes.append(f'[{arquivo}]')


				else:
					Arquivo_Selecionado_Completo.append(diretorio)
					Arquivo_Selecionado_Nomes.append(arquivo)
		st.markdown("----")

	return Arquivo_Selecionado_Nomes, Arquivo_Selecionado_Completo