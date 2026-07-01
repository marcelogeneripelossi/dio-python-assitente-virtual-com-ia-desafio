# ============================================================
# Utilidades
# ============================================================

import re
import unicodedata

import os
import subprocess

import contexto

def cls():
    comando = 'cls' if os.name == 'nt' else 'clear'
    subprocess.run (comando, shell = True)

def formatar_moeda(valor):
    return (
        f"{valor:,.2f}"
        .replace(",", "_")
        .replace(".", ",")
        .replace("_", ".")
    )

def normalizar_texto(texto):
    texto = texto.lower()

    texto = unicodedata.normalize(
        "NFD",
        texto
    )

    texto = "".join(
        c
        for c in texto
        if unicodedata.category(c) != "Mn"
    )

    return texto

def normalizar_perfil(perfil):
    perfil = perfil.lower().strip()

    mapa = {
        "conservador": "conservador",
        "conservadora": "conservador",
        "conservadores": "conservador",
        "conservadoras": "conservador",

        "moderado": "moderado",
        "moderada": "moderado",
        "moderados": "moderado",
        "moderadas": "moderado",

        "arrojado": "arrojado",
        "arrojada": "arrojado",
        "arrojados": "arrojado",
        "arrojadas": "arrojado"
    }

    return mapa.get(perfil, perfil)

def tokenizar(texto):
    texto = normalizar_texto(texto)

    return re.findall(
        r'\b[\w/]+\b',
        texto.lower()
    )

def termo_negado(tokens, indice, janela=4):
    """
    Verifica se existe uma negação nas palavras imediatamente anteriores ao termo.

    Suporta:
    - unigramas: "não", "nunca", "jamais"
    - bigramas: "nem pensar", "forma alguma"
    """

    inicio = max(0, indice - janela)

    trecho = tokens[inicio:indice]

    # unigramas
    for token in trecho:

        if token in contexto.negacoes:
            return True

    # bigramas
    for i in range(len(trecho) - 1):

        expressao = f"{trecho[i]} {trecho[i + 1]}"

        if expressao in contexto.negacoes:
            return True

    return False

def detectar_intencao(pergunta, chave):

    pergunta_normalizada = normalizar_texto(
        pergunta
    )

    termos = contexto.palavras_chave.get(
        chave,
        []
    )

    return any(
        normalizar_texto(termo)
        in pergunta_normalizada
        for termo in termos
    )
