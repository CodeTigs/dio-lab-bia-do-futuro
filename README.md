# 👽GeminiCrypto AI👽 - Agente Financeiro Inteligente com IA Generativa

# Video explicativo do projeto
https://youtu.be/Btra6SJPFoY

## Contexto

Este projeto é um protótipo de um agente financeiro que utiliza IA Generativa para atuar de forma consultiva no mercado de criptoativos. O objetivo é ultrapassar a barreira dos chatbots comuns para:
- **Antecipar necessidades** ao invés de apenas responder perguntas
- **Personalizar** sugestões com base no contexto de cada cliente
- **Cocriar soluções** financeiras de forma consultiva
- **Garantir segurança** e confiabilidade nas respostas (anti-alucinação)



---

## O Que Foi Entregue

### 1. Documentação do Agente
- **Caso de Uso:** Mitigar o risco de decisões baseadas em FOMO na alta volatilidade do mercado cripto.
- **Persona e Tom de Voz:** Consultivo, analítico e técnico, atuando como um analista sênior (Nexus Crypto AI).
- **Arquitetura:** Interface em Streamlit conectada ao modelo Gemini 2.5 Flash, com injeção de dados locais e requisições em tempo real à API da CoinGecko.
- **Segurança:** Regras estritas de NFA (Not Financial Advice) e bloqueio de alucinações através de *Few-Shot Prompting* e checagem de *whitelist* de contratos.

### 2. Base de Conhecimento
Os dados do cliente e parâmetros de segurança foram estruturados localmente na pasta `data/`:

| Arquivo | Formato | Descrição |
|---------|---------|-----------|
| `carteira_crypto.json` | JSON | Ativos em posse, rede e preço médio de compra. |
| `historico_alertas.csv` | CSV | Histórico de interações recentes para memória de curto prazo. |
| `perfil_risco.json` | JSON | Perfil do cliente e limites máximos de exposição (ex: altcoins/memecoins). |
| `whitelist_tokens.json` | JSON | Lista de contratos inteligentes verificados para evitar *scams*. |

### 3. Prompts do Agente
As diretrizes de comportamento e restrições (System Prompt) foram documentadas e implementadas diretamente na inicialização do agente, garantindo o tratamento de *edge cases* (como tentativa de obter chaves privadas ou recomendações de moedas fora do Top 50).

### 4. Aplicação Funcional
O protótipo foi desenvolvido utilizando:
- **Interface:** Streamlit
- **Integração LLM:** API nativa do Google Gemini (modelo `gemini-2.5-flash`).
- **Dados Externos:** Biblioteca `requests` para consumo da CoinGecko API.

---

## Estrutura do Repositório

```text
📁 GeminiCrypto-AI/
│
├── 📄 README.md
├── 📄 requirements.txt               # Dependências do projeto (Streamlit, Pandas, etc.)
├── 📄 .env                           # Chave da API (não versionado)
│
├── 📁 data/                          # Dados mockados para o agente
│   ├── carteira_crypto.json          
│   ├── historico_alertas.csv         
│   ├── perfil_risco.json             
│   └── whitelist_tokens.json         
│
├── 📁 docs/                          # Documentação do projeto
│   ├── 01-documentacao-agente.md     # Caso de uso e arquitetura
│   ├── 02-base-conhecimento.md       # Estratégia de dados
│   ├── 03-prompts.md                 # Engenharia de prompts
│   └── 04-metricas.md                # Avaliação e métricas
│
└── 📁 src/                           # Código da aplicação
    ├── agente.py                     # Lógica principal, integração LLM e APIs
    ├── app.py                        # Interface gráfica 
    └── config.py                     # Gerenciamento de variáveis de ambiente
