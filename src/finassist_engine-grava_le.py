## Para simulação utilizando uma interface simples com Streamlit, é utilizado o app.py
## Versão: grava os dados das variáveis em arquivos na pasta 'data/', lê esses dados e inicia a simulação do Agente.

import csv
import json
import pandas as pd
import random
import re

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
# Geração dos arquivos de dados na pasta "data"
# ============================================================

def gerar_dados():
    # Cria a pasta 'data/' se não existir
    os.makedirs("data", exist_ok=True)

    # Dados do arquivo historico_atendimento.csv
    dados_historico = [
        ["id_cliente","data","canal","tema","resumo","resolvido"],
        [1,"2025-09-01","chat","CDB","Explicação sobre impostos no CDB","sim"],
        [2,"2025-09-05","telefone","App","Erro de login resolvido","sim"],
        [3,"2025-09-10","chat","Tesouro","Dúvida sobre taxa de custódia","sim"],
        [4,"2025-09-15","email","Investimento","Consulta sobre LCI","sim"],
        [5,"2025-09-15","chat","CDB","Cliente perguntou sobre rentabilidade e prazos","sim"],
        [4,"2025-09-22","telefone","Problema no app","Erro ao visualizar extrato foi corrigido","sim"],
        [3,"2025-10-01","chat","Tesouro Selic","Cliente pediu explicação sobre o funcionamento do Tesouro Direto","sim"],
        [2,"2025-10-01","chat","Metas","Ajuste de meta de reserva","sim"],
        [1,"2025-10-05","telefone","Cartão","Bloqueio por suspeita de fraude","sim"],
        [4,"2025-10-10","chat","Fundo","Rentabilidade do multimercado","sim"],
        [2,"2025-10-12","chat","Metas financeiras","Cliente acompanhou o progresso da reserva de emergência","sim"],
        [3,"2025-10-15","chat","Perfil","Atualização de renda mensal","sim"],
        [5,"2025-10-20","email","Documento","Envio de comprovante","sim"],
        [4,"2025-10-25","email","Atualização cadastral","Cliente atualizou e-mail e telefone","sim"],
        [2,"2025-10-25","chat","Ações","Dúvida sobre volatilidade","sim"],
        [1,"2025-11-01","telefone","Investimento","Resgate antecipado","não"],
        [3,"2025-11-05","chat","Metas","Configuração de débito automático","sim"]
    ]

    # Caminho do arquivo
    arquivo = "data/historico_atendimento.csv"

    # Gravação dos dados
    with open(arquivo, mode="w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerows(dados_historico)

    # Caminho do arquivo
    arquivo_json = "data/perfil_investidor.json"

    # Dados do arquivo
    perfil_investidor = [
        {
            "id": 1,
            "nome": "João Silva",
            "idade": 32,
            "profissao": "Analista de Sistemas",
            "renda_mensal": 5000,
            "perfil_investidor": "moderado",
            "objetivo_principal": "Construir reserva de emergência",
            "patrimonio_total": 15000,
            "reserva_emergencia_atual": 10000,
            "aceita_risco": False,
            "metas": [
                {"meta": "Completar reserva de emergência", "valor_necessario": 15000, "prazo": "2026-06"},
                {"meta": "Entrada do apartamento", "valor_necessario": 50000, "prazo": "2027-12"}
            ]
        },
        {
            "id": 2,
            "nome": "Maria Souza",
            "idade": 25,
            "profissao": "Designer",
            "renda_mensal": 3000,
            "perfil_investidor": "conservador",
            "objetivo_principal": "Viagem internacional",
            "patrimonio_total": 5000,
            "reserva_emergencia_atual": 2000,
            "aceita_risco": False,
            "metas": [
                {"meta": "Viagem para Europa", "valor_necessario": 12000, "prazo": "2026-12"}
            ]
        },
        {
            "id": 3,
            "nome": "Carlos Mendes",
            "idade": 45,
            "profissao": "Gerente de Projetos",
            "renda_mensal": 12000,
            "perfil_investidor": "arrojado",
            "objetivo_principal": "Aposentadoria antecipada",
            "patrimonio_total": 250000,
            "reserva_emergencia_atual": 50000,
            "aceita_risco": True,
            "metas": [
                {"meta": "Aposentadoria FIRE", "valor_necessario": 1000000, "prazo": "2035-01"},
                {"meta": "Intercâmbio filhos", "valor_necessario": 80000, "prazo": "2028-05"}
            ]
        },
        {
            "id": 4,
            "nome": "Ana Oliveira",
            "idade": 35,
            "profissao": "Advogada",
            "renda_mensal": 7500,
            "perfil_investidor": "moderado",
            "objetivo_principal": "Quitação de dívidas",
            "patrimonio_total": 20000,
            "reserva_emergencia_atual": 5000,
            "aceita_risco": False,
            "metas": [
                {"meta": "Quitação Financiamento", "valor_necessario": 30000, "prazo": "2027-01"}
            ]
        },
        {
            "id": 5,
            "nome": "Pedro Lima",
            "idade": 30,
            "profissao": "Engenheiro Civil",
            "renda_mensal": 4500,
            "perfil_investidor": "conservador",
            "objetivo_principal": "Compra de veículo",
            "patrimonio_total": 12000,
            "reserva_emergencia_atual": 8000,
            "aceita_risco": False,
            "metas": [
                {"meta": "Veículo seminovo", "valor_necessario": 40000, "prazo": "2026-10"}
            ]
        }
    ]

    # Gravação dos dados
    with open(arquivo_json, mode="w", encoding="utf-8") as f:
        json.dump(perfil_investidor, f, ensure_ascii=False, indent=4)

    # Caminho do arquivo
    arquivo_json = "data/produtos_financeiros.json"

    # Dados do arquivo
    produtos_financeiros = [
        {
            "nome": "Tesouro Selic",
            "categoria": "renda_fixa",
            "risco": "baixo",
            "rentabilidade": "100% da Selic",
            "aporte_minimo": 30.00,
            "indicado_para": "Reserva de emergência e iniciantes"
        },
        {
            "nome": "CDB Liquidez Diária",
            "categoria": "renda_fixa",
            "risco": "baixo",
            "rentabilidade": "102% do CDI",
            "aporte_minimo": 100.00,
            "indicado_para": "Quem busca segurança com rendimento diário"
        },
        {
            "nome": "LCI/LCA",
            "categoria": "renda_fixa",
            "risco": "baixo",
            "rentabilidade": "95% do CDI",
            "aporte_minimo": 1000.00,
            "indicado_para": "Quem pode esperar 90 dias (isento de IR)"
        },
        {
            "nome": "Fundo Multimercado",
            "categoria": "fundo",
            "risco": "medio",
            "rentabilidade": "CDI + 2%",
            "aporte_minimo": 500.00,
            "indicado_para": "Perfil moderado que busca diversificação"
        },
        {
            "nome": "Fundo de Ações",
            "categoria": "fundo",
            "risco": "alto",
            "rentabilidade": "Variável",
            "aporte_minimo": 100.00,
            "indicado_para": "Perfil arrojado com foco no longo prazo"
        },
        {
            "nome":"Tesouro Selic 2029",
            "categoria":"renda_fixa",
            "risco":"baixo",
            "rentabilidade":"100% Selic",
            "aporte_minimo":30.00,
            "indicado_para":"Reserva de emergência"
        },
        {
            "nome":"CDB Pós-Fixado 110%",
            "categoria":"renda_fixa",
            "risco":"baixo",
            "rentabilidade":"110% CDI",
            "aporte_minimo":500.00,
            "indicado_para":"Curto/Médio prazo"
        },
        {
            "nome":"LCI Direto 95%",
            "categoria":"renda_fixa",
            "risco":"baixo",
            "rentabilidade":"95% CDI (Isento IR)",
            "aporte_minimo":1000.00,
            "indicado_para":"Prazo mínimo de 90 dias"
        },
        {
            "nome":"Fundo Multimercado Agressivo",
            "categoria":"fundo",
            "risco":"medio",
            "rentabilidade":"CDI + 3.5%",
            "aporte_minimo":200.00,
            "indicado_para":"Diversificação moderada"
        },
        {
            "nome":"Fundo de Ações Tech",
            "categoria":"fundo",
            "risco":"alto",
            "rentabilidade":"Variável",
            "aporte_minimo":100.00,
            "indicado_para":"Longuíssimo prazo"
        },
        {
            "nome":"ETF S&P 500",
            "categoria":"fundo",
            "risco":"alto",
            "rentabilidade":"Dólar + Variação Global",
            "aporte_minimo":50.00,
            "indicado_para":"Exposição internacional"
        }
    ]

    # Gravação dos dados
    with open(arquivo_json, mode="w", encoding="utf-8") as f:
        json.dump(produtos_financeiros, f, ensure_ascii=False, indent=4)


    # Caminho do arquivo
    arquivo = "data/transacoes.csv"

    # Dados do arquivo historico_atendimento.csv
    dados_historico = [
        ["id_cliente","data","canal","tema","resumo","resolvido"],
        [1,"2025-09-01","chat","CDB","Explicação sobre impostos no CDB","sim"],
        [2,"2025-09-05","telefone","App","Erro de login resolvido","sim"],
        [3,"2025-09-10","chat","Tesouro","Dúvida sobre taxa de custódia","sim"],
        [4,"2025-09-15","email","Investimento","Consulta sobre LCI","sim"],
        [5,"2025-09-15","chat","CDB","Cliente perguntou sobre rentabilidade e prazos","sim"],
        [4,"2025-09-22","telefone","Problema no app","Erro ao visualizar extrato foi corrigido","sim"],
        [3,"2025-10-01","chat","Tesouro Selic","Cliente pediu explicação sobre o funcionamento do Tesouro Direto","sim"],
        [2,"2025-10-01","chat","Metas","Ajuste de meta de reserva","sim"],
        [1,"2025-10-05","telefone","Cartão","Bloqueio por suspeita de fraude","sim"],
        [4,"2025-10-10","chat","Fundo","Rentabilidade do multimercado","sim"],
        [2,"2025-10-12","chat","Metas financeiras","Cliente acompanhou o progresso da reserva de emergência","sim"],
        [3,"2025-10-15","chat","Perfil","Atualização de renda mensal","sim"],
        [5,"2025-10-20","email","Documento","Envio de comprovante","sim"],
        [4,"2025-10-25","email","Atualização cadastral","Cliente atualizou e-mail e telefone","sim"],
        [2,"2025-10-25","chat","Ações","Dúvida sobre volatilidade","sim"],
        [1,"2025-11-01","telefone","Investimento","Resgate antecipado","não"],
        [3,"2025-11-05","chat","Metas","Configuração de débito automático","sim"]
    ]

    # Gravação dos dados
    with open(arquivo, mode="w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerows(dados_historico)

    # Caminho do arquivo
    arquivo_json = "data/palavras_chave.json"

    # Dados do arquivo
    palavras_chave = {
    "meta": ["meta", "objetivo", "planejamento", "alvo"],
    "seguro": ["seguro", "poupança", "poupanca", "selic", "lci/lca", "lci_lca"],
    "poupanca": ["poupança", "guardar dinheiro", "economizar", "poupar"],
    "acoes": ["ações", "arriscar", "bolsa", "mercado", "volatilidade"],
    "tesouro": ["tesouro", "selic", "direto", "título público"],
    "cdb": ["cdb", "certificado de depósito", "liquidez diária"],
    "lci_lca": ["lci", "lca", "lci/lca", "letra de crédito", "imobiliário", "agrícola"],
    "fundo_multimercado": ["multimercado", "diversificação"],
    "fundo_acoes": ["fundo de ações", "ações tech", "ações", "variável"],
    "etf": ["etf", "s&p", "internacional", "global"],
    "investir": ["investir", "investimento", "aplicar", "aplicação"]
    }

    # Gravação dos dados
    with open(arquivo_json, mode="w", encoding="utf-8") as f:
        json.dump(palavras_chave, f, ensure_ascii=False, indent=4)


    # Caminho do arquivo
    arquivo_json = "data/chave_sugestoes.json"

    # Dados do arquivo
    palavras_chave_sugestoes = {
    "poupanca": [
        "Tesouro Selic é ideal para reserva de emergência.",
        "CDB Liquidez Diária é uma alternativa à poupança tradicional."
    ],
    "acoes": [
        "Fundo de Ações é indicado para perfil arrojado.",
        "ETF S&P 500 dá exposição internacional."
    ],
    "tesouro": [
        "Tesouro Selic é ideal para reserva de emergência.",
        "Tesouro IPCA protege contra inflação em longo prazo."
    ],
    "cdb": [
        "CDB Liquidez Diária é indicado para segurança e liquidez.",
        "CDB Pós-Fixado 110% oferece maior rentabilidade."
    ],
    "lci_lca": [
        "LCI/LCA são isentos de IR e indicados para médio prazo.",
        "LCI Direto 95% exige prazo mínimo de 90 dias."
    ],
    "fundo_multimercado": [
        "Fundo Multimercado é indicado para perfil moderado.",
        "Fundo Multimercado Agressivo oferece diversificação com maior risco."
    ],
    "fundo_acoes": [
        "Fundo de Ações é indicado para longo prazo.",
        "Fundo de Ações Tech é voltado para perfil arrojado."
    ],
    "etf": [
        "ETF S&P 500 oferece exposição internacional.",
        "Ideal para diversificação global."
    ],
    "seguro": [
        "Tesouro Selic é ideal para reserva de emergência.",
        "CDB Liquidez Diária é indicado para segurança e liquidez.",
        "LCI/LCA são isentos de IR e indicados para médio prazo."
    ]
    }

    # Gravação dos dados
    with open(arquivo_json, mode="w", encoding="utf-8") as f:
        json.dump(palavras_chave_sugestoes, f, ensure_ascii=False, indent=4)

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
    """
    Remove pontuação e devolve uma lista de palavras.
    """

    return re.findall(
        r'\b[\w/]+\b',
        texto.lower()
    )

NEGACOES = {
    "dispensar",
    "dispenso",
    "forma alguma",
    "evitar",
    "jamais",
    "nada",
    "não",
    "nao",
    "nem",
    "nem pensar",
    "nem quero",
    "nem sequer",
    "nunca"}

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

        if token in NEGACOES:
            return True

    # bigramas
    for i in range(len(trecho) - 1):

        expressao = f"{trecho[i]} {trecho[i + 1]}"

        if expressao in NEGACOES:
            return True

    return False

mapa_risco_perfil = {
    "baixo": "conservador",
    "medio": "moderado",
    "alto": "arrojado"
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

    pergunta_lower = pergunta.lower()

    tokens = tokenizar(pergunta)

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
    # 2) Histórico, Transações e Gastos
    # ========================================================

    quer_ultimo_atendimento = any(
        termo in pergunta_lower
        for termo in [
            "último atendimento",
            "ultimo atendimento",
            "último contato",
            "ultimo contato",
            "atendimento mais recente",
            "atendimento recente"
        ]
    )

    if quer_ultimo_atendimento:

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
                f"{ultimo['data']} via {ultimo['canal']}.\n"
                f"Tema: {ultimo['tema']}.\n"
                f"Resumo: {ultimo['resumo']}."
            )


    quer_historico = any(
        termo in pergunta_lower
        for termo in [
            "histórico de atendimento",
            "historico de atendimento",
            "meu histórico",
            "meu historico",
            "todos os atendimentos",
            "listar atendimentos"
        ]
    )

    if quer_historico:

        hist = historico[
            historico["id_cliente"] == perfil["id"]
        ]

        if not hist.empty:

            hist = hist.sort_values(
                "data",
                ascending=False
            )

            linhas = []

            for _, atendimento in hist.iterrows():

                linhas.append(
                    f"- {atendimento['data']} | "
                    f"{atendimento['tema']} | "
                    f"{atendimento['canal']}"
                )

            resposta_final.append(
                "Seu histórico de atendimento:\n"
                + "\n".join(linhas)
            )


    quer_transacoes = any(
        termo in pergunta_lower
        for termo in [
            "transação",
            "transações",
            "transacao",
            "transacoes",
            "movimentação",
            "movimentações",
            "movimentacao",
            "movimentacoes"
        ]
    )

    if quer_transacoes:

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

            resposta_final.append(
                "Suas últimas transações foram:\n"
                + "\n".join(linhas)
            )

    quer_gastos = any(
        termo in pergunta_lower
        for termo in [
            "quanto gastei",
            "total de despesas",
            "despesas"
        ]
    )

    if quer_gastos:

        saidas = transacoes[
            (transacoes["id_cliente"] == perfil["id"])
            &
            (transacoes["tipo"] == "saida")
        ]

        total = saidas["valor"].sum()

        resposta_final.append(
            f"Suas despesas totalizam "
            f"R$ {formatar_moeda(total)}."
        )

    quer_categoria = any(
        termo in pergunta_lower
        for termo in [
            "gastando mais",
            "maior despesa",
            "categoria"
        ]
    )

    if quer_categoria:

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

            resposta_final.append(
                f"Sua maior despesa está na categoria "
                f"'{categoria}', totalizando "
                f"R$ {formatar_moeda(valor)}."
            )
    
    # ========================================================
    # 3) Riscos
    # ========================================================

    if (
        "risco" in pergunta_lower
        or "volatilidade" in pergunta_lower
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

    perfis = dados["perfis"]
    produtos = dados["produtos"]
    transacoes = dados["transacoes"]
    historico = dados["historico"]  
    palavras_chave = dados["palavras_chave"]
    chave_sugestoes = dados["chave_sugestoes"]

    rodar_interacao(dados)
