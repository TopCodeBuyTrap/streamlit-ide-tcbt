import os
from pathlib import Path

from APP_SUB_Funcitons import Identificar_linguagem, sincronizar_estrutura, Sinbolos
from APP_SUB_Janela_Explorer import listar_arquivos_e_pastas
from Banco_dados import ler_CONTROLE_ARQUIVOS, Del_CONTROLE_ARQUIVOS, se_CONTROLE_ARQUIVOS
import streamlit as st

def Sidebar_Diretorios(st, lista_projeto, qt_col):

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
			is_venv = any(venv in nome_item.lower() for venv in ['.venv', 'virtual'])
			emoji = '🛠️' if is_venv else '📁'  # 🐍 para venv, ➤ para outros

			mostrar_conteudo = st.checkbox(
				f"{nome_item} {emoji}",
				key=pasta_id,
				value=pasta_id in st.session_state.expanders_abertos_sidebar
			)
			'''mostrar_conteudo = st.pills(
				label=f"📁{nome_item}",  # obrigatoriamente o primeiro argumento
				options=[f"📁{nome_item}"],  # lista de opções
				key=pasta_id,
				selection_mode="single",
				width='stretch',
				label_visibility="collapsed"
			)'''
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
			em = Sinbolos(nome_item)
			status = st.pills('caminho_item',f'{em}{nome_item}', key=f"chk_sidebar_{caminho_item.replace('/', '_').replace('\\', '_')}",
             selection_mode="single",width='stretch',label_visibility="collapsed",)
			st.session_state.file_status_sidebar[nome_item] = status
			if status:
				abertos_locais.append((nome_item, caminho_item, "projeto"))
		return abertos_locais

	# Processa PROJETO
	lista_projeto = [item for item in lista_projeto if item is not None and len(item) == 2]
	with st.container(border=True):
		for nome_item, caminho_item in lista_projeto:
			abertos_item = processar_projeto(nome_item, caminho_item)
			todos_abertos.extend(abertos_item)

	# 2. ADICIONA BANCO (SEM DUPLICAR)
	banco_arquivos = ler_CONTROLE_ARQUIVOS()
	for nome_arq, caminho, conteudo, ext in banco_arquivos:
		if sincronizar_estrutura(caminho) == False:# verifica se o aruivo esta no ".virtual_tcbt" / "Arvore_projeto.json"
			if se_CONTROLE_ARQUIVOS(caminho, None):
					todos_abertos.append((nome_arq, caminho, "banco"))

	# Remove duplicatas mantendo último (MELHORADO)
	vistos = set()
	todos_abertos_unicos = []
	for item in reversed(todos_abertos):
		todos_abertos_unicos.append(item)
		vistos.add(item[0])
	todos_abertos = todos_abertos_unicos[::-1]

	# 3. LOOP PRINCIPAL - PROJETO + BANCO
	Arquivo_Selecionado_Completo = []
	Arquivo_Selecionado_Nomes = []
	if todos_abertos:
		with st.container(border=True):
			for im in range(0, len(todos_abertos), qt_col):
				for j, (arquivo, diretorio, origem) in enumerate(todos_abertos[im:im + qt_col]):
					Arquivo_Selecionado_Completo.append(diretorio)
					Arquivo_Selecionado_Nomes.append(arquivo)
					if origem == "banco":
						if st.button(f"{Sinbolos(arquivo)}{arquivo}' X",key=f"btn_banco_{arquivo}_{j}",use_container_width=True,type='tertiary'):
							Del_CONTROLE_ARQUIVOS(arquivo)
							st.rerun()



	return Arquivo_Selecionado_Nomes, Arquivo_Selecionado_Completo

import os
import streamlit as st
import pandas as pd
from st_aggrid import AgGrid, GridOptionsBuilder, GridUpdateMode, JsCode
from pathlib import Path

EXT_ICONS = {
    ".py": "🐍",
    ".txt": "📄",
    ".js": "🟨",
    ".html": "🌐",
    ".css": "🎨",
    ".json": "🗂️",
    ".md": "📝",
    ".cpp": "⚙️",
    ".java": "☕",
    ".php": "🐘",
    ".rb": "💎"
}

