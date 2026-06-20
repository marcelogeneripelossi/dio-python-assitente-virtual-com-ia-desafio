# Finassist - Assistente Financeiro Inteligente

O **Finassist** é um agente financeiro inspirado em conceitos de RAG (Retrieval-Augmented Generation), utilizando uma base de conhecimento estruturada em arquivos locais, projetado para oferecer orientações financeiras personalizadas, educativas e seguras. O projeto foca na integridade dos dados, respeitando o perfil de risco do usuário e isolando informações entre clientes.

## 🚀 Funcionalidades
* **Identificação do Cliente**

  * Seleção do cliente a partir do nome ou sobrenome.
  * Isolamento de contexto por `id_cliente`, garantindo que cada usuário acesse apenas suas próprias informações.

* **Análise do Perfil do Investidor**

  * Reconhecimento dos perfis **conservador**, **moderado** e **arrojado**.
  * Normalização automática de variações como "conservadora", "moderada" e "arrojada".
  * Recomendação de produtos compatíveis com o nível de risco adequado.

* **Consulta de Metas Financeiras**

  * Recuperação das metas cadastradas para cada cliente.
  * Exibição do valor necessário e do prazo previsto para cada objetivo.
  * Combinação de intenções, permitindo responder perguntas como:

    > "Quais investimentos podem me ajudar a atingir minhas metas?"

* **Recomendações de Produtos Financeiros**

  * Sugestões de investimentos baseadas no perfil do cliente.
  * Consulta de produtos específicos, como Tesouro Direto, CDB, LCI/LCA, fundos multimercado, fundos de ações e ETFs.
  * Explicação dos níveis de risco associados aos produtos disponíveis.

* **Motor de Inferência Baseado em Regras**

  * Identificação de intenções por meio de palavras-chave.
  * Recuperação dinâmica de sugestões a partir da base de conhecimento.
  * Combinação de múltiplas intenções em uma única pergunta.

* **Tratamento de Negações**

  * Identificação de termos negados em frases como:

    > "Não quero arriscar, quero algo seguro."
  * Evita interpretações equivocadas em recomendações financeiras.

* **Consulta ao Histórico de Atendimento**

  * Recuperação do último atendimento realizado pelo cliente.
  * Exibição do tema tratado e do resumo da interação anterior.

* **Consulta de Transações Financeiras**

  * Visualização das movimentações recentes do cliente.
  * Identificação das principais categorias de gastos.
  * Apoio à contextualização das recomendações financeiras.

* **Segurança e Conformidade**

  * Respeito ao perfil de risco do investidor.
  * Alerta sobre incompatibilidade entre o perfil do cliente e o perfil de risco solicitado, mantendo recomendações com caráter educativo e transparente.
  * Utilização exclusiva de dados mockados para fins educacionais e de demonstração.
 
## 🛠️ Tecnologias Utilizadas
- **Linguagem:** Python
- **Interface:** Streamlit (Web) / Notebook (Simulação)
- **Processamento de Dados:** Pandas & JSON
- **IA Generativa:** Google Gemini (via API)

## 📂 Estrutura do Projeto
- `/data`: Arquivos de dados (JSON e CSV) com informações dos clientes, transações e produtos.
- `/src`: Código-fonte (`app.py` para interface web e `finassist_engine.py` para simulação).
- `/docs`: Documentação técnica, métricas e roteiros de avaliação.

## 🧠 Base de Conhecimento

O Finassist utiliza uma base de conhecimento local composta por arquivos JSON e CSV armazenados na pasta [`data/`](./data/). Esses dados simulam o contexto necessário para que o agente realize consultas, personalize respostas e faça recomendações financeiras aderentes ao perfil do cliente.

