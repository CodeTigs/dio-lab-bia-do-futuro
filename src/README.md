# Código da Aplicação

## Estrutura

```
├── data/
│   ├── carteira_crypto.json    # Ativos em posse e preço médio
│   ├── historico_alertas.csv   # Memória de curto prazo
│   ├── perfil_risco.json       # Limites de exposição e perfil
│   └── whitelist_tokens.json   # Contratos seguros verificados
├── src/
│   ├── agente.py               # Lógica principal, integração LLM e APIs
│   ├── app.py                  # Interface gráfica Streamlit
│   └── config.py               # Carregamento de variáveis de ambiente
├── .env                        # Chave da API do Google (não versionado)
├── README.md                   # Documentação do projeto
└── requirements.txt            # Dependências do Python
```

##requirements.txt

```
streamlit>=1.32.0
google-generativeai>=0.4.1
pandas>=2.2.1
python-dotenv>=1.0.1
requests>=2.31.0
```

## Como Rodar

```bash
# Instalar dependências
pip install -r requirements.txt

# Rodar a aplicação
streamlit run app.py
```
