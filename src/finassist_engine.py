## Código para testes do Motor do Finassist. Pode ser executado no VS Code ou via CLI. Veja o item '3. Interface de Linha de Comando (CLI)' na seção 'Como Executar' do README.
## Para simulação utilizando uma interface simples com Streamlit, é utilizado o app.py
## Versão: lê os dados já gravados em arquivos na pasta 'data/'

import csv
import json
import pandas as pd
import random

import os

import consultas_cliente
import contexto
from util import (
    cls,
    detectar_chaves,
    normalizar_perfil,
    normalizar_expressao,
    normalizar_texto,
    obter_produtos_por_tipo,
    termo_negado,
    tokenizar
)

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


# ==========================================================
# Configurações
# ==========================================================

BASE_DIR = os.path.dirname(
    os.path.abspath(__file__)
)

DATA_DIR = os.path.join(
    BASE_DIR,
    "..",
    "data"
)

DATA_DIR = os.path.abspath(
    DATA_DIR
)

# ==========================================================
# Inicialização
# ==========================================================

def inicializar_contexto(dados):
    global chave_sugestoes
    global historico
    global normalizacao_expressoes
    global normalizacao_palavras
    global palavras_chave
    global palavras_chave_produtos
    global perfis
    global produtos
    global transacoes

    contexto.chave_sugestoes = dados["chave_sugestoes"]
    contexto.historico = dados["historico"]
    contexto.normalizacao_expressoes = dados["normalizacao_expressoes"]
    contexto.normalizacao_palavras = dados["normalizacao_palavras"]
    contexto.palavras_chave = dados["palavras_chave"]
    contexto.palavras_chave_produtos = dados["palavras_chave_produtos"]
    contexto.perfis = dados["perfis"]
    contexto.produtos = dados["produtos"]
    contexto.transacoes = dados["transacoes"]

    chave_sugestoes = contexto.chave_sugestoes
    historico = contexto.historico
    normalizacao_expressoes = contexto.normalizacao_expressoes
    normalizacao_palavras = contexto.normalizacao_palavras
    palavras_chave = contexto.palavras_chave
    palavras_chave_produtos = contexto.palavras_chave_produtos
    perfis = contexto.perfis
    produtos = contexto.produtos
    transacoes = contexto.transacoes

# ============================================================
# Carregamento dos dados
# ============================================================

def carregar_dados():
    with open(
        os.path.join(
            DATA_DIR,
            "chave_sugestoes.json"
        ),
        encoding="utf-8") as f:
        chave_sugestoes = json.load(f)

    with open(
        os.path.join(
            DATA_DIR,
            "normalizacao_expressoes.json"
        ),
        encoding="utf-8") as f:
        normalizacao_expressoes = json.load(f)

    with open(
        os.path.join(
            DATA_DIR,
            "normalizacao_palavras.json"
        ),
        encoding="utf-8") as f:
        normalizacao_palavras = json.load(f)

    with open(
        os.path.join(
            DATA_DIR,
            "perfil_investidor.json"
        ), 
        'r', encoding='utf-8') as f:
        perfis = json.load(f)

    with open(
        os.path.join(
            DATA_DIR,
            "produtos_financeiros.json"
        ), 
        'r', encoding='utf-8') as f:
        produtos = json.load(f)

    with open(
        os.path.join(
            DATA_DIR,
            "palavras_chave.json"
        ),
        encoding="utf-8") as f:
        palavras_chave = json.load(f)

    with open(
        os.path.join(
            DATA_DIR,
            "palavras_chave_produtos.json"
        ),
        encoding="utf-8") as f:
        palavras_chave_produtos = json.load(f)

    transacoes = pd.read_csv(
            os.path.join(
                DATA_DIR,
                "transacoes.csv"
            ))

    historico = pd.read_csv(
        os.path.join(
            DATA_DIR,
            "historico_atendimento.csv"
        ))

    return {
        "chave_sugestoes": chave_sugestoes,
        "historico": historico,
        "normalizacao_expressoes": normalizacao_expressoes,
        "normalizacao_palavras": normalizacao_palavras,
        "palavras_chave": palavras_chave,
        "palavras_chave_produtos": palavras_chave_produtos,
        "perfis": perfis,
        "produtos": produtos,
        "transacoes": transacoes,
    }

