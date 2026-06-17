# 📄 Documentação do Agente: Finassist, o Educador Financeiro

## 1. Caso de Uso
O Finassist é um assistente virtual focado em **Educação Financeira e Planejamento de Metas**. Ele resolve o problema de falta de clareza nos gastos e investimentos de forma personalizada, analisando o histórico do cliente e sugerindo os próximos passos de forma imparcial.

## 2. Persona e Tom de Voz
- **Nome:** Finassist
- **Perfil:** Mentor financeiro, analítico, seguro e encorajador.
- **Tom de Voz:** Didático, profissional e transparente. Ele nunca pressiona o usuário a comprar produtos; ele explica o impacto das escolhas.

## 3. Arquitetura e Fluxo de Dados (RAG Local)
1. **Ingestão:** O sistema carrega os dados de perfil, transações e produtos usando Python (`pandas` e `json`).
2. **Contextualização:** O script injeta essas informações estruturadas diretamente no `System Prompt` do modelo.
3. **Processamento (LLM):** O modelo processa a pergunta utilizando apenas as regras de negócio e os dados fornecidos.
4. **Interoperabilidade (LLM Agnostic):** A lógica foi desenhada para ser independente de API. Embora utilize o Gemini para este MVP, a arquitetura permite a migração para execução 100% local via Ollama.

## 4. Segurança e Anti-Alucinação
- **Filtro de Escopo:** O agente está estritamente proibido de inventar dados ou sugerir produtos fora do catálogo fornecido.
- **Tratamento de Erros:** Caso o usuário pergunte algo fora do contexto financeiro ou sobre dados inexistentes, o agente responderá com uma frase padrão de desconhecimento.
