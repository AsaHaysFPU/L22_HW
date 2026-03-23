import streamlit as st
import requests
import pandas as pd

st.title("Crypto Dashboard")

@st.cache_data(ttl=300)
def fetch_data(url, params=None):
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        return response.json()
    except:
        st.error("Error fetching data from API")
        return None

coin = st.sidebar.selectbox(
    "Select Cryptocurrency",
    ["bitcoin", "ethereum", "dogecoin"]
)

days = st.sidebar.slider("Select Days", 1, 30, 7)

url = f"https://api.coingecko.com/api/v3/coins/{coin}/market_chart"
params = {
    "vs_currency": "usd",
    "days": days
}

data = fetch_data(url, params)

if data:
    prices = data["prices"]

    df = pd.DataFrame(prices, columns=["timestamp", "price"])
    df["timestamp"] = pd.to_datetime(df["timestamp"], unit="ms")
    df = df.set_index("timestamp")

    st.subheader("Price Over Time")
    st.line_chart(df["price"])

    current_price = df["price"].iloc[-1]
    previous_price = df["price"].iloc[0]

    st.metric(
        label="Current Price",
        value=f"${current_price:.2f}",
        delta=f"{current_price - previous_price:.2f}"
    )

    st.subheader("Last 10 Prices")
    st.bar_chart(df["price"].tail(10))

    st.subheader("Raw Data")
    st.dataframe(df.tail(20))