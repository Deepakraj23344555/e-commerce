import streamlit as st
from database.db import SessionLocal
from database.models import Order
from utils.auth import init_session

st.set_page_config(page_title="Orders & Tracking", layout="wide")
init_session()

st.title("Order Tracking 📦")

tab1, tab2 = st.tabs(["Track an Order", "My Order History"])

db = SessionLocal()

# TAB 1: Public Tracking via UUID
with tab1:
    st.write("Enter your unique Tracking ID to see real-time updates.")
    tracking_id = st.text_input("Tracking ID (UUID)")
    
    if st.button("Track Status"):
        if tracking_id:
            order = db.query(Order).filter(Order.tracking_id == tracking_id).first()
            if order:
                st.subheader(f"Status: {order.status}")
                # Visual Status Pipeline
                stages = ["Pending", "Confirmed", "Shipped", "Out for Delivery", "Delivered"]
                try:
                    current_idx = stages.index(order.status)
                except ValueError:
                    current_idx = 0
                
                st.progress((current_idx + 1) / len(stages))
                st.write(f"Order Placed on: {order.created_at.strftime('%Y-%m-%d %H:%M')}")
            else:
                st.error("Invalid Tracking ID. Please check and try again.")

# TAB 2: Logged-in User History
with tab2:
    if not st.session_state.get('logged_in'):
        st.warning("Please log in to view your order history.")
    else:
        user_orders = db.query(Order).filter(Order.user_id == st.session_state['user_id']).order_by(Order.created_at.desc()).all()
        if not user_orders:
            st.info("You haven't placed any orders yet.")
        else:
            for order in user_orders:
                with st.expander(f"Order on {order.created_at.strftime('%Y-%m-%d')} - ${order.total_amount:.2f}"):
                    st.write(f"**Status:** {order.status}")
                    st.write(f"**Tracking ID:** `{order.tracking_id}`")

db.close()
