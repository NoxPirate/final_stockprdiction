import numpy as np
import pandas as pd
import yfinance as yf
from keras.models import load_model
import streamlit as st
import matplotlib.pyplot as plt
from sklearn.preprocessing import MinMaxScaler
from datetime import date
import requests 

# --- Load the pre-trained Model ---
model = load_model('C:\\Users\\hrish\\OneDrive\\Documents\\Desktop\\stockpr-main\\stockpr-main\\mainapp\\Stock Prediction model.keras')

# --- Custom CSS for Background Image and Styling ---
st.markdown(
    """
    <style>
    .stApp {
        background: linear-gradient(to bottom right, #0f2027, #203a43, #2c5364),
                    url('https://source.unsplash.com/1600x900/?finance,stock,market');
        background-size: cover;
        background-attachment: fixed;
        color: white;
    }
    h1, h2, h3, h4 {
        font-family: 'Arial', sans-serif;
        color: #f5f5f5;
        text-align: center;
    }
    .sidebar .sidebar-content {
        background-color: rgba(0, 0, 0, 0.8);
        padding: 10px;
        border-radius: 10px;
    }
    .stButton button {
        background-color: #1f77b4;
        color: white;
        border-radius: 10px;
    }
    .stCheckbox span {
        color: white;
    }
    .stPlotlyChart {
        background-color: rgba(255, 255, 255, 0.8);
        padding: 20px;
        border-radius: 15px;
    }
    </style>
    """, unsafe_allow_html=True
)

# --- Function to Fetch Stock List from CSV ---
@st.cache_data(ttl=86400)  # Cache for 24 hours
def get_stock_list():
    try:
        # Load stock symbols and names from a local CSV file
        stock_df = pd.read_csv('C:\\Users\\hrish\\OneDrive\\Documents\\Desktop\\stockpr-main\\stockpr-main\\nasdaq_screener_1729353736245.csv')
        return stock_df[['Symbol', 'Name']]  # Load both columns
    except Exception as e:
        st.error(f"Error loading stock list: {e}")
        return pd.DataFrame({"Symbol": ["AAPL", "MSFT", "GOOG", "AMZN", "TSLA"], "Name": ["Apple", "Microsoft", "Google", "Amazon", "Tesla"]})  # Fallback list

# --- Sidebar for Inputs ---
st.sidebar.title("📊 Stock Market Dashboard")
st.sidebar.header("Settings")
stock_list_df = get_stock_list()
formatted_stock_list = [f"{row['Name']} ({row['Symbol']})" for index, row in stock_list_df.iterrows()]
stock = st.sidebar.selectbox('Choose Stock Symbol', formatted_stock_list)
start = st.sidebar.date_input("Start Date", pd.to_datetime('2012-01-01'))
end = st.sidebar.date_input("End Date", date.today())
show_ma50 = st.sidebar.checkbox('Show 50-Day MA', True)
show_ma100 = st.sidebar.checkbox('Show 100-Day MA', True)
show_ma200 = st.sidebar.checkbox('Show 200-Day MA', True)

# Extract the selected stock symbol from the formatted name
selected_stock_symbol = stock.split('(')[-1].strip(' )')

# --- Fetch and Display Stock Data ---
data = yf.download(selected_stock_symbol, start=start, end=end)
st.header(f"📈 Stock Data for {selected_stock_symbol}")
st.write(data)
st.subheader("📑 Data Summary")
st.write(data.describe())

# --- Explanation of Current Stock Data ---
st.subheader("📊 Explanation of Current Stock Data")
st.write("""
The data displayed represents the historical stock prices for the selected company. 
The key columns in the dataset include:
- **Open**: The price at which the stock opened at the beginning of the trading session.
- **High**: The highest price reached during the trading session.
- **Low**: The lowest price recorded during the trading session.
- **Close**: The price of the stock at the end of the trading session.
- **Volume**: The total number of shares traded during the session.

The summary statistics above provide insights into the stock's performance over the selected date range, helping investors to understand its volatility and overall behavior.
""")

# --- Moving Averages ---
ma_50_days = data.Close.rolling(50).mean()
ma_100_days = data.Close.rolling(100).mean()
ma_200_days = data.Close.rolling(200).mean()

# Plotting Stock Price with Moving Averages
fig1 = plt.figure(figsize=(12, 6))
plt.plot(data.Close, label='Price', color='#16a085')
if show_ma50:
    plt.plot(ma_50_days, label='50-Day MA', color='#e74c3c')
if show_ma100:
    plt.plot(ma_100_days, label='100-Day MA', color='#3498db')
if show_ma200:
    plt.plot(ma_200_days, label='200-Day MA', color='#f1c40f')

plt.title(f'{selected_stock_symbol} Stock Price with Moving Averages')
plt.xlabel('Date')
plt.ylabel('Price')
plt.legend()
st.pyplot(fig1)

# --- Model Predictions ---
data_train = data['Close'][0:int(len(data) * 0.8)]
data_test = data['Close'][int(len(data) * 0.8):]
scaler = MinMaxScaler(feature_range=(0, 1))
past_100_days = data_train.tail(100)
data_test_combined = pd.concat([past_100_days, data_test], ignore_index=True)
data_test_scaled = scaler.fit_transform(data_test_combined.values.reshape(-1, 1))

