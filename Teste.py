import os
import streamlit as st
import pandas as pd
from st_aggrid import AgGrid, GridOptionsBuilder, GridUpdateMode, JsCode

st.set_page_config(layout="wide")

ROOT = os.getcwd()

if "expanded" not in st.session_state:
	st.session_state.expanded = set()

# ✅ SEMPRE LISTA - NUNCA SET!
if "selecionados" not in st.session_state:
	st.session_state.selecionados = []


def montar(base, nivel=0):
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
			"selecionado": caminho in st.session_state.selecionados
		})

		if is_dir and caminho in st.session_state.expanded:
			linhas.extend(montar(caminho, nivel + 1))

	return linhas

st.color_picker('cor')
df = pd.DataFrame(montar(ROOT))

tree_renderer = JsCode("""
class TreeRenderer {
  init(params) {
    this.eGui = document.createElement('div');
    this.eGui.style.paddingLeft = (params.data.nivel * 25) + 'px';
    this.eGui.style.fontFamily = 'monospace';
    this.eGui.style.cursor = 'pointer';

    let icon = '';
    let corIcone = '#666';

    if (params.data.tipo === 'pasta') {
      icon = params.data.expanded ? '▾' : '▸';
      corIcone = '#007acc';
    } else {
      if (params.value.toLowerCase().endsWith('.py')) icon = '🐍';
      else if (params.value.toLowerCase().endsWith('.js')) icon = '⚡';
      else if (params.value.toLowerCase().endsWith('.html')) icon = '🌐';
      else if (params.value.toLowerCase().endsWith('.css')) icon = '🎨';
      else if (params.value.toLowerCase().endsWith('.json')) icon = '📄';
      else icon = '📄';
    }

    let nome = params.value || '';
    let isSelected = params.data.selecionado;

    this.eGui.innerHTML = `
      <span style="margin-right: 12px; color: ${corIcone}; font-weight: bold; font-size: 14px;">${icon}</span>
      <span style="${isSelected ? 'color: #059669; font-weight: bold;' : 'color: #E4DDD0;'}">${nome}</span>
    `;
  }

  getGui() {
    return this.eGui;
  }

  refresh(params) {
    return false;
  }
}
""")

gb = GridOptionsBuilder.from_dataframe(df)

gb.configure_column(
	"nome",
	headerName="📁 Explorador de Arquivos",
	cellRenderer=tree_renderer,
	width=800,
	resizable=True,
	sortable=True,
	filter=True,
	pinned="left"
)

gb.configure_column("caminho", hide=True)
gb.configure_column("tipo", hide=True)
gb.configure_column("nivel", hide=True)
gb.configure_column("expanded", hide=True)
gb.configure_column("selecionado", hide=True)

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

grid_options = gb.build()

response = AgGrid(
	df,
	gridOptions=grid_options,
	update_mode=GridUpdateMode.SELECTION_CHANGED,
	allow_unsafe_jscode=True,
	height=500,
	fit_columns_on_grid_load=True
)

selected = response["selected_rows"]

if selected is not None and not selected.empty:
	item = selected.iloc[0]
	caminho = item["caminho"]

	if item["tipo"] == "pasta":
		if caminho in st.session_state.expanded:
			st.session_state.expanded.remove(caminho)
		else:
			st.session_state.expanded.add(caminho)
		st.rerun()
	else:
		# ✅ FUNCIONA COM LISTA:
		if caminho in st.session_state.selecionados:
			st.session_state.selecionados.remove(caminho)
		else:
			st.session_state.selecionados.append(caminho)  # ✅ LISTA!
		st.rerun()

# UI dos selecionados
col1, col2 = st.columns([3, 1])
with col1:
	st.markdown("### 📋 Arquivos Selecionados")
	if st.session_state.selecionados:
		for i, caminho in enumerate(st.session_state.selecionados, 1):
			st.markdown(f"{i}. `{caminho}`")
			nome_arquivo = os.path.basename(caminho)

		st.success(f"✅ Total: {len(st.session_state.selecionados)}")
	else:
		st.info("Nenhum arquivo selecionado")

with col2:
	col_btn1, col_btn2 = st.columns(2)
	with col_btn1:
		if st.button("🗑️ Limpar", use_container_width=True):
			st.session_state.selecionados = []
			st.rerun()
	with col_btn2:
		if st.button("📤 Caminhos", use_container_width=True):
			st.code("\n".join(st.session_state.selecionados))

st.divider()
st.caption(f"📂 {len(df)} itens | `{ROOT}`")
