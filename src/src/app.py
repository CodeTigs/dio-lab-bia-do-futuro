import streamlit as st
from agente import inicializar_agente, enviar_mensagem

# Configuração da página
st.set_page_config(page_title="GeminiCrypto AI", page_icon="🪙", layout="centered")

st.title("👽GeminiCrypto AI👽")
st.markdown("Seu assistente consultivo para o mercado de criptoativos e DeFi.")

# Inicializa o chat e o histórico de mensagens na sessão do Streamlit
if "chat_session" not in st.session_state:
    try:
        st.session_state.chat_session = inicializar_agente()
        st.session_state.mensagens = []
        # Mensagem de boas-vindas do agente
        st.session_state.mensagens.append({
            "role": "assistant", 
            "content": "Sistemas online e dados carregados. Como posso ajudar a analisar sua carteira hoje, Mestre?"
        })
    except Exception as e:
        st.error(f"Erro ao inicializar o agente: {e}")
        st.stop()

# Renderiza o histórico de mensagens na tela
for msg in st.session_state.mensagens:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# Captura o input do usuário
prompt = st.chat_input("Digite sua dúvida sobre o mercado ou sua carteira...")

if prompt:
    # Mostra a mensagem do usuário imediatamente
    st.session_state.mensagens.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Mostra um indicador de carregamento enquanto o Gemini processa
    with st.chat_message("assistant"):
        with st.spinner("Analisando métricas..."):
            try:
                resposta = enviar_mensagem(st.session_state.chat_session, prompt)
                st.markdown(resposta)
                st.session_state.mensagens.append({"role": "assistant", "content": resposta})
            except Exception as e:
                st.error(f"Ocorreu um erro na comunicação com a API: {e}")