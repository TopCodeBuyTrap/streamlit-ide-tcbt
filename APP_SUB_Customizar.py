

def Customization(st,NOME_CUSTOM):
	from Banco_dados import ler_CUSTOMIZATION_coluna,ATUAL_CUSTOM_agora

	TAM_EDITOR = ler_CUSTOMIZATION_coluna('EDITOR_TAM_MENU')
	TAM_TERM = ler_CUSTOMIZATION_coluna('TERMINAL_TAM_MENU')
	TAM_PREV = ler_CUSTOMIZATION_coluna('PREVIEW_TAM_MENU')
	RADIO_entra = ler_CUSTOMIZATION_coluna('RADIAL')
	BORDA_entra = ler_CUSTOMIZATION_coluna('BORDA')
	t1, t2, t3 = st.columns(3)
	with t1:
		c1, c2, c3, c4, c5 = st.columns(5)
		st.write(TAM_EDITOR,TAM_TERM,TAM_PREV,RADIO_entra,BORDA_entra)
		Tam_Font = c1.number_input('Tam Ft Editor:', max_value=40, min_value=5, value=TAM_EDITOR)
		Tam_Run = c2.number_input('Tam Ft Run:', max_value=40, min_value=5, value=TAM_PREV)
		Tam_Term = c3.number_input('Tam Ft Terminal:', max_value=40, min_value=TAM_TERM)
		RADIO = c4.number_input('Radio', value=RADIO_entra, max_value=80, min_value=0)
		BORDA = c5.number_input('Borda', value=BORDA_entra, max_value=2, min_value=0)

	if t3.button('Aplicar:'):
		ATUAL_CUSTOM_agora(st, NOME_CUSTOM, 'EDITOR_TAM_MENU', Tam_Font)
		ATUAL_CUSTOM_agora(st, NOME_CUSTOM, 'PREVIEW_TAM_MENU', Tam_Run)
		ATUAL_CUSTOM_agora(st, NOME_CUSTOM, 'TERMINAL_TAM_MENU', Tam_Term)
		ATUAL_CUSTOM_agora(st, NOME_CUSTOM, 'RADIAL', RADIO)
		ATUAL_CUSTOM_agora(st, NOME_CUSTOM, 'RADIAL', RADIO)
		ATUAL_CUSTOM_agora(st, NOME_CUSTOM, 'RADIAL', RADIO)
		ATUAL_CUSTOM_agora(st, NOME_CUSTOM, 'BORDA', BORDA)
		st.rerun()