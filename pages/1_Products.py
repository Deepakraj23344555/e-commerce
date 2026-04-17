import streamlit as st
from database.db import SessionLocal
from database.models import Product
from utils.cart import add_to_cart

st.set_page_config(page_title="Products", layout="wide")
st.title("Discover Products")

# Simple Search
search_query = st.text_input("Search products...", "")

db = SessionLocal()
query = db.query(Product)
if search_query:
    query = query.filter(Product.name.ilike(f"%{search_query}%"))
products = query.all()
db.close()

if not products:
    st.warning("No products found in the database. (Admins need to add some!)")

# Display in a grid using Streamlit columns
cols = st.columns(3)
for index, product in enumerate(products):
    with cols[index % 3]:
        st.markdown(f"""
        <div class="product-card">
            <h3>{product.name}</h3>
            <p>{product.category}</p>
            <p class="price-tag">${product.price:.2f}</p>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button(f"Add to Cart", key=f"btn_{product.id}"):
            add_to_cart(product.id)
