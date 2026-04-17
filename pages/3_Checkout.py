import streamlit as st
import time
from database.db import SessionLocal
from database.models import Product, Order
from utils.auth import init_session

st.set_page_config(page_title="Checkout", layout="centered")
init_session()

if not st.session_state.get('logged_in'):
    st.warning("Please log in to proceed with checkout.")
    st.stop()

st.title("Secure Checkout 💳")

cart = st.session_state.get('cart', {})
if not cart:
    st.info("Your cart is empty.")
    st.stop()

db = SessionLocal()
total_amount = 0.0

st.subheader("Order Summary")
for prod_id, quantity in cart.items():
    product = db.query(Product).filter(Product.id == prod_id).first()
    if product:
        cost = product.price * quantity
        total_amount += cost
        st.write(f"{product.name} (x{quantity}) - **${cost:.2f}**")

st.divider()
st.subheader(f"Total Amount to Pay: ${total_amount:.2f}")

# Payment Simulation Form
with st.form("payment_form"):
    st.write("### Payment Details (Mock Integration)")
    payment_method = st.radio("Select Payment Method", ["Credit/Debit Card", "UPI", "Net Banking"])
    
    if payment_method == "Credit/Debit Card":
        st.text_input("Card Number", max_chars=16, placeholder="1234 5678 9101 1121")
        col1, col2 = st.columns(2)
        col1.text_input("Expiry (MM/YY)", placeholder="12/26")
        col2.text_input("CVV", type="password", max_chars=3)
    elif payment_method == "UPI":
        st.text_input("UPI ID", placeholder="username@upi")

    submit_payment = st.form_submit_button("Pay Now", type="primary")

if submit_payment:
    with st.spinner("Processing Payment via Mock Gateway..."):
        time.sleep(2) # Simulate network delay
        
        # Create Order in DB
        try:
            new_order = Order(
                user_id=st.session_state['user_id'],
                total_amount=total_amount,
                status="Pending"
            )
            db.add(new_order)
            db.commit()
            db.refresh(new_order)
            
            # Clear Cart
            st.session_state['cart'] = {}
            
            st.success("Payment Successful! 🎉")
            st.info(f"Your Tracking ID is: **{new_order.tracking_id}**")
            st.balloons()
        except Exception as e:
            db.rollback()
            st.error("Payment failed. Please try again.")

db.close()
