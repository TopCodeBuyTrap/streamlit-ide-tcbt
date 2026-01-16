# -*- mode: python ; coding: utf-8 -*-
from PyInstaller.utils.hooks import collect_all
from PyInstaller.utils.hooks import copy_metadata

datas = [('C:\\Users\\henri\\PycharmProjects\\TBCT_STREAM_IDE\\APP_.py', '.')]
binaries = []
hiddenimports = ['APP_Editor_Run_Preview.Editor_Previews', 'APP_Htmls.Main_App', 'APP_Menus.Abrir_Menu', 'APP_Menus.Apagar_Arq', 'APP_Menus.Cria_Projeto', 'APP_Menus.Custom', 'APP_SUB_Controle_Driretorios._DIRETORIO_EXECUTAVEL_', 'APP_SUB_Controle_Driretorios._DIRETORIO_PROJETOS_', 'APP_SUB_Controle_Driretorios._DIRETORIO_PROJETO_ATUAL_', 'APP_SUB_Customizar.Customization', 'APP_SUB_Funcitons.Identificar_linguagem', 'APP_SUB_Funcitons.chec_se_arq_do_projeto', 'APP_SUB_Funcitons.escreve', 'APP_SUB_Janela_Explorer.Open_Explorer', 'APP_SUB_Janela_Explorer.listar_arquivos_e_pastas', 'APP_Sidebar.Sidebar', 'APP_Terminal.Terminal', 'Abertura_TCBT.Abertura', 'Banco_dados.Del_A_CONTROLE_ABSOLUTO', 'Banco_dados.Del_CUSTOMIZATION', 'Banco_dados.ler_A_CONTROLE_ABSOLUTO', 'Banco_dados.ler_B_ARQUIVOS_RECENTES', 'os', 'pathlib.Path', 'streamlit', 'textwrap.shorten', 'time']
datas += copy_metadata('streamlit')
tmp_ret = collect_all('streamlit')
datas += tmp_ret[0]; binaries += tmp_ret[1]; hiddenimports += tmp_ret[2]
tmp_ret = collect_all('streamlit')
datas += tmp_ret[0]; binaries += tmp_ret[1]; hiddenimports += tmp_ret[2]


a = Analysis(
    ['C:\\Users\\henri\\AppData\\Local\\Temp\\tmpcjd54gwu.py'],
    pathex=['.'],
    binaries=binaries,
    datas=datas,
    hiddenimports=hiddenimports,
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='TcbT_Stream_IDE',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
coll = COLLECT(
    exe,
    a.binaries,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='TcbT_Stream_IDE',
)
