# Finassist - Assistente Financeiro Inteligente

O **Finassist** é um agente financeiro baseado em arquitetura RAG (Retrieval-Augmented Generation), projetado para oferecer orientações financeiras personalizadas, educativas e seguras. O projeto foca na integridade dos dados, respeitando o perfil de risco do usuário e isolando informações entre clientes.

## 🚀 Funcionalidades
- **Gestão de Perfil:** Análise de risco personalizada (conservador, moderado, arrojado).
- **Consultoria Inteligente:** Respostas baseadas no contexto de transações e histórico do cliente.
- **Segurança de Dados:** Isolamento de contexto por `id_cliente`, garantindo privacidade.
- **Conformidade:** Regras de negócio rígidas contra alucinações e sugestões de alto risco para perfis inadequados.

## 🛠️ Tecnologias Utilizadas
- **Linguagem:** Python
- **Interface:** Streamlit (Web) / Notebook (Simulação)
- **Processamento de Dados:** Pandas & JSON
- **IA Generativa:** Google Gemini (via API)

## 📂 Estrutura do Projeto
- `/data`: Arquivos de dados (JSON e CSV) com informações dos clientes, transações e produtos.
- `/src`: Código-fonte (`app.py` para interface web e `finassist_engine.py` para simulação).
- `/docs`: Documentação técnica, métricas e roteiros de avaliação.

## ⚙️ Como Executar
1. **Configuração do Ambiente:** Certifique-se de ter as bibliotecas instaladas (`pip install pandas streamlit google-generativeai`).
2. **Execução Web:** `streamlit run src/app.py`
3. **Simulação no Colab:** Execute o arquivo `analise_e_execucao.ipynb` para testar o motor de inferência diretamente no ambiente de notebook.

---
*Projeto desenvolvido como parte do desafio técnico de IA Generativa.*
