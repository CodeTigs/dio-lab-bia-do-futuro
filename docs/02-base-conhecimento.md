# Base de Conhecimento

## Dados Utilizados

Descreva se usou os arquivos da pasta `data`, por exemplo:

| Arquivo | Formato | Utilização no Agente |
|---------|---------|---------------------|
| `carteira_crypto.json` | JSON |Mapear os ativos atuais, saldos, redes (chains) e preço médio de compra para análise de PnL (Lucros/Perdas). | 
| `perfil_risco.json` | JSON | Definir a tolerância a risco, limites de exposição a altcoins/memecoins e preferências de notificação do investidor. |
| `historico_alertas.csv` | CSV | Fornecer memória de curto prazo para contextualizar interações recentes e evitar alertas repetitivos. |
| `whitelist_tokens.json` | JSON | Atuar como camada de segurança, validando contratos inteligentes aprovados para evitar sugestões de scams. |

> [!TIP]
> **Quer um dataset mais robusto?** Você pode utilizar datasets públicos do [Hugging Face](https://huggingface.co/datasets) relacionados a finanças, desde que sejam adequados ao contexto do desafio.

---

## Adaptações nos Dados

Os dados mockados foram desenvolvidos especificamente para as particularidades do ecossistema de criptoativos (DeFi e CeFi). Expandimos a estrutura tradicional de finanças para incluir metadados essenciais, como a identificação da blockchain (ex: Ethereum, Solana) e limites de alocação categorizados (ex: máximo de 5% em memecoins). Também implementamos a estrutura de whitelist, que é uma adaptação de segurança crítica, permitindo que o agente verifique a autenticidade de um token pelo seu endereço de contrato inteligente antes de realizar qualquer análise.

---

## Estratégia de Integração

### Como os dados são carregados?
Os arquivos locais (JSON e CSV) são lidos e carregados em memória no momento da inicialização da interface (via bibliotecas como json e pandas em Python). Os dados estruturados são então convertidos em strings formatadas para compor o contexto do LLM.

[ex: Os JSON/CSV são carregados no início da sessão e incluídos no contexto do prompt]

### Como os dados são usados no prompt?
System Prompt (Instruções do Sistema): Recebe os dados estáticos e as diretrizes definitivas, como o conteúdo do perfil_risco.json e a listagem de ativos do carteira_crypto.json. Isso define a "personalidade" e os limites de atuação do agente desde o primeiro turno da conversa.

Consulta Dinâmica (Context Window): Os dados do historico_alertas.csv e validações do whitelist_tokens.json são acionados e injetados dinamicamente na janela de contexto apenas quando a interação do usuário exige essa validação ou resgate de memória recente, otimizando o consumo de tokens na API do Gemini.
---

## Exemplo de Contexto Montado

[DADOS DE CONTEXTO DO USUÁRIO]
Identificação do Investidor: Mestre
Perfil de Risco: Agressivo (Experiência: Avançado)
Diretriz de Segurança: Não recomendar exposição acima de 5% em Memecoins.

Carteira Atual (Holdings):
- 0.45 BTC (Rede: Bitcoin | Preço Médio: $42,000.00)
- 4.2 ETH (Rede: Ethereum | Preço Médio: $2,100.00)
- 150.0 SOL (Rede: Solana | Preço Médio: $85.50)
- 300.0 LINK (Rede: Ethereum | Preço Médio: $14.20)

Últimos Alertas/Interações:
- 23/03 (09:00): BTC - Fechamento diário acima de $65k. Cenário Bullish. (Status: Lido)
- 23/03 (19:45): LINK - Atingiu alvo de +10% em relação à compra. (Status: Não Lido)