| Arquivo                     | Formato | Descrição                                                                                                                                                                                                          |
| --------------------------- | ------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| `perfil_investidor.json`    | JSON    | Cadastro dos clientes contendo informações pessoais, perfil de investidor (conservador, moderado ou arrojado), renda mensal, patrimônio, reserva de emergência, aceitação a risco e metas financeiras individuais. |
| `produtos_financeiros.json` | JSON    | Catálogo de produtos financeiros disponíveis, incluindo categoria, nível de risco, rentabilidade, aporte mínimo e indicação de uso conforme o perfil do investidor.                                                |
| `transacoes.csv`            | CSV     | Histórico simplificado de movimentações financeiras dos clientes, contendo receitas, despesas, investimentos, categorias de gastos e tipo da transação (entrada ou saída).                                         |
| `historico_atendimento.csv` | CSV     | Registro de atendimentos anteriores realizados pelos clientes, incluindo canal de contato, tema abordado, resumo da interação e status de resolução.                                                               |
| `palavras_chave.json`       | JSON    | Dicionário de intenções utilizado pelo motor de inferência para identificar temas presentes nas perguntas dos usuários e direcionar o fluxo de resposta.                                                           |
| `chave_sugestoes.json`      | JSON    | Base de sugestões educativas e recomendações pré-definidas associadas a temas financeiros específicos, utilizada para complementar as respostas do agente.                                                         |

Esses arquivos representam a fonte de conhecimento do Finassist e permitem a implementação de um mecanismo simples de recuperação de informações (retrieval), sem dependência de bancos de dados externos.

## 💬 Exemplos de Perguntas

A seguir, alguns exemplos de perguntas que podem ser realizadas ao Finassist para demonstrar suas capacidades de personalização, recuperação de conhecimento e inferência baseada em regras.

### Recomendações e Perfil do Investidor

* Indique produtos para o meu perfil.
* Tenho o perfil moderado. Quais produtos pode me indicar?
* Para perfil conservador, o que tem em mente?
* Sou conservadora. Quais produtos posso pensar em adquirir?
* Indique produtos para investir com perfil arrojado.
* Tenho curiosidade sobre investimentos arrojados.
* Quero algo moderado para investir.

### Produtos e Estratégias de Investimento

* Quero investir meu dinheiro em algo seguro.
* Quero saber mais sobre CDB.
* O que você recomenda para investir no Tesouro Direto?
* Vale a pena investir em LCI/LCA?
* Quais fundos multimercado se encaixam no meu perfil?
* Quero diversificar com um ETF internacional.
* Tenho interesse em ações, mas me preocupo com a volatilidade.

### Metas Financeiras

* Quais são meus objetivos?
* Quais metas financeiras devo priorizar neste momento?
* Quais investimentos para atingir minhas metas?

> O agente é capaz de combinar intenções, apresentando simultaneamente as metas do cliente e sugestões de investimentos adequadas ao seu perfil.

### Risco e Educação Financeira

* Qual é o nível de risco dos produtos recomendados?
* Tenho curiosidade sobre investimentos arrojados.
* Quero algo moderado para investir.

> Caso o cliente solicite informações sobre produtos incompatíveis com seu perfil cadastrado, o Finassist apresenta um alerta educativo antes de exibir as recomendações.

### Histórico de Atendimento

* Qual foi meu último atendimento?
* Qual meu histórico de atendimento?

### Transações e Movimentações Financeiras

* Quais foram minhas últimas transações?
* Quero ver minhas movimentações.
* Quanto gastei no período?
* Qual foi meu total de despesas?
* Em que estou gastando mais?
* Qual categoria consome mais do meu orçamento?


## ⚙️ Como Executar
1. **Configuração do Ambiente:** Certifique-se de ter as bibliotecas instaladas (`pip install pandas streamlit google-generativeai`).
2. **Execução Web:** `streamlit run src/app.py`
3. **Simulação no Colab:** Execute o arquivo `analise_e_execucao.ipynb` para testar o motor de inferência diretamente no ambiente de notebook.

---
*Projeto desenvolvido como parte do desafio técnico de IA Generativa.*
