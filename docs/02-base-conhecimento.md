# Base de Conhecimento - Finassist

O Finassist opera sobre uma estrutura de dados normalizada, garantindo que o agente possua contexto suficiente para oferecer orientações financeiras personalizadas e seguras.

## 1. Fontes de Dados
A base de conhecimento é composta por arquivos estruturados que permitem a análise relacional:

- **`perfil_investidor.json`**: Contém os dados demográficos, objetivos financeiros, nível de tolerância ao risco e metas específicas de cada cliente.
- **`produtos_financeiros.json`**: Catálogo curado de produtos de investimento, incluindo categoria, nível de risco, rentabilidade e público-alvo.
- **`transacoes.csv`**: Registro histórico de movimentações financeiras (receitas e despesas), contendo `id_cliente`, data, categoria e valor.
- **`historico_atendimento.csv`**: Logs de interações anteriores com o cliente, permitindo que o Finassist compreenda o contexto de atendimentos prévios e o status de resoluções de problemas.

## 2. Modelo de Dados Relacional
Para assegurar a privacidade e a precisão das respostas, utilizamos o campo `id_cliente` como chave primária para o relacionamento entre as fontes de dados.

> **Regra de Integração:** Nenhuma transação ou histórico de atendimento é processado sem que seja filtrado pelo `id_cliente` correspondente ao perfil ativo no momento da sessão.

## 3. Estratégia de Atualização
Os dados são carregados em tempo de execução via Python (`pandas` para CSV e `json` para arquivos JSON). Utilizamos uma abordagem de **Leitura Direta**, garantindo que o agente sempre tenha acesso à versão mais atualizada dos registros mockados, sem necessidade de consultas a bancos externos complexos durante o MVP.

## 4. Segurança dos Dados
- **Isolamento:** O motor de inferência (`finassist_engine`) realiza o filtro de dados na camada de aplicação, impedindo o cruzamento indevido de informações entre diferentes clientes.
- **Privacidade:** Apenas os dados estritamente necessários para responder à dúvida atual do usuário são injetados no contexto da LLM, minimizando a exposição de dados sensíveis.
