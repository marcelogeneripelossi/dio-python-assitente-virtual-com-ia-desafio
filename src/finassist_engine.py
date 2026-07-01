## Código a ser utilizado no Colab. No Notebook são gerados os arquivos de dados para utilização da simulação do Agente.
## Para simulação utilizando uma interface simples com Streamlit, é utilizado o app.py
## Versão: lê os dados já gravados em arquivos na pasta 'data/'

import csv
import json
import pandas as pd
import random
import re
import unicodedata

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
# Contexto global
# ==========================================================

perfis = None
produtos = None
transacoes = None
historico = None
palavras_chave = None
chave_sugestoes = None

# ==========================================================
# Constantes
# ==========================================================

mapa_risco_perfil = {
    "baixo": "conservador",
    "medio": "moderado",
    "alto": "arrojado"
}

negacoes = {
    "dispensar",
    "dispenso",
    "forma alguma",
    "evitar",
    "jamais",
    "nada",
    "nao",
    "nem",
    "nem pensar",
    "nem quero",
    "nem sequer",
    "nunca"}

perfil_sinonimos = {
    "arriscado": "arrojado",
    "risco": "arrojado",
    "acoes": "arrojado",
    "ação": "arrojado",
    "acao": "arrojado",
    "bolsa": "arrojado",

    "seguro": "conservador",
    "segurança": "conservador",

    "equilibrado": "moderado"
}

perfil_tipos = [
        "conservador",
        "conservadora",
        "conservadores",
        "conservadoras",
        "moderado",
        "moderada",
        "moderados",
        "moderadas",
        "arrojado",
        "arrojada",
        "arrojados",
        "arrojadas"
    ]

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

    produtos = dados["produtos"]
    transacoes = dados["transacoes"]
    historico = dados["historico"]
    palavras_chave = dados["palavras_chave"]
    chave_sugestoes = dados["chave_sugestoes"]
    perfis = dados["perfis"]

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

        if token in negacoes:
            return True

    # bigramas
    for i in range(len(trecho) - 1):

        expressao = f"{trecho[i]} {trecho[i + 1]}"

        if expressao in negacoes:
            return True

    return False

def detectar_intencao(pergunta, chave):

    pergunta_normalizada = normalizar_texto(
        pergunta
    )

    termos = palavras_chave.get(
        chave,
        []
    )

    return any(
        normalizar_texto(termo)
        in pergunta_normalizada
        for termo in termos
    )

# ============================================================
# Motor do Finassist 
# ============================================================
# ===================================
# Métodos do Motor (início)
# ===================================

def obter_gastos_maior_categoria(perfil):

        saidas = transacoes[
            (transacoes["id_cliente"] == perfil["id"])
            &
            (transacoes["tipo"] == "saida")
        ]

        if not saidas.empty:

            resumo = (
                saidas
                .groupby("categoria")["valor"]
                .sum()
            )

            categoria = resumo.idxmax()

            valor = resumo.max()

            return (
                f"Sua maior despesa está na categoria "
                f"'{categoria}', totalizando "
                f"R$ {formatar_moeda(valor)}."
            )

def obter_gastos(perfil):
        saidas = transacoes[
            (transacoes["id_cliente"] == perfil["id"])
            &
            (transacoes["tipo"] == "saida")
        ]

        total = saidas["valor"].sum()

        return(
            f"Suas despesas totalizam "
            f"R$ {formatar_moeda(total)}."
        )

def obter_historico(perfil):
    hist = historico[
        historico["id_cliente"] == perfil["id"]
    ]

    if hist.empty:
        return "Você não possui atendimentos registrados."

    hist = hist.sort_values("data", ascending=False)    #.head(5)

    linhas = []

    for _, atendimento in hist.iterrows():

        linhas.append(
            f"- {atendimento['data']} | "
            f"{atendimento['tema']} | "
            f"{atendimento['canal']}"
        )

    return (
        "Seu histórico de atendimento:\n"
        + "\n".join(linhas)
    )

