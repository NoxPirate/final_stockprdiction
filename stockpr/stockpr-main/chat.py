import os
import streamlit as st
from google import genai
from google.genai import types
import yfinance as yf
import matplotlib.pyplot as plt

# -------------------------
# App Configuration
# -------------------------
st.set_page_config(page_title="Pulse AI - Financial Advisor", page_icon="🧠", layout="centered")

# -------------------------
# AI Setup & Logic
# -------------------------
SYSTEM_INSTRUCTION = """
You are 'Pulse', an elite, highly intellectual, and extremely articulate Wall Street analyst and financial advisor.
Your primary role is to demystify the complex world of stock markets, mutual funds, crypto, and personal finance for your clients.
Maintain a sophisticated but exceptionally clear and approachable tone.
Break down heavy financial jargon into simple, digestible concepts, often using intuitive analogies.
Structure your answers logically with clear headings, bold text, and bullet points to maximize readability.
Never be confusing or overly verbose. If a user asks a simple question, answer concisely but intellectually.
"""

def get_chat_session(api_key):
    client = genai.Client(api_key=api_key)
    chat = client.chats.create(model="gemini-2.5-flash", config=types.GenerateContentConfig(system_instruction=SYSTEM_INSTRUCTION))
    return client, chat

# -------------------------
# Data Fetching & Plotting
# -------------------------
def fetch_stock_data(ticker):
    try:
        stock_data = yf.download(ticker, period="1mo", interval="1d")
        if stock_data.empty:
            return None
        return stock_data
    except Exception:
        return None

def plot_stock_data(stock_data, ticker):
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.plot(stock_data.index, stock_data['Close'], label='Close Price', color='#00d2ff', linewidth=2)
    ax.set_title(f"{ticker} 1-Month Market Trend", color='white', fontsize=14, pad=15)
    ax.set_xlabel("Date", color='#b3b3b3')
    ax.set_ylabel("Price (USD)", color='#b3b3b3')
    ax.legend(facecolor='#1a1a1a', edgecolor='none', labelcolor='white')
    ax.grid(color='#333333', linestyle='--', alpha=0.5)
    ax.tick_params(colors='#b3b3b3')
    fig.patch.set_facecolor('#0a0a0f')
    ax.set_facecolor('#0a0a0f')
    
    for spine in ax.spines.values():
        spine.set_color('#333333')
        
    return fig

# -------------------------
# Main UI
# -------------------------
def main():
    st.markdown("""
        <style>
        .stApp { background-color: #0a0a0f; color: #ffffff; }
        p, li { font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; font-size: 1.05rem; color: #e0e0e0; line-height: 1.6; }
        h1, h2, h3 { color: #00d2ff; }
        [data-testid="stChatInput"] { background-color: rgba(20, 20, 30, 0.9); border-radius: 12px; border: 1px solid rgba(0, 210, 255, 0.3); }
        [data-testid="stChatMessage"] { background-color: rgba(30, 30, 45, 0.5); border-radius: 10px; padding: 10px; margin-bottom: 5px; border-left: 3px solid #00d2ff; }
        [data-testid="stChatMessage"][data-baseweb="block"]:nth-child(even) { background-color: rgba(20, 20, 30, 0.5); border-left: 3px solid #b3b3b3; }
        </style>
    """, unsafe_allow_html=True)

    st.title("Pulse AI Assistant 🧠")
    st.caption("Your intellectual, deep-learning powered financial advisor.")
    
    # Check default hardcoded key or override
    st.sidebar.markdown("### API Configuration")
    st.sidebar.write("If you get connection errors, your default API Key may be suspended.")
    api_key_input = st.sidebar.text_input(
        "Override Gemini API Key", 
        type="password", 
        help="If the default key fails, paste yours here to reconnect the AI."
    )
    
    # Determine the API key
    default_key = os.environ.get('GOOGLE_API_KEY')
    active_key = api_key_input if api_key_input else default_key

    # Initialize session memory
    if "messages" not in st.session_state:
        st.session_state.messages = []
    if "chat_session" not in st.session_state or st.session_state.get("active_key") != active_key:
        try:
            client, chat = get_chat_session(active_key)
            st.session_state.chat_client = client
            st.session_state.chat_session = chat
            st.session_state.active_key = active_key
        except Exception as e:
            st.error(f"Failed to initialize AI. Please ensure your API key is valid. Error: {e}")
            st.stop()
            
    st.markdown("---")
    st.write("Ask me to analyze market conditions, explain complex mutual fund structures, or just chat about personal finance! **Hint: Type `$TICKER` (e.g. `$AAPL`) to instantly view live market charts.**")

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            if message.get("type") == "plot":
                st.pyplot(message["content"])
            else:
                st.markdown(message["content"])

    if prompt := st.chat_input("Ask about mutual funds, stock strategies, or type $AAPL..."):
        with st.chat_message("user"):
            st.markdown(prompt)
        st.session_state.messages.append({"role": "user", "content": prompt})

        if prompt.startswith('$') and len(prompt) <= 6 and prompt[1:].isalpha():
            ticker = prompt[1:].upper()
            with st.chat_message("assistant"):
                with st.spinner(f"Pulling live market data for {ticker}..."):
                    stock_data = fetch_stock_data(ticker)
                    if stock_data is None:
                        response_msg = f"My apologies, but I couldn't locate reliable market data for the ticker '{ticker}'."
                        st.markdown(response_msg)
                        st.session_state.messages.append({"role": "assistant", "content": response_msg})
                    else:
                        intro_msg = f"Certainly! Here is the 1-month market trend for **{ticker}**:"
                        st.markdown(intro_msg)
                        fig = plot_stock_data(stock_data, ticker)
                        st.pyplot(fig)
                        st.session_state.messages.append({"role": "assistant", "content": intro_msg})
                        st.session_state.messages.append({"role": "assistant", "content": fig, "type": "plot"})
        else:
            with st.chat_message("assistant"):
                with st.spinner("Analyzing query..."):
                    try:
                        response = st.session_state.chat_session.send_message(prompt)
                        st.markdown(response.text)
                        st.session_state.messages.append({"role": "assistant", "content": response.text})
                    except Exception as e:
                        # Print the real exception safely so user knows immediately if it's the API key
                        error_msg = f"⚠️ Cognitive Interruption: {str(e)} \n\n*If this says 'API key not valid' or 'API key has been suspended', please enter a new API key in the sidebar!*"
                        st.error(error_msg)
                        st.session_state.messages.append({"role": "assistant", "content": error_msg})

if __name__ == "__main__":
    main()
