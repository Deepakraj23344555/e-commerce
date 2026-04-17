import streamlit as st
import pandas as pd
import plotly.express as px
from database.db import SessionLocal
from database.models import User, Product, Order
from utils.auth import init_session

st.set_page_config(page_title="Admin Dashboard", layout="wide")
init_session()

# Security Check
if not st.session_state.get('logged_in') or st.session_state.get('role') != 'admin':
    st.error("Access Denied. Administrator privileges required.")
    st.stop()

st.title("Admin Dashboard 📊")
db = SessionLocal()

tab1, tab2, tab3 = st.tabs(["Analytics", "Manage Products", "Manage Orders"])

# TAB 1: Analytics
with tab1:
    st.header("Store Analytics")
    col1, col2, col3 = st.columns(3)
    
    total_sales = db.query(Order).filter(Order.status != "Cancelled").count()
    revenue = sum([order.total_amount for order in db.query(Order).all()])
    total_users = db.query(User).count()
    
    col1.metric("Total Orders", total_sales)
    col2.metric("Total Revenue", f"${revenue:.2f}")
    col3.metric("Registered Users", total_users)
    
    # Simple Plotly Chart for Orders
    orders = db.query(Order).all()
    if orders:
        df = pd.DataFrame([{ "Date": o.created_at.date(), "Amount": o.total_amount } for o in orders])
        df_grouped = df.groupby("Date").sum().reset_index()
        fig = px.bar(df_grouped, x="Date", y="Amount", title="Daily Revenue")
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("Not enough data for analytics yet.")

# TAB 2: Manage Products
with tab2:
    st.header("Add New Product")
    with st.form("add_product"):
        name = st.text_input("Product Name")
        category = st.selectbox("Category", ["Electronics", "Clothing", "Home", "Books", "Other"])
        desc = st.text_area("Description")
        price = st.number_input("Price ($)", min_value=0.0, format="%.2f")
        stock = st.number_input("Stock Quantity", min_value=0)
        
        if st.form_submit_button("Add Product"):
            new_prod = Product(name=name, category=category, description=desc, price=price, stock=stock)
            db.add(new_prod)
            db.commit()
            st.success(f"Added {name} successfully!")

# TAB 3: Manage Orders
with tab3:
    st.header("Update Order Status")
    all_orders = db.query(Order).order_by(Order.created_at.desc()).all()
    
    if not all_orders:
        st.info("No orders in the system.")
    else:
        for order in all_orders:
            col1, col2, col3, col4 = st.columns([2, 1, 1, 1])
            col1.write(f"**ID:** {order.tracking_id[:8]}... | **User:** {order.user_id}")
            col2.write(f"${order.total_amount:.2f}")
            col3.write(f"Current: {order.status}")
            
            with col4:
                new_status = st.selectbox(
                    "Update Status", 
                    ["Pending", "Confirmed", "Shipped", "Out for Delivery", "Delivered"], 
                    key=f"status_{order.id}",
                    index=["Pending", "Confirmed", "Shipped", "Out for Delivery", "Delivered"].index(order.status)
                )
                if new_status != order.status:
                    order.status = new_status
                    db.commit()
                    st.toast(f"Order updated to {new_status}")

db.close()
