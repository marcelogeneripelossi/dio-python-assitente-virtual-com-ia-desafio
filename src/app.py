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
    perfil = json.load(open('data/perfil_investidor.json'))
    produtos = json.load(open('data/produtos_financeiros.json'))
    transacoes = pd.read_csv('data/transacoes.csv')
    historico = pd.read_csv('data/historico_atendimento.csv')
    return perfil, produtos, transacoes, historico

perfil, produtos, transacoes, historico = carregar_dados()

# 2. Interface com o Usuário (Streamlit)
st.title("Finassist - Assistente Financeiro Inteligente")
st.write(f"Olá, **{perfil['nome']}**! Como posso te ajudar com suas finanças hoje?")

# Caixa de texto para a pergunta
pergunta = st.text_input("Digite sua dúvida (ex: Qual produto é indicado para mim?):")

if pergunta:
    # Montagem do Contexto (Conectando os dados para o RAG)
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
        # MODO DE DEMONSTRAÇÃO/FALLBACK (Evita que o app quebre sem a API)
        st.warning("Executando em Modo de Demonstração (API do Gemini desativada).")
        
        pergunta_minuscula = pergunta.lower()
        if "produto" in pergunta_minuscula or "investir" in pergunta_minuscula:
            st.write(f"**Finassist:** Com base no seu perfil **{perfil['perfil_investidor']}**, o produto mais indicado no nosso catálogo é o **Tesouro Selic** ou **CDB Liquidez Diária**, pois seu objetivo atual é '{perfil['objetivo_principal']}'.")
        elif "gasto" in pergunta_minuscula or "transação" in pergunta_minuscula:
            gasto_total = transacoes[transacoes['tipo'] == 'saida']['valor'].sum()
            st.write(f"**Finassist:** Analisando suas transações recentes, você teve um total de **R$ {gasto_total:.2f}** em despesas. O seu maior gasto fixo registrado é o Aluguel (R$ 1200.00).")
        else:
            st.write("**Finassist:** Entendi sua dúvida! Para respostas personalizadas usando IA Generativa em tempo real, ative a chave da API do Gemini no código-fonte.")
