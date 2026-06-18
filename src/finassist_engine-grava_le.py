## Para simulação utilizando uma interface simples com Streamlit, é utilizado o app.py
## Versão: grava os dados das variáveis em arquivos na pasta 'data/' e lê esses dados para a simulação do Agente.

import os

import csv
import json
import pandas as pd

import subprocess

def cls():
    comando = 'cls' if os.name == 'nt' else 'clear'
    subprocess.run (comando, shell = True)


# 0. Geração dos arquivos de dados na pasta "data"
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
    "poupanca": ["poupança", "guardar dinheiro", "economizar", "poupar"],
    "acoes": ["ações", "bolsa", "mercado", "volatilidade"],
    "tesouro": ["tesouro", "selic", "direto", "título público"],
    "cdb": ["cdb", "certificado de depósito", "liquidez diária"],
    "lci_lca": ["lci", "lca", "lci/lca", "letra de crédito", "imobiliário", "agrícola"],
    "fundo_multimercado": ["multimercado", "diversificação", "moderado"],
    "fundo_acoes": ["fundo de ações", "ações tech", "ações", "variável"],
    "etf": ["etf", "s&p", "internacional", "global"],
    "risco": ["risco", "perigo", "incerteza"],
    "investir": ["investir", "investimento", "aplicar", "aplicação"]
    }

    # Gravação dos dados
    with open(arquivo_json, mode="w", encoding="utf-8") as f:
        json.dump(palavras_chave, f, ensure_ascii=False, indent=4)


    # Caminho do arquivo
    arquivo_json = "data/chave_sugestoes.json"

    # Dados do arquivo
    palavras_chave_sugestoes = {
    "risco": [
        "Tesouro Selic é indicado para quem busca baixo risco.",
        "CDB Liquidez Diária oferece segurança com rendimento diário."
    ],
    "investir": [
        "Tesouro Selic 2029 é uma opção segura.",
        "CDB Pós-Fixado 110% pode ser usado para curto/médio prazo."
    ],
    "meta": [
        "Planeje suas metas com Tesouro IPCA para longo prazo.",
        "Use CDB ou LCI/LCA para metas de médio prazo."
    ],
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
    ]
    }

    # Gravação dos dados
    with open(arquivo_json, mode="w", encoding="utf-8") as f:
        json.dump(palavras_chave_sugestoes, f, ensure_ascii=False, indent=4)

# 1. Carregamento dos dados
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


# 2. Motor de inferência (Lógica de resposta do Finassist)
def motor_finassist(perfil, pergunta):
    pergunta = pergunta.lower()

    # Varre o dicionário de palavras-chave
    for chave, termos in palavras_chave.items():
        if any(t in pergunta for t in termos):

            # Tratamento especial para metas do cliente
            if chave == "meta":
                metas = perfil.get("metas", [])
                if metas:
                   return "Suas metas atuais:\n" + "\n".join (
                        [
                            f"- {m['meta']} (R$ {str(f'{m['valor_necessario']:,.2f}').replace(",", "_").replace(".", ",").replace("_", ".")} até {m['prazo']})"
                            for m in metas
                        ]
                    )
                else:
                    return "Você não possui metas cadastradas no momento."
                
            # Busca sugestões dinâmicas
            if chave in chave_sugestoes:
                return f"Sugestões para {chave}: \n" + "\n".join(chave_sugestoes[chave])

    # Caso não encontre correspondência
    return "Sinto muito, mas não tenho essa informação detalhada no momento. Posso ajudar com suas metas ou sugestões de investimento?"

# 3. Execução da interação (Simulação)
def rodar_interacao():
    print("Finassist: Olá! Sou seu assistente financeiro pessoal.")
    print("Clientes cadastrados:")
    for p in sorted(perfis, key=lambda x: x['nome']):
      print(f"- {p['nome']}")    

    # Validação simples
    while True:
        nome_escolhido = input("\nDigite o nome ou sobrenome do cliente: ").strip().lower()

        if nome_escolhido.lower() == 'fim':
          print("Encerrando ...")
          return

        # Busca todos os perfis que contenham o trecho digitado
        resultados = [p for p in perfis if nome_escolhido in p["nome"].lower()]

        if not resultados:
            print("Nenhum cliente encontrado. Tente novamente ou 'FIM' para encerrar.")
            continue

        if len(resultados) > 1:
            print("\nForam encontrados vários perfis:")
            for p in sorted(resultados, key=lambda x: x['nome']):
                print(f"- {p['nome']}")
            print()
            print("Digite novamente para refinar a busca ou 'FIM' para encerrar.")
            continue

        # Se chegou aqui, significa que encontrou apenas 1 perfil
        perfil = resultados[0]
        print(f"\nConectado como: {perfil['nome']} ({perfil['perfil_investidor']})")

        while True:
            pergunta = input(f"{perfil['nome']}, como posso te ajudar? ('FIM' para encerrar.): ")
            if pergunta.lower() == 'fim':
                print("Encerrando ...")
                return
            resposta = motor_finassist(perfil, pergunta)
            print(f"\nFinassist: {resposta}")
            print()
            

# --- Rodar ---
cls()
gerar_dados()
# Carrega os dados na memória
perfis, produtos, transacoes, historico, palavras_chave, chave_sugestoes = carregar_dados()

rodar_interacao()
