# auth.py
import streamlit as st
import sqlite3
import hashlib
import re

# Database setup
def create_connection():
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS users
                 (email TEXT PRIMARY KEY, password TEXT, name TEXT)''')
    conn.commit()
    return conn

# Password hashing
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# Email validation
def is_valid_email(email):
    pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
    return re.match(pattern, email)

# Sign up function
def sign_up():
    st.subheader("Create New Account")
    name = st.text_input("Full Name")
    email = st.text_input("Email")
    password = st.text_input("Password", type='password')
    confirm_password = st.text_input("Confirm Password", type='password')
    
    if st.button("Sign Up"):
        if not name or not email or not password:
            st.error("All fields are required!")
            return False
        if not is_valid_email(email):
            st.error("Please enter a valid email address")
            return False
        if password != confirm_password:
            st.error("Passwords do not match!")
            return False
        
        conn = create_connection()
        c = conn.cursor()
        
        try:
            c.execute("INSERT INTO users VALUES (?, ?, ?)", 
                     (email, hash_password(password), name))
            conn.commit()
            st.success("Account created successfully! Please login.")
            return True
        except sqlite3.IntegrityError:
            st.error("Email already exists. Please login instead.")
            return False
        finally:
            conn.close()

# Login function
def login():
    st.subheader("Login")
    email = st.text_input("Email")
    password = st.text_input("Password", type='password')
    
    if st.button("Login"):
        if not email or not password:
            st.error("Both email and password are required!")
            return False
        
        conn = create_connection()
        c = conn.cursor()
        c.execute("SELECT * FROM users WHERE email=? AND password=?", 
                  (email, hash_password(password)))
        user = c.fetchone()
        conn.close()
        
        if user:
            st.session_state.authenticated = True
            st.session_state.user_email = email
            st.session_state.user_name = user[2]
            st.success(f"Welcome back, {user[2]}!")
            return True
        else:
            st.error("Invalid email or password")
            return False
    return False

# Main auth function
def show_auth_page():
    st.set_page_config(page_title="Authentication", layout="centered")
    st.title("📰 Personalized News Aggregator")
    
    menu = ["Login", "Sign Up"]
    choice = st.selectbox("Select Option", menu)
    
    if choice == "Login":
        if login():
            st.experimental_rerun()
    else:
        if sign_up():
            st.experimental_rerun()