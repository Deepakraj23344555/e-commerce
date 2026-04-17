import streamlit as st
from database.db import SessionLocal
from database.models import Product

st.set_page_config(page_title="Your Cart")
st.title("Shopping Cart 🛒")

cart = st.session_state.get('cart', {})

if not cart:
    st.info("Your cart is empty. Go add some products!")
else:
    db = SessionLocal()
    total_price = 0
    
    for prod_id, quantity in cart.items():
        product = db.query(Product).filter(Product.id == prod_id).first()
        if product:
            item_total = product.price * quantity
            total_price += item_total
            
            col1, col2, col3 = st.columns([3, 1, 1])
            with col1:
                st.write(f"**{product.name}**")
            with col2:
                st.write(f"Qty: {quantity}")
            with col3:
                st.write(f"${item_total:.2f}")
                
    db.close()
    
    st.divider()
    st.subheader(f"Total: ${total_price:.2f}")
    
    if st.button("Proceed to Checkout", type="primary"):
        if not st.session_state.get('logged_in'):
            st.error("Please login to checkout.")
        else:
            st.switch_page("pages/3_Checkout.py")
