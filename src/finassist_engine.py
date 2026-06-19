## Código a ser utilizado no Colab. No Notebook são gerados os arquivos de dados para utilização da simulação do Agente.
## Para simulação utilizando uma interface simples com Streamlit, é utilizado o app.py
## Versão: lê os dados já gravados em arquivos na pasta 'data/'

import csv
import json
import pandas as pd

import os
import subprocess

def cls():
    comando = 'cls' if os.name == 'nt' else 'clear'
    subprocess.run (comando, shell = True)

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
    with open("data/palavras_chave.json", encoding="utf-8") as f:
        palavras_chave = json.load(f)
    with open("data/chave_sugestoes.json", encoding="utf-8") as f:
        chave_sugestoes = json.load(f)
    transacoes = pd.read_csv('data/transacoes.csv')
    historico = pd.read_csv('data/historico_atendimento.csv')
    return perfis, produtos, transacoes, historico, palavras_chave, chave_sugestoes

# 2. Gerais
# Normalização do perfil do investidor
def normalizar_perfil(perfil_investidor: str) -> str:
    perfil_investidor = perfil_investidor.lower().strip()
    mapa = {
        "conservador": "conservador",
        "conservadora": "conservador",
        "moderado": "moderado",
        "moderada": "moderado",
        "arrojado": "arrojado",
        "arrojada": "arrojado"
    }
    return mapa.get(perfil_investidor, perfil_investidor)

# 3. Motor de inferência (Lógica de resposta do Finassist)
def motor_finassist(perfil, pergunta, produtos, palavras_chave, chave_sugestoes):
    pergunta_lower = pergunta.lower()
    perfil_cliente = normalizar_perfil(perfil["perfil_investidor"])
    
    resposta_final = []
    sugestoes_coletadas = []

    # 1. Detecção de Metas
    if any(t in pergunta_lower for t in palavras_chave.get("meta", [])):
        metas = perfil.get("metas", [])
        if metas:
            lista = "\n".join([f"- {m['meta']} (R$ {m['valor_necessario']:,.2f} até {m['prazo']})" for m in metas])
            resposta_final.append(f"Suas metas atuais:\n{lista}")
        else:
            resposta_final.append("Você não possui metas cadastradas no momento.")

    # 2. Detecção de Perfil explícito na pergunta ou padrão do cliente
    perfil_detectado = None
    for p_termo in ["conservador", "conservadora", "moderado", "moderada", "arrojado", "arrojada"]:
        if p_termo in pergunta_lower:
            perfil_detectado = normalizar_perfil(p_termo)
            break
    
    if not perfil_detectado and ("perfil" in pergunta_lower or "meu perfil" in pergunta_lower):
        perfil_detectado = perfil_cliente

    # 3. Coleta de sugestões baseada em palavras-chave
    for chave, termos in palavras_chave.items():
        if any(t in pergunta_lower for t in termos):
            if chave in chave_sugestoes:
                sugestoes_coletadas.extend(chave_sugestoes[chave])

    # 4. Busca de produtos (se perfil detectado ou se o usuário pediu sugestões gerais)
    risco_map = {"conservador": "baixo", "moderado": "medio", "arrojado": "alto"}
    risco_alvo = risco_map.get(perfil_detectado or perfil_cliente)
    
    produtos_filtrados = [p["nome"] for p in produtos if p["risco"] == risco_alvo]
    
    if produtos_filtrados:
        p_nome = perfil_detectado or perfil_cliente
        resposta_final.append(f"Investimentos para o perfil {p_nome}: " + ", ".join(produtos_filtrados))
    
    if sugestoes_coletadas:
        resposta_final.append("Sugestões relacionadas:")
        for sugestao in list(set(sugestoes_coletadas)): # set para evitar duplicatas
            resposta_final.append(f"- {sugestao}")

    return "\n\n".join(resposta_final) if resposta_final else "Sinto muito, mas não tenho essa informação detalhada no momento. Posso ajudar com suas metas ou sugestões de investimento?"

# 4. Execução da interação (Simulação)
def rodar_interacao():
    perfis, produtos, transacoes, historico, palavras_chave, chave_sugestoes = carregar_dados()
    print("Finassist: Olá! Sou seu assistente financeiro pessoal.")
    print("Clientes cadastrados:")
    for p in sorted(perfis, key=lambda x: x['nome']):
      print(f"- {p['nome']}")    

    # Validação simples
    while True:
        nome_escolhido = input("\nDigite o nome do cliente (ou 'fim'): ").strip().lower()
        if nome_escolhido.lower() == 'fim':
          print("Encerrando ...")
          return
        
        # Busca todos os perfis que contenham o trecho digitado
        resultados = [p for p in perfis if nome_escolhido in p["nome"].lower()]
        if not resultados:
            print("Nenhum cliente encontrado. Tente novamente ou 'FIM' para encerrar.")
            continue
        
        perfil = resultados[0]
        print(f"\nConectado como: {perfil['nome']} ({perfil['perfil_investidor']})")

        while True:
            pergunta = input(f"{perfil['nome']}, como posso te ajudar? ('fim'): ")
            if pergunta.lower() == 'fim':
                print("Encerrando ...")
                return
            resposta = motor_finassist(perfil, pergunta, produtos, palavras_chave, chave_sugestoes)
            print(f"\nFinassist: {resposta}\n")
            print()

if __name__ == "__main__":
    cls()
    rodar_interacao()
