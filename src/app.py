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
    transacoes = pd.read_csv('data/transacoes.csv', dtype={'id_cliente': int})
    historico = pd.read_csv('data/historico_atendimento.csv', dtype={'id_cliente': int})
    return perfis, produtos, transacoes, historico

perfis, produtos, transacoes, historico = carregar_dados()

# 2. Interface com o Usuário (Streamlit)
st.title("Finassist - Assistente Financeiro Inteligente")

# Seletor de Cliente (Adicionado para dinamismo)
nome_clientes = [p['nome'] for p in perfis]
cliente_selecionado = st.sidebar.selectbox("Selecione o Cliente:", nome_clientes)

# Filtra o perfil e os dados específicos desse cliente
perfil = next(p for p in perfis if p['nome'] == cliente_selecionado)
transacoes_cliente = transacoes[transacoes['id_cliente'] == perfil['id']]
historico_cliente = historico[historico['id_cliente'] == perfil['id']]

st.write(f"Olá, **{perfil['nome']}**! Como posso te ajudar com suas finanças hoje?")

# Caixa de texto para a pergunta
pergunta = st.text_input("Digite sua dúvida (ex: Qual produto é indicado para mim?):")

if pergunta:
    # O contexto é dinâmico baseado no cliente selecionado
    contexto = f"""
    Perfil do Cliente: {perfil}
    Produtos Disponíveis: {produtos}
    Transações do Cliente: {transacoes_cliente.to_string()}
    Histórico de Atendimento: {historico_cliente.to_string()}
    """
   
    # Execução baseada na configuração do usuário
    if USE_GEMINI:
        # prompt = f"Com base nos dados: {contexto}. Responda: {pergunta}"
        # resposta = model.generate_content(prompt)
        # st.write(resposta.text)
        pass
    else:
        # Lógica de Demonstração (Sem API ativada)
        st.warning("Executando em Modo de Demonstração.")
        
        st.write(f"*(Processando dúvida de {perfil['nome']}...)*")
            
        # Exemplo de resposta baseada no perfil dinâmico
        pergunta_lower = pergunta.lower()
        
        if "risco" in pergunta_lower or "investir" in pergunta_lower:
            st.write(f"**Finassist:** Como seu perfil é **{perfil['perfil_investidor']}**, "
                     f"recomendo focar em produtos com risco **{'baixo' if not perfil['aceita_risco'] else 'médio/alto'}**.")
        
        elif "gasto" in pergunta_lower or "transação" in pergunta_lower:
            total_gasto = transacoes_cliente[transacoes_cliente['tipo'] == 'saida']['valor'].sum()
            st.write(f"**Finassist:** Analisando suas transações, você gastou um total de **R$ {total_gasto:.2f}** recentemente.")
            
        else:
            st.write("**Finassist:** Analisei seus dados. Para melhor te ajudar, poderia reformular sua pergunta?")
