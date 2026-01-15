import os
import textwrap
from pathlib import Path

import ast
import re
from typing import List, Dict, Any, Optional



# ============================================================
# PARSE AST SEGURO
# ============================================================
def _parse_ast(codigo: str) -> Optional[ast.AST]:
    try:
        return ast.parse(codigo)
    except SyntaxError:
        return None


# ============================================================
# ANNOTATIONS PROFISSIONAIS (GUTTER SIMPLES, HOVER RICO)
# ============================================================
def Anotations_Editor(codigo: str) -> List[Dict[str, Any]]:
    annotations: List[Dict[str, Any]] = []
    linhas = codigo.split("\n")
    tree = _parse_ast(codigo)

    def add(row: int, level: str, emoji: str, msg: str):
        annotations.append({
            "row": row,
            "type": level,              # controla ❌ ou ⚠️
            "text": f"{emoji} {msg}"    # aparece SOMENTE no hover
        })

    # --------------------------------------------------------
    # 1. ANÁLISE TEXTUAL
    # --------------------------------------------------------
    for i, linha in enumerate(linhas):
        l = linha.strip()

        if re.search(r"\b(TODO|FIXME|BUG|HACK|XXX|NOTE)\b", l, re.I):
            add(i, "warning", "🧩", "Pendência anotada no código")

        if len(linha) > 100:
            add(i, "warning", "📏", "Linha excede 100 caracteres")

        if l.startswith("#") and len(linha) > 80:
            add(i, "warning", "💬", "Comentário excessivamente longo")

        if "print(" in l and not l.startswith("#"):
            add(i, "warning", "🐞", "Uso de print como debug")

        if "eval(" in l or "exec(" in l:
            add(i, "error", "☠️", "Uso de eval/exec (risco de segurança)")

        if l.startswith("global "):
            add(i, "warning", "🌍", "Uso de variável global")

        if l == "pass":
            add(i, "warning", "🕳️", "Bloco vazio (pass)")

        if l.startswith("except:") or ("except Exception" in l and "as" not in l):
            add(i, "error", "🚫", "Except genérico oculta erros reais")

    # --------------------------------------------------------
    # 2. ANÁLISE AST
    # --------------------------------------------------------
    if tree:
        for node in ast.walk(tree):

            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                add(
                    node.lineno - 1,
                    "warning" if ast.get_docstring(node) is None else "info",
                    "⚙️",
                    f"Função '{node.name}' sem docstring"
                    if ast.get_docstring(node) is None
                    else f"Função '{node.name}'"
                )

            elif isinstance(node, ast.ClassDef):
                add(
                    node.lineno - 1,
                    "warning" if ast.get_docstring(node) is None else "info",
                    "🏷️",
                    f"Classe '{node.name}' sem docstring"
                    if ast.get_docstring(node) is None
                    else f"Classe '{node.name}'"
                )

            elif isinstance(node, ast.Import):
                for alias in node.names:
                    add(node.lineno - 1, "info", "📦", f"Import: {alias.name}")

            elif isinstance(node, ast.ImportFrom):
                add(node.lineno - 1, "info", "📥", f"Import from {node.module}")

    else:
        try:
            ast.parse(codigo)
        except SyntaxError as e:
            add(
                (e.lineno or 1) - 1,
                "error",
                "💥",
                f"Erro de sintaxe: {e.msg}"
            )

    return annotations


# ============================================================
# MARKERS (VISUAL LIMPO, SEM POLUIÇÃO)
# ============================================================
def Marcadores_Editor(codigo: str) -> List[Dict[str, Any]]:
    markers: List[Dict[str, Any]] = []
    linhas = codigo.split("\n")
    tree = _parse_ast(codigo)

    for i, linha in enumerate(linhas):

        if len(linha) > 100:
            markers.append({
                "startRow": i,
                "startCol": 100,
                "endRow": i,
                "endCol": len(linha),
                "className": "marker-longline",
                "type": "range"
            })

        if linha.strip() == "pass":
            markers.append({
                "startRow": i,
                "startCol": 0,
                "endRow": i,
                "endCol": len(linha),
                "className": "marker-pass",
                "type": "fullLine"
            })

    if tree:
        for node in ast.walk(tree):

            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                markers.append({
                    "startRow": node.lineno - 1,
                    "startCol": 0,
                    "endRow": (node.end_lineno or node.lineno) - 1,
                    "endCol": 0,
                    "className": "marker-function-scope",
                    "type": "fullBlock"
                })

            elif isinstance(node, ast.ClassDef):
                markers.append({
                    "startRow": node.lineno - 1,
                    "startCol": 0,
                    "endRow": (node.end_lineno or node.lineno) - 1,
                    "endCol": 0,
                    "className": "marker-class-scope",
                    "type": "fullBlock"
                })

    return markers

# ============================================================
# MÉTRICA DE QUALIDADE (DASHBOARD)
# ============================================================
def calcular_qualidade(codigo: str) -> Dict[str, Any]:
    """Score profissional para dashboard da IDE."""
    ann = Anotations_Editor(codigo)

    erros = sum(1 for a in ann if a["type"] == "error")
    warnings = sum(1 for a in ann if a["type"] == "warning")
    info = sum(1 for a in ann if a["type"] == "info")
    success = sum(1 for a in ann if a["type"] == "success")

    score = max(0, 100 - (erros * 25 + warnings * 8))

    return {
        "score": round(score, 1),
        "erros": erros,
        "warnings": warnings,
        "info": info,
        "success": success,
        "total": len(ann),
        "status": "⭐ Excelente" if score > 90 else "⚡ Boa" if score > 70 else "🚨 Crítica"
    }



def Identificar_linguagem(arquivo):
    ext_map = {
        ".py": "python",
        ".js": "javascript",
        ".html": "html",
        ".css": "css",
        ".json": "json",
        ".md": "markdown",
        ".txt": "plaintext",
    }
    return ext_map.get(Path(arquivo).suffix.lower(), "plaintext")


def Criar_Arquivo_TEXTO(caminho, titulo, conteudo, ext):
    caminho_txt =rf"{caminho}\\{titulo}{ext}"

    with open(caminho_txt, "w", encoding="utf-8") as f:
        f.write(conteudo)
    return caminho_txt


def wrap_text(text, width=80):
    # Quebra o texto nas linhas originais
    lines = text.splitlines()
    wrapped_lines = []
    for line in lines:
        # Aplica wrap apenas em cada linha separadamente
        wrapped_lines.extend(textwrap.wrap(line, width=width) or [""])
    return "\n".join(wrapped_lines)


# Henrique, essa função é só pra olhar na pasta se tem um arquivo com o mesmo nome e se tiver ele procura outro nome diferente.
def gerar_nome_unico(pasta_base: Path, nome_desejado: str) -> Path:
    """
    Gera um caminho único dentro de pasta_base.
    Ex:
    Projeto
    Projeto_2
    Projeto_3
    """
    pasta_base = Path(pasta_base)
    nome_desejado = nome_desejado.strip()

    caminho = pasta_base / nome_desejado
    if not caminho.exists():
        return caminho

    contador = 2
    while True:
        novo_nome = f"{nome_desejado}_{contador}"
        novo_caminho = pasta_base / novo_nome
        if not novo_caminho.exists():
            return novo_caminho
        contador += 1