# ============================================================
# Motor do Finassist 
# ============================================================

def motor_finassist(perfil, pergunta, dados):

    pergunta_normalizada = normalizar_expressao(pergunta)

    pergunta_normalizada = normalizar_texto(pergunta_normalizada)

    tokens = tokenizar(pergunta_normalizada)
    
    resposta_final = []

    perfil_cliente = normalizar_perfil(
        perfil["perfil_investidor"]
    )

    risco_por_perfil = {
        "conservador": "baixo",
        "moderado": "medio",
        "arrojado": "alto"
    }

    intencoes = detectar_chaves(
        pergunta_normalizada,
        tokens,
        contexto.palavras_chave
    )

    # ========================================================
    # 1) Metas
    # ========================================================

    if "meta" in intencoes:
        resposta = consultas_cliente.obter_metas(perfil)
        resposta_final.append(resposta)

    # ========================================================
    # 2) Histórico, Transações e Gastos
    # ========================================================

    #=====================
    # Último atendimento
    #=====================

    if "atendimento_ultimo" in intencoes:
        resposta = consultas_cliente.obter_ultimo_atendimento(perfil)
        resposta_final.append(resposta)

    #=====================
    # Histórico de atendimento
    #=====================

    if "atendimento_historico" in intencoes:
        resposta = consultas_cliente.obter_historico(perfil)
        resposta_final.append(resposta)
    
    #=====================
    # Últimas transações, gastos e categoria de maior gasto
    #=====================

    #=======
    # Transações
    #=======

    if "transacoes" in intencoes:
        resposta = consultas_cliente.obter_transacoes(perfil)
        resposta_final.append(resposta)


    #=======
    # Gastos
    #=======
    
    if "gastos" in intencoes:
        resposta = consultas_cliente.obter_despesas(perfil)
        resposta_final.append(resposta)

    #=======
    # Categoria de maior gasto
    #=======

    if "maior_gasto" in intencoes:
        resposta = consultas_cliente.obter_despesas_maior_categoria(perfil)
        resposta_final.append(resposta)

    #=======
    # Receitas
    #=======

    if "receitas" in intencoes:
        resposta = consultas_cliente.obter_receitas(perfil)
        resposta_final.append(resposta)

    #=====================
    # Ajuda / Suporte
    #=====================

    #=======
    # Ajuda
    #=======

    quer_ajuda = False

    if "ajuda" in intencoes:
        resposta = consultas_cliente.obter_ajuda()

        if resposta is not None:
            quer_ajuda = True
            resposta_final.append(resposta)

    #=======
    # Suporte
    #=======

    quer_suporte = False

    if "suporte" in intencoes:
        resposta = consultas_cliente.obter_suporte()

        if resposta is not None:
            quer_suporte = True
            resposta_final.append(resposta)

    # ========================================================
    # 3) Riscos
    # ========================================================

    if (
        "risco" in pergunta_normalizada
        or "volatilidade" in pergunta_normalizada
    ):

        # Cria uma cópia da lista de produtos e embaralha para garantir aleatoriedade
        produtos_embaralhados = dados["produtos"].copy()
        random.shuffle(produtos_embaralhados)
     
        produtos_por_risco = {}

        for produto in produtos_embaralhados:

            risco = produto["risco"]
            nome = produto["nome"]

            produtos_por_risco.setdefault(
                risco,
                []
            ).append(nome)

        linhas = []

        ordem = {
            "baixo": "baixo",
            "medio": "médio",
            "alto": "alto"
        }

        for risco_json, risco_texto in ordem.items():

            nomes = produtos_por_risco.get(
                risco_json,
                []
            )

            if nomes:
                nomes_limitados = nomes[:2]

                linhas.append(
                    f"- Risco {risco_texto} "
                    f"(perfil {contexto.mapa_risco_perfil[risco_json]}): "
                    + ", ".join(nomes_limitados)
                    + "."
                )

        resposta_final.append(
            "Os produtos financeiros podem apresentar:\n"
            + "\n".join(linhas)
        )

    # ========================================================
    # 4) Perfil explícito
    # ========================================================

    perfil_detectado = None
    perfil_negado = None

    for termo in contexto.perfil_tipos:
        termo_busca = termo.lower()

        for indice, token in enumerate(tokens):
            token_normalizado = token.lower()

            if token_normalizado != termo_busca:
                continue

            # ignora perfis explicitamente negados
            if termo_negado(tokens, indice):
                perfil_negado = normalizar_perfil(termo)
                break

            perfil_detectado = normalizar_perfil(termo)
            break

        if perfil_detectado:
            break

    # ========================================================
    # 4.1) Sinônimos de Perfil
    # ========================================================

    if perfil_detectado is None and perfil_negado is None:

        for termo, perfil_associado in contexto.perfil_sinonimos.items():

            if termo not in tokens:
                continue

            indice = tokens.index(termo)

            if termo_negado(tokens, indice):
                perfil_negado = perfil_associado
            else:
                perfil_detectado = perfil_associado

            break

    # ========================================================
    # 5) Meu perfil / Sugestões
    # ========================================================

    # if (perfil_detectado is None and "perfil" in pergunta_normalizada):
    #      perfil_detectado = perfil_cliente

    quer_sugestoes = False

    if "sugestoes" in intencoes:
        quer_sugestoes = True

    if quer_sugestoes and perfil_detectado is None:
        perfil_detectado = perfil_cliente

    # ========================================================
    # 6) Investimentos
    # ========================================================

    quer_investimento = any(
        termo in pergunta_normalizada
        for termo in contexto.palavras_chave.get(
            "investir",
            []
        )
    )

    if quer_investimento and perfil_detectado is None:
        perfil_detectado = perfil_cliente

    # ========================================================
    # 7) Produtos pelo perfil
    # ========================================================

    if (perfil_detectado and perfil_negado is None):

        risco_alvo = risco_por_perfil[
            perfil_detectado
        ]

        produtos_perfil = [

            p["nome"]

            for p in produtos

            if p["risco"] == risco_alvo
        ]

        if produtos_perfil:

            if perfil_detectado != perfil_cliente:

                resposta_final.append(
                    f"Atenção: seu perfil cadastrado é "
                    f"'{perfil_cliente}', mas você solicitou "
                    f"informações para um perfil "
                    f"'{perfil_detectado}'.\n"
                    "Os produtos abaixo possuem um nível "
                    "de risco diferente daquele "
                    "habitualmente recomendado para você."
                    + "\n"
                )

            random.shuffle(produtos_perfil)

            resposta_final.append(
                f"Investimentos para o perfil "
                f"{perfil_detectado} são:\n"
                + "\n".join(
                    f"- {p}"
                    for p in sorted(produtos_perfil[:3])
                )
                + "\n"
            )

    # ========================================================
    # 7.1) Perfil negado
    # ========================================================

    if perfil_negado == perfil_cliente:

        resposta_final.append(
            "Seu perfil é "
            f"'{perfil_cliente}', e você comentou de evitar "
            "produtos para o seu perfil."
        )

    elif perfil_negado:
        resposta_final.append(
            f"Entendi que você prefere evitar "
            f"investimentos com perfil '{perfil_negado}'."
        )

        sugestoes = []
        if (
            perfil_negado == "arrojado"
            and perfil_cliente == "moderado"
        ):
            riscos = ["medio", "baixo"]

        elif (
            perfil_negado == "moderado"
            and perfil_cliente == "conservador"
        ):
            riscos = ["baixo"]

        else:
            riscos = [risco_por_perfil[perfil_cliente]]

        for risco in riscos:

            produtos_risco = [

                p["nome"]

                for p in produtos

                if p["risco"] == risco

            ][:3]

            sugestoes.extend(produtos_risco)

        sugestoes = list(dict.fromkeys(sugestoes))

        resposta_final.append(
            "Talvez estas alternativas façam mais sentido:\n"
            + "\n".join(
                f"- {produto}"
                for produto in sugestoes
            )
        )

    # ========================================================
    # 8) Sobre Produtos Financeiros
    # ========================================================

    assuntos = detectar_chaves(
        pergunta_normalizada,
        tokens,
        contexto.palavras_chave_produtos
    )

    assunto_detectado = assuntos[0] if assuntos else None

    if assunto_detectado: #and not resposta_final:
        sugestoes = chave_sugestoes.get(assunto_detectado, [])
        sugestoes = random.sample(sugestoes, 2) if sugestoes else ""

        produtos_tipo = obter_produtos_por_tipo(
                assunto_detectado
            )

        produtos_tipo = [
            p["nome"]
            for p in produtos_tipo
        ]

        if produtos_tipo:
            random.shuffle(produtos_tipo)

        resposta_final.append(
            "\n".join(f"{s}" for s in sugestoes[:2]
            )
        )

        resposta_final.append(
            "\n".join(f"- {p}" for p in (produtos_tipo[:5])
            )
        )

    # ========================================================
    # 9) Sugestões acumuladas
    # ========================================================

    if not quer_suporte and not quer_ajuda:
        sugestoes = []

        for chave, termos in contexto.palavras_chave.items():

            encontrou_chave = False

            for termo in termos:

                termo_busca = termo.lower()

                for indice, token in enumerate(tokens):

                    if token != termo_busca:
                        continue

                    # ignora se estiver negado
                    if termo_negado(tokens, indice):
                        continue

                    encontrou_chave = True
                    break

                if encontrou_chave:
                    break

            if not encontrou_chave:
                continue

            # chave direta
            if chave in contexto.chave_sugestoes:

                sugestoes.extend(
                    contexto.chave_sugestoes[chave]
                )

        # remove duplicidades
        sugestoes = list(dict.fromkeys(sugestoes))

        if sugestoes and not assunto_detectado:

            random.shuffle(sugestoes)

            resposta_final.append(
                "Sugestões:\n"
                + "\n".join(
                    f"- {s}"
                    for s in sugestoes[:2]
                )
            )

    # ========================================================
    # 10) Fallback
    # ========================================================

    #return obter_resposta(resposta_final, chave_sugestoes)

    if resposta_final:

        return "\n".join(resposta_final)

    return "Sinto muito, mas não tenho essa informação detalhada no momento. Posso ajudar com suas metas ou sugestões de investimento?"

