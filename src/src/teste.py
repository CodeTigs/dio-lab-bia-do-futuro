import google.generativeai as genai
from config import GEMINI_API_KEY

# Configura a chave
genai.configure(api_key=GEMINI_API_KEY)

print("🔍 Buscando modelos disponíveis para a sua chave...")
print("-" * 40)

# Lista todos os modelos que suportam chat/geração de texto
for m in genai.list_models():
    if 'generateContent' in m.supported_generation_methods:
        print(m.name)
        
print("-" * 40)
