import streamlit as st

from finassist_engine import (
    carregar_dados,
    inicializar_contexto,
    motor_finassist
)

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

# ======================================================================
# SYSTEM PROMPT
# ======================================================================

system_prompt = """
Você é o Finassist, um assistente virtual com IA especializado em educação financeira e planejamento de metas. Seu público-alvo são clientes que buscam organizar suas finanças de forma consciente.

[DIRETRIZES DE COMPORTAMENTO]

1. Papel:
Atue como um mentor e educador financeiro.
Seu foco é explicar os conceitos e ajudar o cliente a entender suas opções, nunca forçar a venda de um produto.

2. Tom de Voz:
Didático, profissional, encorajador e transparente.
Evite jargões excessivamente complexos sem explicá-los primeiro.

3. Personalização:
Utilize ativamente os dados de perfil, transações e histórico fornecidos no contexto para dar respostas personalizadas.

[REGRAS DE SEGURANÇA E ANTI-ALUCINAÇÃO]

1. Restrição de Base:
Responda às perguntas baseando-se ESTRITAMENTE nos dados fornecidos.

2. Proibição de Invenção:
Se a informação não estiver disponível na base, responda exatamente:

"Sinto muito, mas não tenho essa informação no momento."

3. Alinhamento de Risco:
Nunca recomende produtos incompatíveis com o perfil cadastrado do cliente sem alertar explicitamente sobre o desvio do perfil.

4. Escopo Fechado:
Se o usuário desviar para temas não financeiros, recuse educadamente e retorne ao foco financeiro.
"""

# ==============================================================================

dados = carregar_dados()
inicializar_contexto(dados)
perfis = dados["perfis"]

st.title("Finassist - Assistente Financeiro Inteligente")

nome_clientes = [p["nome"] for p in sorted(perfis, key=lambda x: x["nome"])]

cliente_selecionado = st.sidebar.selectbox(
    "Selecione o Cliente:",
    nome_clientes
)

perfil = next(
    p
    for p in perfis
    if p["nome"] == cliente_selecionado
)

st.write(
    f"Olá, **{perfil['nome']}**! "
    f"Seu perfil é **{perfil['perfil_investidor']}**."
)

pergunta = st.text_input(
    "Digite sua dúvida:"
)

if pergunta:
    resposta = motor_finassist(
        perfil,
        pergunta,
        dados
    )

    if USE_GEMINI:
        prompt = f"""
        {system_prompt}
        
        CONTEXTO DO CLIENTE:
        {perfil}
        
        PERGUNTA:
        {pergunta}
        
        RESPOSTA GERADA PELO MOTOR:
        {resposta_motor}
        
        INSTRUÇÕES:
        - Não invente informações.
        - Não acrescente produtos.
        - Não altere recomendações.
        - Apenas reescreva a resposta de forma mais natural.
        """

        resposta = model.generate_content(
            prompt
        )

        st.write(resposta.text)

    else:
        st.markdown("### Finassist")
        st.write(resposta)
