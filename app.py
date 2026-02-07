import streamlit as st
import requests
import pandas as pd
from datetime import datetime

# ---------------- PAGE CONFIG ----------------
st.set_page_config(page_title="Crypto Dashboard", page_icon="💰", layout="wide")

# ---------------- SESSION STATE ----------------
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False


# ---------------- LOGIN FUNCTION ----------------
def login():
    st.markdown(
        """
        <style>
        .main {
            background: linear-gradient(135deg,#050b24,#0b1c44);
            color:white;
        }
        .stTextInput>div>div>input {
            border-radius:10px;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    st.title("🔐 Crypto Dashboard Login")

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        if username == "admin" and password == "1234":
            st.session_state.logged_in = True
            st.success("Login Successful ✔")
            st.rerun()
        else:
            st.error("Invalid Username or Password ❌")


# ---------------- FETCH DATA ----------------
def fetch_crypto_data():
    url = "https://api.coingecko.com/api/v3/coins/markets"
    params = {
        "vs_currency": "usd",
        "order": "market_cap_desc",
        "per_page": 5,
        "page": 1,
        "sparkline": False
    }

    response = requests.get(url, params=params)
    data = response.json()

    crypto_list = []

    for coin in data:
        crypto_list.append({
            "Crypto": coin["name"],
            "Symbol": coin["symbol"].upper(),
            "Price ($)": coin["current_price"],
            "24h Change (%)": coin["price_change_percentage_24h"],
            "Volume": coin["total_volume"]
        })

    df = pd.DataFrame(crypto_list)
    df.fillna(0, inplace=True)
    df["Time"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    df.to_csv("crypto_data.csv", index=False)

    return df


# ---------------- DASHBOARD ----------------
def dashboard():
    st.title("💰 Live Crypto Price Dashboard")

    col1, col2 = st.columns([5,1])

    with col2:
        if st.button("Logout"):
            st.session_state.logged_in = False
            st.rerun()

    st.write("Top 5 Cryptocurrencies (Live Data)")

    df = fetch_crypto_data()

    st.dataframe(df, use_container_width=True)

    st.success("Last Updated: " + datetime.now().strftime("%Y-%m-%d %H:%M:%S"))


# ---------------- MAIN ----------------
if st.session_state.logged_in:
    dashboard()
else:
    login()
