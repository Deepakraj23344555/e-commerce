import streamlit as st

def add_to_cart(product_id):
    if product_id in st.session_state['cart']:
        st.session_state['cart'][product_id] += 1
    else:
        st.session_state['cart'][product_id] = 1
    st.toast("Added to cart! 🛒", icon="✅")

def get_cart_count():
    return sum(st.session_state['cart'].values())
