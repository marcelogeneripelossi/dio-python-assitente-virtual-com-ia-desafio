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

def detectar_intencao(
    pergunta,
    tokens,
    chave
):

    termos = contexto.palavras_chave.get(
        chave,
        []
    )

    resultado_termo_no_texto = any(
        normalizar_texto(termo) in pergunta
        for termo in termos
    )

    if resultado_termo_no_texto:
        return True     

    resultado_singular_nos_tokens = any(
        singularizar(normalizar_texto(termo)) in tokens
        for termo in termos
    )

    return resultado_termo_no_texto or resultado_singular_nos_tokens

def detectar_intencao_tokens(tokens, chave):

    termos = contexto.palavras_chave.get(
        chave,
        []
    )

    termos_normalizados = [
        normalizar_texto(termo)
        for termo in termos
    ]

    return any(
        termo in tokens
        for termo in termos_normalizados
    )

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

    texto = re.sub(
        r"[^\w\s]",
        " ",
        texto
    )

    texto = re.sub(
        r"\s+",
        " ",
        texto
    ).strip()

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

def singularizar(token):

    if len(token) <= 3:
        return token

    if token.endswith("oes"):
        return token[:-3] + "ao"

    if token.endswith("aes"):
        return token[:-3] + "ao"

    if token.endswith("ais"):
        return token[:-3] + "al"

    if token.endswith("eis"):
        return token[:-3] + "el"

    if token.endswith("is"):
        return token[:-2] + "il"

    if token.endswith("ns"):
        return token[:-2] + "m"

    if token.endswith("es"):
        return token[:-2]

    if token.endswith("s"):
        return token[:-1]

    return token

def tokenizar(texto):
    texto = normalizar_texto(texto)

    tokens = texto.split()

    tokens_normalizados = [
        singularizar(token)
        for token in tokens
    ]    

    return tokens_normalizados

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

