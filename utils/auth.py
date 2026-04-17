import bcrypt
import streamlit as st
from database.db import SessionLocal
from database.models import User

def hash_password(password: str) -> str:
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

def verify_password(password: str, hashed: str) -> bool:
    return bcrypt.checkpw(password.encode('utf-8'), hashed.encode('utf-8'))

def login_user(username, password):
    db = SessionLocal()
    user = db.query(User).filter(User.username == username).first()
    db.close()
    if user and verify_password(password, user.password_hash):
        st.session_state['user_id'] = user.id
        st.session_state['username'] = user.username
        st.session_state['role'] = user.role
        st.session_state['logged_in'] = True
        return True
    return False

def init_session():
    if 'logged_in' not in st.session_state:
        st.session_state['logged_in'] = False
    if 'cart' not in st.session_state:
        st.session_state['cart'] = {} # Format: {product_id: quantity}
