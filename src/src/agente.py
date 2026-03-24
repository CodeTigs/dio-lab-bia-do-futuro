import os
import json
import pandas as pd
import requests
import google.generativeai as genai
from config import GEMINI_API_KEY

# Configura a API do Google Gemini
genai.configure(api_key=GEMINI_API_KEY)

def carregar_dados_locais():
    """Lê os arquivos mockados da pasta data e formata como string de contexto."""
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    data_dir = os.path.join(base_dir, 'data')

    try:
        with open(os.path.join(data_dir, 'carteira_crypto.json'), 'r', encoding='utf-8') as f:
            carteira = json.load(f)
        with open(os.path.join(data_dir, 'perfil_risco.json'), 'r', encoding='utf-8') as f:
            perfil = json.load(f)
        historico = pd.read_csv(os.path.join(data_dir, 'historico_alertas.csv')).to_string(index=False)
    except FileNotFoundError as e:
        return f"Aviso: Arquivo de dados não encontrado ({e})."

    contexto = f"""
[DADOS DE CONTEXTO DO USUÁRIO]
Identificação do Investidor: Mestre
Perfil de Risco: {perfil.get('perfil')}
Objetivo: {perfil.get('objetivo_principal')}

Carteira Atual (Holdings):
{json.dumps(carteira.get('ativos'), indent=2, ensure_ascii=False)}

Últimos Alertas/Interações:
{historico}
    """
    return contexto

def buscar_mercado_coingecko():
    """Busca o top 50 de criptomoedas com histórico de 24h, 7d, 30d e 1 ano."""
    try:
        url = "https://api.coingecko.com/api/v3/coins/markets"
        params = {
            "vs_currency": "usd",
            "order": "market_cap_desc",
            "per_page": 100,
            "page": 1,
            # O segredo está aqui: pedimos os dados de múltiplos períodos!
            "price_change_percentage": "24h,7d,30d,1y" 
        }
        response = requests.get(url, params=params)
        dados = response.json()

        resumo = "\n[DADOS DE MERCADO EM TEMPO REAL - TOP 50 COINGECKO]\n"
        for moeda in dados:
            nome = moeda['name']
            simbolo = moeda['symbol'].upper()
            preco = moeda['current_price']
            
            # Captura os dados com segurança (retorna 0 se a API não enviar o dado)
            var_24h = moeda.get('price_change_percentage_24h', 0)
            var_7d = moeda.get('price_change_percentage_7d_in_currency')
            var_30d = moeda.get('price_change_percentage_30d_in_currency')
            var_1y = moeda.get('price_change_percentage_1y_in_currency')

            # Formatação limpa lidando com valores vazios (N/A)
            str_24h = f"{var_24h:.2f}%" if var_24h is not None else "N/A"
            str_7d = f"{var_7d:.2f}%" if var_7d is not None else "N/A"
            str_30d = f"{var_30d:.2f}%" if var_30d is not None else "N/A"
            str_1y = f"{var_1y:.2f}%" if var_1y is not None else "N/A"
            
            resumo += f"- {nome} ({simbolo}): ${preco} | Variação: 24h ({str_24h}), 7d ({str_7d}), 30d ({str_30d}), 1 Ano ({str_1y})\n"
            
        return resumo
    except Exception as e:
        return f"\n[Aviso: Falha ao buscar dados em tempo real da CoinGecko: {e}]"


SYSTEM_PROMPT = """
Você é o GeminiCrypto, um analista financeiro sênior especializado em criptoativos, Web3 e finanças descentralizadas (DeFi).
Seu objetivo é auxiliar o usuário (que você DEVE chamar de Mestre) na leitura de mercado e monitoramento de portfólio.

REGRAS ESTABELECIDAS:
1. Baseamento em Dados: Sempre embase suas respostas nos dados do contexto fornecido (carteira local e dados em tempo real da CoinGecko).
2. Isenção de Responsabilidade (NFA): Nunca forneça aconselhamento financeiro direto com ordens imperativas.
3. Se o usuário perguntar sobre o mercado atual ou histórico recente (semana, mês, ano), cruze as variações temporais da seção [DADOS DE MERCADO EM TEMPO REAL].
4. Filtro de Stablecoins: Ignore stablecoins (como USDT, USDC, DAI) ao relatar as maiores altas ou quedas do mercado. Foque apenas em criptoativos voláteis.
"""

def inicializar_agente():
    contexto_dados = carregar_dados_locais()
    instrucoes_completas = f"{SYSTEM_PROMPT}\n\n{contexto_dados}"

    model = genai.GenerativeModel(model_name="gemini-2.5-flash")
    
    chat = model.start_chat(history=[
        {"role": "user", "parts": [instrucoes_completas]},
        {"role": "model", "parts": ["Entendido, Mestre. Li meu System Prompt e carreguei os dados da sua carteira. Estou operando como GeminiCrypto e pronto para iniciar as análises."]}
    ])
    return chat

def enviar_mensagem(chat_session, mensagem_usuario):
    """Envia a mensagem e injeta os dados ao vivo da CoinGecko sorrateiramente."""
    
    # Busca os dados no exato segundo em que o usuário faz a pergunta
    dados_ao_vivo = buscar_mercado_coingecko()
    
    # Junta a pergunta do usuário com o contexto atualizado do mercado
    prompt_enriquecido = f"Pergunta do usuário: {mensagem_usuario}\n{dados_ao_vivo}"

    response = chat_session.send_message(prompt_enriquecido)
    return response.text