# ============================================================
# Interação
# ============================================================

def rodar_interacao(dados):

    print(
        "Finassist: Olá! "
        "Sou seu assistente financeiro pessoal."
    )

    encontrados = []

    while True:

      if len(encontrados) == 0:
        print("\nClientes cadastrados:")

        for p in sorted(
            contexto.perfis,
            key=lambda x: x["nome"]
        ):

          print(f"- {p['nome']}")

      nome = input(
          "\nDigite o nome ou sobrenome "
          "do cliente ('FIM' para sair): "
      ).strip()

      if nome.lower() == "fim":
          print()
          print("Encerrando Finassist ...")
          return

      encontrados = [
          p
          for p in contexto.perfis
          if nome.lower()
          in p["nome"].lower()
      ]

      if len(encontrados) == 0:
          print()
          print("Nenhum cliente encontrado.")

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
              print()
              print(f"Finalizando atendimento para {perfil['nome']} ...")
              encontrados = []
              break

          resposta = motor_finassist(perfil, pergunta, dados)

          print(
              "\nFinassist:"
          )

          print(resposta)

# ============================================================
# Main
# ============================================================

if __name__ == "__main__":

    cls()

    dados = carregar_dados()

    inicializar_contexto(dados)

    #perfis = dados["perfis"]
    #produtos = dados["produtos"]
    #transacoes = dados["transacoes"]
    #historico = dados["historico"]  
    #palavras_chave = dados["palavras_chave"]
    #chave_sugestoes = dados["chave_sugestoes"]

    rodar_interacao(dados)
