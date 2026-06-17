import streamlit as st
import pandas as pd
import json

# ==============================================================================
# CONFIGURAÇÃO DA IA (GEMINI)
# ==============================================================================
# NOTA: Para ativar o Gemini, instale a biblioteca com:
# pip install google-generativeai
# Depois, descomente as linhas abaixo e insira sua API Key.

# import google.generativeai as genai
# genai.configure(api_key="SUA_CHAVE_AQUI")
# model = genai.GenerativeModel('gemini-1.5-flash')

USE_GEMINI = False # Mude para True quando descomentar as linhas acima
# ==============================================================================

# 1. Carregamento dos Dados
def carregar_dados():
    perfis = json.load(open('data/perfil_investidor.json'))
    produtos = json.load(open('data/produtos_financeiros.json'))
    transacoes = pd.read_csv('data/transacoes.csv')
    historico = pd.read_csv('data/historico_atendimento.csv')
    return perfis, produtos, transacoes, historico

perfis, produtos, transacoes, historico = carregar_dados()

# 2. Interface com o Usuário (Streamlit)
st.title("Finassist - Assistente Financeiro Inteligente")

# Seletor de Cliente (Adicionado para dinamismo)
nome_clientes = [p['nome'] for p in perfis]
cliente_selecionado = st.sidebar.selectbox("Selecione o Cliente:", nome_clientes)

# Filtrar o perfil do cliente selecionado
perfil = next(p for p in perfis if p['nome'] == cliente_selecionado)

st.write(f"Olá, **{perfil['nome']}**! Como posso te ajudar com suas finanças hoje?")

# Caixa de texto para a pergunta
pergunta = st.text_input("Digite sua dúvida (ex: Qual produto é indicado para mim?):")

if pergunta:
    # O contexto é dinâmico baseado no cliente selecionado
    contexto = f"""
    Perfil do Cliente: {perfil}
    Produtos Disponíveis: {produtos}
    Transações Recentes: {transacoes.to_string()}
    """
   
    # Execução baseada na configuração do usuário
    if USE_GEMINI:
        # prompt = f"Com base nos dados: {contexto}. Responda: {pergunta}"
        # resposta = model.generate_content(prompt)
        # st.write(resposta.text)
        pass
    else:
        # Lógica de Demonstração (Sem API ativada)
        st.warning("Executando em Modo de Demonstração (API do Gemini desativada).")
        
        st.write(f"*(Processando dúvida de {perfil['nome']}...)*")
            
        # Exemplo de resposta baseada no perfil dinâmico
        if "risco" in pergunta.lower() or "investir" in pergunta.lower():
            st.write(f"**Finassist:** Como seu perfil é **{perfil['perfil_investidor']}**, "
                     f"recomendo focar em produtos com risco **{ 'baixo' if not perfil['aceita_risco'] else 'médio/alto'}**.")
        elif:
            st.write("**Finassist:** Analisei seus dados. Para melhor te ajudar, poderia reformular sua pergunta?")
        else:
            st.write("**Finassist:** Entendi sua dúvida! Para respostas personalizadas usando IA Generativa em tempo real, ative a chave da API do Gemini no código-fonte.")
