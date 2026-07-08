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

def detectar_chaves(
    pergunta,
    tokens,
    dicionario
):

    chaves_encontradas = []

    for chave, termos in dicionario.items():

        encontrou_texto = any(
            normalizar_texto(termo) in pergunta
            for termo in termos
        )

        encontrou_token = any(
            singularizar(
                normalizar_texto(termo)
            ) in tokens
            for termo in termos
        )

        if encontrou_texto or encontrou_token:
            chaves_encontradas.append(chave)

    return chaves_encontradas

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

    for termo in termos:
        singularizar(normalizar_texto(termo)) in tokens

    resultado_singular_nos_tokens = any(
        singularizar(normalizar_texto(termo)) in tokens
        for termo in termos
    )

    return resultado_termo_no_texto or resultado_singular_nos_tokens

def detectar_intencao_DEBUG(pergunta, tokens, chave):

    termos = contexto.palavras_chave.get(chave, [])

    resultado_termo_no_texto = any(
        normalizar_texto(termo) in pergunta
        for termo in termos
    )

    resultado_singular_nos_tokens = any(
        singularizar(normalizar_texto(termo)) in tokens
        for termo in termos
    )

    if resultado_termo_no_texto or resultado_singular_nos_tokens:
        print(f"\nCHAVE: {chave}")

        for termo in termos:
            print(
                f"{termo!r}",
                normalizar_texto(termo) in pergunta,
                singularizar(normalizar_texto(termo)) in tokens
            )

        print(
            "texto =", resultado_termo_no_texto,
            "tokens =", resultado_singular_nos_tokens
        )

    return resultado_termo_no_texto or resultado_singular_nos_tokens

def formatar_moeda(valor):
    return (
        f"{valor:,.2f}"
        .replace(",", "_")
        .replace(".", ",")
        .replace("_", ".")
    )

def normalizar_expressao(texto):

    #texto = normalizar_texto(texto)

    for origem, destino in contexto.normalizacao_expressoes.items():
        texto = texto.replace(
            origem,
            destino
        )

    return texto

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

def obter_produtos(
    campo,
    valor
):
    return [
        produto
        for produto in contexto.produtos
        if produto[campo] == valor
    ]

def obter_produtos_por_tag(tag):
    produto = [
        produto for produto in contexto.produtos
                if tag in produto.get("tags", [])
                ]
    
    return produto

def obter_produtos_por_tipo(tipo):

    return [
        produto
        for produto in contexto.produtos
        if produto["tipo"] == tipo
    ]

import random
def obter_resposta(resposta_final, chave_sugestoes):
    if resposta_final:
        return "\n\n".join(resposta_final)

    # Se não houver conteúdo em resposta_final, junta todas as sugestões
    todas_sugestoes = []
    for lista in chave_sugestoes.values():
        todas_sugestoes.extend(lista)

    if todas_sugestoes:
        sugestao = random.choice(todas_sugestoes)

    # Caso não haja nenhuma sugestão em nenhuma chave
        return (
            "Sinto muito, mas não tenho essa informação detalhada no momento. Posso ajudar com suas metas ou sugestões de investimento?\n"
            f"{sugestao}"
        )

def singularizar(token):

    token = normalizar_texto(token)

    if len(token) <= 3:
        return token

    # Exceções definidas no JSON
    if token in contexto.normalizacao_palavras:
        return contexto.normalizacao_palavras[token]

    # Plurais irregulares comuns
    if token.endswith("oes"):
        return token[:-3] + "ao"

    if token.endswith("aes"):
        return token[:-3] + "ao"

    if token.endswith("ais"):
        return token[:-3] + "al"

    if token.endswith("eis"):
        return token[:-3] + "el"

    if token.endswith("is") and not token.endswith("ais"):
        return token[:-2] + "il"

    if token.endswith("ns"):
        return token[:-2] + "m"

    # plural simples
    if (
        token.endswith("s")
        and not token.endswith("ss")
    ):
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

