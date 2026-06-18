## Código a ser utilizado no Colab. No Notebook são gerados os arquivos de dados para utilização da simulação do Agente.
## Para simulação utilizando uma interface simples com Streamlit, é utilizado o app.py

import json
import pandas as pd

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

# 1. Carregamento dos dados
def carregar_dados():
    with open('data/perfil_investidor.json', 'r', encoding='utf-8') as f:
        perfis = json.load(f)
    with open('data/produtos_financeiros.json', 'r', encoding='utf-8') as f:
        produtos = json.load(f)
    transacoes = pd.read_csv('data/transacoes.csv')
    historico = pd.read_csv('data/historico_atendimento.csv')
    return perfis, produtos, transacoes, historico

# Carrega os dados na memória
perfis, produtos, transacoes, historico = carregar_dados()

# 2. Motor de inferência (Lógica de resposta do Finassist)
def motor_finassist(perfil, pergunta):
    pergunta = pergunta.lower()
    
    # Exemplo de lógica RAG simplificada
    if "risco" in pergunta or "investir" in pergunta:
        nivel_risco = 'baixo' if not perfil['aceita_risco'] else 'médio/alto'
        sugestao = [p['nome'] for p in produtos if p['risco'] == nivel_risco]
        return f"Como seu perfil é {perfil['perfil_investidor']}, recomendo produtos de risco {nivel_risco}. Sugestões: {', '.join(sugestao)}."
    
    elif "meta" in pergunta:
        metas = perfil['metas']
        return f"Suas metas atuais: " + ", ".join([m['meta'] for m in metas])
    
    else:
        return "Sinto muito, mas não tenho essa informação detalhada no momento. Posso ajudar com suas metas ou sugestões de investimento?"

# 3. Execução da interação (Simulação)
def rodar_interacao():
    print("Finassist: Olá! Sou seu assistente financeiro pessoal.")
    print("Clientes cadastrados:", ", ".join([p['nome'] for p in perfis]))
    
    # Validação simples
    while True:
        nome_escolhido = input("\nDigite o nome ou sobrenome do cliente: ").strip().lower()

        if nome_escolhido.lower() == 'fim':
          print("Encerrando ...")
          break

        # Busca todos os perfis que contenham o trecho digitado
        resultados = [p for p in perfis if nome_escolhido in p["nome"].lower()]

        if not resultados:
            print("Nenhum cliente encontrado. Tente novamente ou 'FIM' para encerrar.")
            continue

        if len(resultados) > 1:
            print("\nForam encontrados vários perfis:")
            for p in resultados:
                print(f"- {p['id']}: {p['nome']}")
            print()
            print("Digite novamente para refinar a busca.")
            continue

        # Se chegou aqui, significa que encontrou apenas 1 perfil
        perfil = resultados[0]
        print(f"\nConectado como: {perfil['nome']} ({perfil['perfil_investidor']})")
        pergunta = input(f"{perfil['nome']}, como posso te ajudar? ")
        resposta = motor_finassist(perfil, pergunta)
        print(f"\nFinassist: {resposta}")
        break

# --- Rodar ---
rodar_interacao()
