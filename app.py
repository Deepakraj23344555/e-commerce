import streamlit as st
from database.db import init_db
from utils.auth import init_session

# Page Config must be the first Streamlit command
st.set_page_config(page_title="StreamCart E-Commerce", layout="wide", page_icon="🛍️")

# Initialize DB and Session
init_db()
init_session()

# Custom CSS for Premium UI
st.markdown("""
    <style>
    .product-card {
        border: 1px solid #e0e0e0;
        border-radius: 10px;
        padding: 15px;
        margin-bottom: 20px;
        box-shadow: 2px 2px 10px rgba(0,0,0,0.05);
    }
    .price-tag {
        font-size: 1.2rem;
        color: #ff4b4b;
        font-weight: bold;
    }
    </style>
""", unsafe_allow_html=True)

st.title("Welcome to StreamCart 🛍️")
st.write("Your premium destination for everything.")

if st.session_state['logged_in']:
    st.sidebar.success(f"Logged in as {st.session_state['username']}")
    if st.sidebar.button("Logout"):
        st.session_state.clear()
        st.rerun()
else:
    st.sidebar.warning("You are not logged in.")
    st.info("👈 Please use the sidebar to navigate to Products or Login/Signup.")
