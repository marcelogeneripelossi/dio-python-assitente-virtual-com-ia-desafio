## Código a ser utilizado no Colab. No Notebook são gerados os arquivos de dados para utilização da simulação do Agente.
## Para simulação utilizando uma interface simples com Streamlit, é utilizado o app.py
## Versão: lê os dados já gravados em arquivos na pasta 'data/'

import csv
import json
import pandas as pd

import os
import subprocess

# system_prompt = """
# Você é o Finassist, um assistente virtual com IA especializado em educação financeira e planejamento de metas. Seu público-alvo são clientes que buscam organizar suas finanças de forma consciente.
# 
# [DIRETRIZES DE COMPORTAMENTO]
# 1. Papel: Atue como um mentor e educador financeiro. Seu foco é explicar os conceitos e ajudar o cliente a entender suas opções, nunca forçar a venda de um produto.
# 2. Tom de Voz: Didático, profissional, encorajador e transparente. Evite jargões excessivamente complexos sem explicá-los primeiro.
# 3. Personalização: Utilize ativamente os dados de perfil (como os do João Silva), transações e histórico fornecidos no contexto para dar respostas personalizadas.
# 
# [REGRAS DE SEGURANÇA E ANTI-ALUCINAÇÃO]
# 1. Restrição de Base: Responda às perguntas baseando-se ESTRITAMENTE nos dados fornecidos (Perfil, Transações e Produtos).
# 2. Proibição de Invenção: Se o cliente perguntar sobre um dado, valor ou produto financeiro que não está na base fornecida, responda exatamente: "Sinto muito, mas não tenho essa informação no momento."
# 3. Alinhamento de Risco: Nunca sugira produtos de risco médio ou alto (como Fundos de Ações) se o perfil do investidor constar como "conservador" ou se o cliente não aceitar riscos.
# 4. Escopo Fechado: Se o usuário tentar desviar o assunto para temas não financeiros (programação, culinária, etc.), recuse educadamente e retorne ao foco financeiro.
# """
#

# ============================================================
# Utilidades
# ============================================================

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


def normalizar_perfil(perfil):
    perfil = perfil.lower().strip()

    mapa = {
        "conservador": "conservador",
        "conservadora": "conservador",
        "moderado": "moderado",
        "moderada": "moderado",
        "arrojado": "arrojado",
        "arrojada": "arrojado"
    }

    return mapa.get(perfil, perfil)

# ============================================================
# Carregamento dos dados
# ============================================================

def carregar_dados():
    with open('data/perfil_investidor.json', 'r', encoding='utf-8') as f:
        perfis = json.load(f)
    with open('data/produtos_financeiros.json', 'r', encoding='utf-8') as f:
        produtos = json.load(f)
    with open("data/palavras_chave.json", encoding="utf-8") as f:
        palavras_chave = json.load(f)
    with open("data/chave_sugestoes.json", encoding="utf-8") as f:
        chave_sugestoes = json.load(f)
    transacoes = pd.read_csv('data/transacoes.csv')
    historico = pd.read_csv('data/historico_atendimento.csv')
    return perfis, produtos, transacoes, historico, palavras_chave, chave_sugestoes

# ============================================================
# Motor do Finassist
# ============================================================