def obter_metas(perfil):
    metas = perfil.get("metas", [])

    if not metas:
        return ("Você não possui metas cadastradas.")

    if metas:
        texto_metas = []

        for meta in metas:
            texto_metas.append(
                f"- {meta['meta']} "
                f"(R$ {formatar_moeda(meta['valor_necessario'])} "
                f"até {meta['prazo']})"
            )

        return (
            "Suas metas atuais são:\n"
            + "\n".join(texto_metas)
        )

def obter_transacoes(perfil):
        trans = transacoes[
            transacoes["id_cliente"] == perfil["id"]
        ]

        if not trans.empty:

            ultimas = (
                trans
                .sort_values("data", ascending=False)
                .head(3)
            )

            linhas = []

            for _, t in ultimas.iterrows():

                linhas.append(
                    f"- {t['data']} | "
                    f"{t['descricao']} | "
                    f"R$ {formatar_moeda(t['valor'])}"
                )

            return (
                "Suas últimas transações foram:\n"
                + "\n".join(linhas)
            )


def obter_ultimo_atendimento(perfil):
    hist = historico[
        historico["id_cliente"] == perfil["id"]
    ]

    if hist.empty:
        return "Você não possui atendimentos registrados."

    ultimo = (
        hist
        .sort_values("data")
        .iloc[-1]
    )

    return (
        f"Seu último atendimento foi em "
        f"{ultimo['data']} via {ultimo['canal']}.\n"
        f"Tema: {ultimo['tema']}.\n"
        f"Resumo: {ultimo['resumo']}."
    )

# ===================================
# Métodos do Motor (fim)
# ===================================

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
        "meta"
    )

    if quer_metas:
        resposta = obter_metas(perfil)
        resposta_final.append(resposta)

    # ========================================================
    # 2) Histórico, Transações e Gastos
    # ========================================================

    #=====================
    # Último atendimento
    #=====================

    quer_ultimo_atendimento = detectar_intencao(
        pergunta_normalizada,
        "ultimo_atendimento"
    )

    if quer_ultimo_atendimento:
        resposta = obter_ultimo_atendimento(perfil)
        resposta_final.append(resposta)

    #=====================
    # Histórico de atendimento
    #=====================

    quer_historico = detectar_intencao(
        pergunta_normalizada,
        "historico_atendimento"
    )

    if quer_historico:
        resposta = obter_historico(perfil)
        resposta_final.append(resposta)

    
    #=====================
    # Últimas transações, gastos e categoria de maior gasto
    #=====================

    #=======
    # Transações
    #=======

    quer_transacoes = detectar_intencao(
        pergunta_normalizada,
        "transacoes"
    )

    if quer_transacoes:
        resposta = obter_transacoes(perfil)
        resposta_final.append(resposta)


    #=======
    # Gastos
    #=======
    
    quer_gastos = detectar_intencao(
        pergunta_normalizada,
        "gastos"
    )

    if quer_gastos:
        resposta = obter_gastos(perfil)
        resposta_final.append(resposta)

    #=======
    # Categoria de maior gasto
    #=======

    quer_categoria_maior_gasto = detectar_intencao(
        pergunta_normalizada,
        "categoria"
    )

    if quer_categoria_maior_gasto:
        resposta = obter_gastos_maior_categoria(perfil)
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
                    f"(perfil {mapa_risco_perfil[risco_json]}): "
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

    for termo in perfil_tipos:
        termo_busca = termo.lower()

        for indice, token in enumerate(tokens):
            token_normalizado = token.lower()

            # trata plural simples
            if token_normalizado.endswith("es") or token_normalizado.endswith("as"):
                token_normalizado = token_normalizado[:-2] 
            elif token_normalizado.endswith("s"):
                token_normalizado = token_normalizado[:-1]

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

        for termo, perfil_associado in perfil_sinonimos.items():

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

    for chave, termos in palavras_chave.items():

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
        if chave in chave_sugestoes:

            sugestoes.extend(
                chave_sugestoes[chave]
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
            perfis,
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
          for p in perfis
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
