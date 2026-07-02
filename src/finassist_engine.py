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
    detectar_intencao,
    normalizar_perfil,
    normalizar_texto,
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
    global produtos
    global transacoes
    global historico
    global palavras_chave
    global chave_sugestoes
    global perfis

    contexto.produtos = dados["produtos"]
    contexto.transacoes = dados["transacoes"]
    contexto.historico = dados["historico"]
    contexto.palavras_chave = dados["palavras_chave"]
    contexto.chave_sugestoes = dados["chave_sugestoes"]
    contexto.perfis = dados["perfis"]

    produtos = contexto.produtos
    transacoes = contexto.transacoes
    historico = contexto.historico
    palavras_chave = contexto.palavras_chave
    chave_sugestoes = contexto.chave_sugestoes
    perfis = contexto.perfis

# ============================================================
# Carregamento dos dados
# ============================================================

def carregar_dados():
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
            "chave_sugestoes.json"
        ),
        encoding="utf-8") as f:
        chave_sugestoes = json.load(f)
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
        "perfis": perfis,
        "produtos": produtos,
        "transacoes": transacoes,
        "historico": historico,
        "palavras_chave": palavras_chave,
        "chave_sugestoes": chave_sugestoes
    }

# ============================================================
# Motor do Finassist 
# ============================================================

def motor_finassist(perfil, pergunta, dados):

    pergunta_normalizada = normalizar_texto(pergunta)

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

    # ========================================================
    # 1) Metas
    # ========================================================

    quer_metas = detectar_intencao(
        pergunta_normalizada,
        tokens,
        "meta"
    )

    if quer_metas:
        resposta = consultas_cliente.obter_metas(perfil)
        resposta_final.append(resposta)

    # ========================================================
    # 2) Histórico, Transações e Gastos
    # ========================================================

    #=====================
    # Último atendimento
    #=====================

    quer_ultimo_atendimento = detectar_intencao(
        pergunta_normalizada,
        tokens,
        "ultimo_atendimento"
    )

    if quer_ultimo_atendimento:
        resposta = consultas_cliente.obter_ultimo_atendimento(perfil)
        resposta_final.append(resposta)

    #=====================
    # Histórico de atendimento
    #=====================

    quer_historico = detectar_intencao(
        pergunta_normalizada,
        tokens,
        "historico_atendimento"
    )

    if quer_historico:
        resposta = consultas_cliente.obter_historico(perfil)
        resposta_final.append(resposta)

    
    #=====================
    # Últimas transações, gastos e categoria de maior gasto
    #=====================

    #=======
    # Transações
    #=======

    quer_transacoes = detectar_intencao(
        pergunta_normalizada,
        tokens,
        "transacoes"
    )

    if quer_transacoes:
        resposta = consultas_cliente.obter_transacoes(perfil)
        resposta_final.append(resposta)


    #=======
    # Gastos
    #=======
    
    quer_gastos = detectar_intencao(
        pergunta_normalizada,
        tokens,
        "gastos"
    )

    if quer_gastos:
        resposta = consultas_cliente.obter_gastos(perfil)
        resposta_final.append(resposta)

    #=======
    # Categoria de maior gasto
    #=======

    quer_categoria_maior_gasto = detectar_intencao(
        pergunta_normalizada,
        tokens,
        "categoria"
    )

    if quer_categoria_maior_gasto:
        resposta = consultas_cliente.obter_gastos_maior_categoria(perfil)
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
    # 5) Meu perfil
    # ========================================================

    if (perfil_detectado is None and "perfil" in pergunta_normalizada):
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
                )

            resposta_final.append(
                f"Investimentos para o perfil "
                f"{perfil_detectado} são:\n"
                + "\n".join(
                    f"- {p}"
                    for p in produtos_perfil
                )
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
    # 8) Sugestões acumuladas
    # ========================================================

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