def motor_finassist(
    perfil,
    pergunta,
    produtos,
    historico,
    palavras_chave,
    chave_sugestoes
):

    pergunta_lower = pergunta.lower()

    resposta_final = []

    perfil_cliente = normalizar_perfil(
        perfil["perfil_investidor"]
    )

    risco_por_perfil = {
        "conservador": "baixo",
        "moderado": "medio",
        "arrojado": "alto"
    }

    # ========================================================
    # 1) Metas
    # ========================================================

    quer_metas = any(
        termo in pergunta_lower
        for termo in palavras_chave.get("meta", [])
    )

    if quer_metas:

        metas = perfil.get("metas", [])

        if metas:

            texto_metas = []

            for m in metas:
                texto_metas.append(
                    f"- {m['meta']} "
                    f"(R$ {formatar_moeda(m['valor_necessario'])} "
                    f"até {m['prazo']})"
                )

            resposta_final.append(
                "Suas metas atuais são:\n"
                + "\n".join(texto_metas)
            )

        else:

            resposta_final.append(
                "Você não possui metas cadastradas."
            )

    # ========================================================
    # 2) Histórico
    # ========================================================

    quer_historico = any(
        termo in pergunta_lower
        for termo in [
            "atendimento",
            "histórico",
            "historico",
            "recentemente",
            "último atendimento",
            "ultimo atendimento"
        ]
    )

    if quer_historico:

        hist = historico[
            historico["id_cliente"] == perfil["id"]
        ]

        if not hist.empty:

            ultimo = (
                hist
                .sort_values("data")
                .iloc[-1]
            )

            resposta_final.append(
                f"Seu último atendimento foi em "
                f"{ultimo['data']}, "
                f"tema: {ultimo['tema']}.\n"
                f"Resumo: {ultimo['resumo']}."
            )

    # ========================================================
    # 3) Riscos
    # ========================================================

    if (
        "risco" in pergunta_lower
        or "volatilidade" in pergunta_lower
    ):

        resposta_final.append(
            "Os produtos financeiros podem apresentar:\n"
            "- Risco baixo: Tesouro Selic, CDB e LCI/LCA.\n"
            "- Risco médio: Fundos Multimercado.\n"
            "- Risco alto: Fundos de Ações e ETFs internacionais."
        )

    # ========================================================
    # 4) Perfil explícito
    # ========================================================

    perfil_detectado = None

    for termo in [
        "conservador",
        "conservadora",
        "moderado",
        "moderada",
        "arrojado",
        "arrojada"
    ]:

        if termo in pergunta_lower:

            perfil_detectado = normalizar_perfil(termo)
            break

    # ========================================================
    # 5) Meu perfil
    # ========================================================

    if (
        perfil_detectado is None
        and "perfil" in pergunta_lower
    ):

        perfil_detectado = perfil_cliente

    # ========================================================
    # 6) Investimentos
    # ========================================================

    quer_investimento = any(
        termo in pergunta_lower
        for termo in palavras_chave.get(
            "investir",
            []
        )
    )

    if quer_investimento and perfil_detectado is None:

        perfil_detectado = perfil_cliente

    # ========================================================
    # 7) Produtos pelo perfil
    # ========================================================

    if perfil_detectado:

        risco_alvo = risco_por_perfil[
            perfil_detectado
        ]

        produtos_perfil = [

            p["nome"]

            for p in produtos

            if p["risco"] == risco_alvo
        ]

        if produtos_perfil:

            resposta_final.append(
                f"Investimentos para o perfil "
                f"{perfil_detectado} são:\n"
                + "\n".join(
                    f"- {p}"
                    for p in produtos_perfil
                )
            )

    # ========================================================
    # 8) Sugestões acumuladas
    # ========================================================

    sugestoes = []

    for chave, termos in palavras_chave.items():

        encontrou_chave = any(
            termo in pergunta_lower
            for termo in termos
        )

        if not encontrou_chave:
            continue

        # chave direta
        if chave in chave_sugestoes:

            sugestoes.extend(
                chave_sugestoes[chave]
            )

        # # procura sugestões pelos termos
        # for termo in termos:

        #     termo_normalizado = (
        #         termo
        #         .lower()
        #         .replace(" ", "_")
        #         .replace("/", "_")
        #     )

        #     if termo_normalizado in chave_sugestoes:

        #         sugestoes.extend(
        #             chave_sugestoes[
        #                 termo_normalizado
        #             ]
        #         )

    # remove duplicidades
    sugestoes = list(dict.fromkeys(sugestoes))

    if sugestoes:

        resposta_final.append(
            "Sugestões:\n"
            + "\n".join(
                f"- {s}"
                for s in sugestoes
            )
        )

    # ========================================================
    # 9) Fallback
    # ========================================================

    if resposta_final:

        return "\n\n".join(resposta_final)

    return (
        "Sinto muito, mas não tenho essa "
        "informação detalhada no momento. "
        "Posso ajudar com metas, histórico "
        "ou sugestões de investimento."
    )


# ============================================================
# Interação
# ============================================================

def rodar_interacao(

    perfis,
    produtos,
    historico,
    palavras_chave,
    chave_sugestoes

):

    print(
        "Finassist: Olá! "
        "Sou seu assistente financeiro pessoal."
    )

    print("\nClientes cadastrados:")

    for p in sorted(
        perfis,
        key=lambda x: x["nome"]
    ):

        print(f"- {p['nome']}")

    while True:

        nome = input(
            "\nDigite o nome ou sobrenome "
            "do cliente ('FIM' para sair): "
        ).strip()

        if nome.lower() == "fim":

            print("Encerrando...")
            return

        encontrados = [

            p

            for p in perfis

            if nome.lower()
            in p["nome"].lower()
        ]

        if len(encontrados) == 0:

            print(
                "Nenhum cliente encontrado."
            )

            continue

        if len(encontrados) > 1:

            print(
                "\nForam encontrados "
                "vários clientes:"
            )

            for p in encontrados:

                print(f"- {p['nome']}")

            continue

        perfil = encontrados[0]

        print(
            f"\nConectado como "
            f"{perfil['nome']} "
            f"({perfil['perfil_investidor']})"
        )

        while True:

            pergunta = input(
                f"\n{perfil['nome']}, "
                f"como posso ajudar? "
                f"('FIM' para sair): "
            )

            if pergunta.lower() == "fim":

                print("Encerrando...")
                return

            resposta = motor_finassist(
                perfil,
                pergunta,
                produtos,
                historico,
                palavras_chave,
                chave_sugestoes
            )

            print(
                "\nFinassist:"
            )

            print(resposta)

# ============================================================
# Main
# ============================================================

if __name__ == "__main__":

    cls()

    (
        perfis,
        produtos,
        transacoes,
        historico,
        palavras_chave,
        chave_sugestoes
    ) = carregar_dados()

    rodar_interacao(
        perfis,
        produtos,
        historico,
        palavras_chave,
        chave_sugestoes
    )
