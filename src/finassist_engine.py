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
    with open('data/perfis_investidores.json', 'r', encoding='utf-8') as f:
        perfis = json.load(f)
    with open('data/produtos_financeiros.json', 'r', encoding='utf-8') as f:
        produtos = json.load(f)
    # Garantindo o tipo de dado correto para o ID
    transacoes = pd.read_csv('data/transacoes.csv', dtype={'id_cliente': int})
    historico = pd.read_csv('data/historico_atendimento.csv', dtype={'id_cliente': int})
    return perfis, produtos, transacoes, historico

# Carrega os dados
perfis, produtos, transacoes, historico = carregar_dados()

# 2. Motor de inferência (Lógica de resposta do Finassist)
# Agora recebe transacoes_cliente e historico_cliente como parâmetros!
def motor_finassist(perfil, pergunta, transacoes_cliente, historico_cliente):
    pergunta = pergunta.lower()
    
    if "risco" in pergunta or "investir" in pergunta:
        nivel_risco = 'baixo' if not perfil['aceita_risco'] else 'médio/alto'
        sugestao = [p['nome'] for p in produtos if p['risco'] == nivel_risco]
        return f"Como seu perfil é {perfil['perfil_investidor']}, recomendo produtos de risco {nivel_risco}. Sugestões: {', '.join(sugestao)}."
    
    elif "meta" in pergunta:
        metas = perfil['metas']
        return f"Suas metas atuais: " + ", ".join([m['meta'] for m in metas])
    
    elif "gasto" in pergunta or "transação" in pergunta:
        total = transacoes_cliente[transacoes_cliente['tipo'] == 'saida']['valor'].sum()
        return f"Analisei suas transações. Você gastou um total de R$ {total:.2f} recentemente."
    
    else:
        return "Sinto muito, mas não tenho essa informação detalhada no momento."

# 3. Execução da interação
def rodar_interacao():
    print("Finassist: Olá! Sou seu assistente financeiro pessoal.")
    print("Clientes disponíveis:", ", ".join([p['nome'] for p in perfis]))
    
    nome_escolhido = input("\nDigite o nome do cliente para simular: ")
    perfil = next((p for p in perfis if p['nome'].lower() == nome_escolhido.lower()), None)
    
    if perfil:
        # Filtra os dados aqui, logo após identificar o perfil
        transacoes_cliente = transacoes[transacoes['id_cliente'] == perfil['id']]
        historico_cliente = historico[historico['id_cliente'] == perfil['id']]
        
        print(f"\nConectado como: {perfil['nome']} (ID: {perfil['id']})")
        pergunta = input(f"{perfil['nome']}, como posso te ajudar? ")
        
        # Passa os dados filtrados para o motor
        resposta = motor_finassist(perfil, pergunta, transacoes_cliente, historico_cliente)
        print(f"\nFinassist: {resposta}")
    else:
        print("Cliente não encontrado.")

# --- Rodar ---
rodar_interacao()