def Sidebar_(st, lista_projeto):
	import os, pandas as pd, json
	from pathlib import Path
	from st_aggrid import AgGrid, GridOptionsBuilder, GridUpdateMode, JsCode


	if "expanded" not in st.session_state:
		st.session_state.expanded = set()
	if "selecionados" not in st.session_state:
		st.session_state.selecionados = []

	ROOT = Path(lista_projeto)

	# Função recursiva para montar estrutura de pastas
	def montar(base, nivel=0, origem="projeto"):
		linhas = []
		try:
			itens = sorted(os.listdir(base))
		except PermissionError:
			return linhas
		for nome in itens:
			caminho = os.path.join(base, nome)
			is_dir = os.path.isdir(caminho)
			linhas.append({
				"nome": nome,
				"caminho": caminho,
				"tipo": "pasta" if is_dir else "arquivo",
				"nivel": nivel,
				"expanded": caminho in st.session_state.expanded,
				"selecionado": caminho in st.session_state.selecionados,
				"origem": origem
			})
			if is_dir and caminho in st.session_state.expanded:
				linhas.extend(montar(caminho, nivel + 1, origem))
		return linhas

	# ------------------------------
	# Monta DataFrame do projeto
	df_projeto = pd.DataFrame(montar(ROOT, origem="projeto"))

	# ------------------------------
	# Monta DataFrame do banco
	banco_arquivos = ler_CONTROLE_ARQUIVOS()  # retorna lista de (nome_arq, caminho, conteudo, ext)
	todos_abertos = []
	for nome_arq, caminho, conteudo, ext in banco_arquivos:
		if not sincronizar_estrutura(caminho):
			if se_CONTROLE_ARQUIVOS(caminho, None):
				todos_abertos.append((nome_arq, caminho, "banco"))

	# Remove duplicatas mantendo último
	vistos = set()
	todos_abertos_unicos = []
	for item in reversed(todos_abertos):
		if item[0] not in vistos:
			todos_abertos_unicos.append(item)
			vistos.add(item[0])
	todos_abertos = todos_abertos_unicos[::-1]

	linhas_banco = []
	for arquivo, diretorio, origem in todos_abertos:
		linhas_banco.append({
			"nome": arquivo,
			"caminho": diretorio,
			"tipo": "arquivo",
			"nivel": 0,
			"expanded": False,
			"selecionado": diretorio in st.session_state.selecionados,
			"origem": origem
		})
	df_banco = pd.DataFrame(linhas_banco)

	# Concatena projeto + banco
	df = pd.concat([df_projeto, df_banco], ignore_index=True)

	# ------------------------------
	# Botão limpar
	if st.button("🗑️ Limpar", use_container_width=True):
		st.session_state.selecionados = []
		st.rerun()

	# ------------------------------
	# Renderer com ícone diferenciado para banco
	tree_renderer = JsCode("""
	class TreeRenderer {
	    init(params) {
	        this.eGui = document.createElement('div');
	        this.eGui.style.paddingLeft = (params.data.nivel * 25) + 'px';
	        this.eGui.style.fontFamily = 'monospace';
	        this.eGui.style.cursor = 'pointer';

	        let icon = '';
	        let corIcone = '#666';
	        let bg = params.data.origem==='banco' ? '#1f1f1f' : 'transparent';  // fundo diferente para arquivos do banco

	        if (params.data.tipo === 'pasta') {
	            icon = params.data.expanded ? '▾' : '▸';
	            corIcone = '#007acc';
	        } else {
	            const EXT_ICONS = """ + json.dumps(EXT_ICONS) + """;
	            let ext = params.value.slice(params.value.lastIndexOf('.'));
	            icon = EXT_ICONS[ext] || '📄';
	            corIcone = params.data.origem === 'banco' ? '#ff7f0e' : '#666';
	        }

	        let nome = params.value || '';
	        let isSelected = params.data.selecionado;

	        this.eGui.innerHTML = `
	        <div style="background-color:${bg};padding:2px;border-radius:4px;">
	            <span style="margin-right:12px;color:${corIcone};font-weight:bold;font-size:14px;">${icon}</span>
	            <span style="${isSelected?'color:#059669;font-weight:bold;':'color:#E4DDD0;'}">${nome}</span>
	        </div>
	        `;
	    }
	    getGui() { return this.eGui; }
	    refresh(params) { return false; }
	}
	""")

	gb = GridOptionsBuilder.from_dataframe(df)
	gb.configure_column("nome", headerName="📁 Explorador de Arquivos",
	                    cellRenderer=tree_renderer, width=800, resizable=True,
	                    sortable=True, filter=True, pinned="left")
	for col in ["caminho", "tipo", "nivel", "expanded", "selecionado", "origem"]:
		gb.configure_column(col, hide=True)
	gb.configure_grid_options(
		domLayout="normal",
		suppressRowHoverHighlight=False,
		rowSelection="multiple",
		rowMultiSelectWithClick=True,
		suppressRowClickSelection=False,
		headerHeight=40,
		rowHeight=28,
		animateRows=True
	)

	response = AgGrid(df, gridOptions=gb.build(),
	                  update_mode=GridUpdateMode.SELECTION_CHANGED,
	                  allow_unsafe_jscode=True,
	                  height=500,
	                  fit_columns_on_grid_load=True)

	# Apenas processa seleção de arquivos do banco
	selected = response["selected_rows"]

	if selected is not None and not selected.empty:
		for idx, item in selected.iterrows():
			caminho = item["caminho"]
			tipo = item["tipo"]
			origem = item["origem"]

			# Pastas: expand/collapse
			if tipo == "pasta":
				if caminho in st.session_state.expanded:
					st.session_state.expanded.remove(caminho)
				else:
					st.session_state.expanded.add(caminho)
				st.rerun()

			else:
				# Arquivos (projeto ou banco) → marca/desmarca
				if caminho in st.session_state.selecionados:
					st.session_state.selecionados.remove(caminho)
				else:
					st.session_state.selecionados.append(caminho)

				# Se for do banco, mostra botão de deletar
				if origem == "banco":
					if st.button(f"❌ Deletar {item['nome']}", key=f"btn_del_{item['nome']}"):
						Del_CONTROLE_ARQUIVOS(item["nome"])
						st.session_state.selecionados.remove(caminho)

		st.rerun()
	nomes = [os.path.basename(c) for c in st.session_state.selecionados]
	completos = st.session_state.selecionados
	return nomes, completos




