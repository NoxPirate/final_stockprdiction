import os
import streamlit as st
import google.generativeai as genai
import yfinance as yf
import matplotlib.pyplot as plt
from PIL import Image  # Import the Image module

# Set up your Gemini API key (ensure you set this in your environment variables)
api_key = 'AIzaSyA0CX4-smKpX2e5Dy06tueR4nYd6FLJawE'  # Replace with the environment variable name
genai.configure(api_key=api_key)

# Function to get response from Google's Gemini API
def get_gemini_response(prompt):
    try:
        model = genai.GenerativeModel('gemini-1.5-flash')  # Specify the model you want to use
        response = model.generate_content(prompt)
        return response.text  # Get the generated text from the response
    except Exception as e:
        st.error(f"Error occurred: {e}")
        return "Sorry, I couldn't get a response at the moment."

# Function to fetch stock data
def fetch_stock_data(ticker):
    try:
        stock_data = yf.download(ticker, period="1d", interval="1m")
        if stock_data.empty:
            return None
        return stock_data
    except Exception as e:
        st.error(f"Error fetching data: {e}")
        return None

# Function to plot stock data
def plot_stock_data(stock_data, ticker):
    plt.figure(figsize=(10, 5))
    plt.plot(stock_data.index, stock_data['Close'], label='Close Price', color='blue')
    plt.title(f"{ticker} Stock Price", color='white')  # Set title color
    plt.xlabel("Time", color='white')  # Set x-label color
    plt.ylabel("Price (USD)", color='white')  # Set y-label color
    plt.legend()
    plt.grid(color='gray')  # Optional: Change grid color to gray
    plt.xticks(rotation=45, color='white')  # Set x-ticks color
    plt.yticks(color='white')  # Set y-ticks color
    plt.gca().set_facecolor('black')  # Set plot background color to black
    st.pyplot(plt)

# Streamlit app layout
def main():
    # Set the CSS styles for the app
    st.markdown(
        """
        <style>
        .stApp {
            background-color: rgba(25,98,130,255);  /* Set the background color to black */
            
        }
        img {
            max-width: 1000px;  /* Decrease image size */
            height: auto;      /* Maintain aspect ratio */
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    # Load the background image
    image_path = 'C:\\Users\\hrish\\OneDrive\\Documents\\Desktop\\stockpr-main\\stockpr-main\\static\\images\\chat.png'  # Adjust the path if necessary
    image = Image.open(image_path)

    # Display the background image
    st.image(image, use_column_width='auto')  # Decrease the image size by using 'auto'

    # App title and description
    st.title("Stock and Mutual Funds Chatbot")
    st.write("Ask me anything about stocks and mutual funds!")

    # Input for user question
    user_input = st.text_input("You:", "")
    
    if st.button("Send"):
        if user_input:
            # Check if user input is a stock ticker
            if user_input.isalpha() and len(user_input) <= 5:  # Simple check for stock ticker
                stock_data = fetch_stock_data(user_input)
                if stock_data is None:  # If no data is returned
                    st.write(f"**Chatbot:** No data found for ticker {user_input}.")
                else:
                    st.write(f"**Chatbot:** Here is the data for {user_input}:")
                    st.dataframe(stock_data)  # Display the stock data in a dataframe
                    plot_stock_data(stock_data, user_input)  # Plot the stock data
            else:
                # Get response from Gemini
                response = get_gemini_response(user_input)
                # Only display chatbot response
                st.write(f"**Chatbot:** {response}")
        else:
            st.warning("Please enter a question.")

if __name__ == "__main__":
    main()
