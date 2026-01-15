import json
import sqlite3





DB_PATH = "Base_Dados_PreDefinidos.db"

conn = sqlite3.connect(DB_PATH, check_same_thread=False)
c = conn.cursor()
c.execute("""
    CREATE TABLE IF NOT EXISTS templates (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT UNIQUE,
        arquivos TEXT
    )
""")
conn.commit()
conn.close()


def salvar_template(nome, arquivos):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute(
        "INSERT OR REPLACE INTO templates (nome, arquivos) VALUES (?, ?)",
        (nome, json.dumps(arquivos, ensure_ascii=False))
    )
    conn.commit()
    conn.close()

def listar_templates():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT nome FROM templates")
    nomes = [i[0] for i in c.fetchall()]
    conn.close()
    return nomes

def carregar_template(nome):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT arquivos FROM templates WHERE nome=?", (nome,))
    row = c.fetchone()
    conn.close()
    return json.loads(row[0]) if row else []
