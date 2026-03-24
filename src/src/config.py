import os
from dotenv import load_dotenv

# Mapeia exatamente onde está a pasta raiz (um nível acima da pasta src)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ENV_PATH = os.path.join(BASE_DIR, '.env')

# Força o carregamento do arquivo .env exato
load_dotenv(ENV_PATH)

# Obtém a chave da API
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

if not GEMINI_API_KEY:
    raise ValueError(f"API Key do Gemini não encontrada! Verifique se o arquivo existe e tem a chave em: {ENV_PATH}")