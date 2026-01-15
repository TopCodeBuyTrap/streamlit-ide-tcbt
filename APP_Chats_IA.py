# https://ollama.com/library/codellama:7b

'''# Instala Ollama
curl -fsSL https://ollama.com/install.sh | sh

# Baixa CodeLlama 7B já pronto (4GB)
ollama pull codellama:7b

# Usa
ollama list
ollama serve

'''
import subprocess

import streamlit as st
from streamlit_ace import st_ace
import requests
import re

MODEL = "codellama:7b"
OLLAMA_URL = "http://localhost:11434/api/generate"

def gerar_codigo(prompt, acao):
    payload = {
        "model": MODEL,
        "prompt": f"SÓ CÓDIGO PYTHON PURO\n{acao.upper()}: {prompt}",
        "stream": False,
        "options": {"temperature": 0.1}
    }

    r = requests.post(OLLAMA_URL, json=payload, timeout=180)

    try:
        data = r.json()
    except Exception:
        raise RuntimeError("Resposta inválida do Ollama")

    if "response" not in data:
        erro = data.get("error") or data.get("detail") or str(data)
        raise RuntimeError(f"Ollama retornou erro: {erro}")

    return re.sub(
        r'```python|```|\n\s*\n',
        '\n',
        data["response"]
    ).strip()






def CODOLLAMA_CHAT(prompt, acao):
    processo = subprocess.Popen(
        [
            r"C:\Users\henri\AppData\Local\Programs\Ollama\ollama.exe",
            "run",
            "codellama:7b"
        ],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        encoding="utf-8",
        errors="replace",
        creationflags=subprocess.CREATE_NO_WINDOW,
    )

    stdout, stderr = processo.communicate(
        input=f"SÓ CÓDIGO PYTHON PURO\n{acao.upper()}: {prompt}"
    )

    if processo.returncode != 0:
        raise RuntimeError(stderr.strip() or "Erro no Ollama CLI")

    return re.sub(
        r'```python|```|\n\s*\n',
        '\n',
        stdout
    ).strip()





def OLLAMA_CHAT_IA(prompt,acao):
    processo = subprocess.Popen(
        [r"C:\Users\henri\AppData\Local\Programs\Ollama\ollama.exe", "run", "llama3.2"], #gemma3:1b  e  llama3.2
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        encoding="utf-8",
        errors="replace",
        bufsize=1,
        creationflags=subprocess.CREATE_NO_WINDOW,
        universal_newlines=True
    )

    stdout, stderr = processo.communicate(input=f"SÓ CÓDIGO PYTHON PURO\n{acao.upper()}: {prompt}",)

    resposta = stdout.strip()

    return resposta