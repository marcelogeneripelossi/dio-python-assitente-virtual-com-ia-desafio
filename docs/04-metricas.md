# Avaliação e Métricas - Finassist

Para garantir que o **Finassist** entregue um serviço de qualidade, seguro e alinhado aos interesses financeiros dos nossos clientes, adotamos um framework de avaliação dividido em três pilares.

## 1. Métricas de Qualidade (KPIs)

| Métrica | Descrição | Meta de Sucesso |
| :--- | :--- | :--- |
| **Precisão de Contexto** | Capacidade da IA em responder baseando-se apenas nos dados injetados (RAG). | > 95% de fidelidade |
| **Taxa de Alucinação** | Frequência com que o agente inventa dados financeiros ou produtos. | 0% (Zero Tolerância) |
| **Conformidade de Perfil** | As sugestões respeitam o perfil de risco do cliente (Conservador/Arrojado). | 100% de conformidade |
| **Tempo de Resposta** | Velocidade da inferência desde a pergunta até a exibição. | < 2 segundos |

## 2. Estratégia de Testes (QA)

Realizamos dois tipos de testes para validar o comportamento do agente:

### A. Testes de "Cenário Limite"
- **Teste de Fora de Escopo:** O agente recebe perguntas sobre culinária, política ou tecnologia para garantir que ele retorne educadamente ao foco financeiro.
- **Teste de Risco Inadequado:** Forçamos o sistema a sugerir produtos de alto risco para um perfil conservador e verificamos se o agente bloqueia a sugestão conforme o System Prompt.
- **Teste de Dados Ausentes:** Perguntamos sobre produtos inexistentes para validar se o agente admite não possuir a informação (evitando alucinações).

### B. Avaliação Humana
Os logs de atendimento (armazenados em `historico_atendimento.csv`) são auditados periodicamente para verificar se o tom de voz do Finassist permanece educativo e prestativo, conforme definido na Persona.

## 3. Segurança e Auditoria
- **Imutabilidade:** O código é desenhado para não permitir que o contexto do cliente A seja acessado pelo cliente B.
- **Rastreabilidade:** Todas as interações podem ser logadas para auditoria de conformidade regulatória (LGPD).