x, y = [], []
for i in range(100, len(data_test_scaled)):
    x.append(data_test_scaled[i - 100:i])
    y.append(data_test_scaled[i, 0])
x, y = np.array(x), np.array(y)

predicted_prices = model.predict(x)
scale_factor = 1 / scaler.scale_[0]
predicted_prices = predicted_prices * scale_factor
y = y * scale_factor

# Plotting Actual vs Predicted Prices
fig2 = plt.figure(figsize=(12, 6))
plt.plot(predicted_prices, label='Predicted Price', color='#e74c3c')
plt.plot(y, label='Actual Price', color='#16a085')
plt.title('Actual vs Predicted Price')
plt.xlabel('Time')
plt.ylabel('Price')
plt.legend()
st.pyplot(fig2)

# --- Explanations for Graphs ---
st.subheader("📊 Explanation of Graphs")
st.write(""" 
1. **Moving Averages**: The moving averages smooth out price data over specified periods. The 50-day MA shows short-term trends, while the 200-day MA indicates long-term trends. A crossover can signal potential buy or sell opportunities.

2. **Predicted vs Actual Prices**: This graph displays the predicted stock prices based on historical data versus the actual closing prices. It helps to assess the model's accuracy and performance in forecasting trends.

3. **Performance Metrics**: Volatility indicates how much the stock price fluctuates, and RSI provides insights into whether the stock is overbought or oversold. These metrics can guide investment decisions.
""")

# --- Interactive Charts ---
st.subheader("📈 Interactive Stock Charts")
st.line_chart(data['Close'])

# --- Stock Recommendation ---
st.subheader('📈 Stock Recommendation')
if ma_50_days.iloc[-1] > ma_200_days.iloc[-1]:
    recommendation = "Buy"
    recommendation_color = "success"
    recommendation_reason = (
        "The 50-day moving average is above the 200-day moving average, indicating a bullish trend. "
        "This suggests that the stock's price may continue to rise in the near future, making it an attractive buy."
    )
elif ma_50_days.iloc[-1] < ma_200_days.iloc[-1]:
    recommendation = "Sell"
    recommendation_color = "error"
    recommendation_reason = (
        "The 50-day moving average is below the 200-day moving average, indicating a bearish trend. "
        "This suggests that the stock's price may continue to fall, which might be a good time to sell."
    )
else:
    recommendation = "Hold"
    recommendation_color = "info"
    recommendation_reason = (
        "The moving averages are close together, indicating no significant trend. "
        "In this scenario, it's wise to hold the stock until clearer signals appear."
    )

st.write(f"Recommendation: **{recommendation}**")
st.write(recommendation_reason)

# --- Stock Performance Metrics ---
st.subheader("📊 Performance Metrics")
data['Daily Return'] = data['Close'].pct_change()
volatility = data['Daily Return'].std()
st.write(f"Volatility: {volatility:.2%}")
st.write("""
**Volatility** measures how much the stock price fluctuates over time. 
A higher volatility indicates that the stock is more unpredictable, which can mean higher risk. 
In contrast, lower volatility suggests that the stock price is more stable.

For investors, understanding volatility is crucial because it helps assess the risk associated with the stock. 
Typically, investors seeking stable returns prefer stocks with lower volatility, while those willing to take on more risk may target higher volatility stocks for potentially greater returns.
""")

# RSI Calculation
window_length = 14
delta = data['Close'].diff()
gain = delta.where(delta > 0, 0).rolling(window_length).mean()
loss = -delta.where(delta < 0, 0).rolling(window_length).mean()
rs = gain / loss
rsi = 100 - (100 / (1 + rs))
st.write(f"RSI: {rsi.iloc[-1]:.2f}")
st.write("""
**Relative Strength Index (RSI)** is a momentum oscillator that measures the speed and change of price movements. 
Typically, RSI values range from 0 to 100. A stock is considered overbought when the RSI is above 70, indicating a potential price decrease, while an RSI below 30 suggests the stock may be oversold and due for a price increase.

RSI is particularly useful for identifying potential reversal points in stock price trends, helping investors make more informed trading decisions.
""")

# --- Latest News Section ---
st.subheader("📰 Latest Stock News")
search_news = st.text_input("Search News for a Stock:")
if search_news:
    news_url = f"https://newsapi.org/v2/everything?q={search_news}&apiKey=bdcd13b0b0fc445a9a198e2b2b5bddc2"
else:
    news_url = f"https://newsapi.org/v2/everything?q={selected_stock_symbol}&apiKey=bdcd13b0b0fc445a9a198e2b2b5bddc2"

response = requests.get(news_url).json()
if response['status'] == 'ok':
    for article in response['articles'][:5]:
        st.write(f"**{article['title']}**")
        st.write(f"{article['description']}")

        # Check if 'urlToImage' exists and is not None or an empty string
        if 'urlToImage' in article and article['urlToImage']:
            st.image(article['urlToImage'], use_column_width=True)
        else:
            st.write("No image available for this news article.")  # Only show content if no image available
        
        st.write(f"[Read more]({article['url']})")


