# app.py
import streamlit as st
from auth_module import login_user, signup_user
from predict_page import heart_disease_predict_page
from visualize_page import show_visualization

st.set_page_config(page_title="Heart Disease Predictor", layout="wide")

# Initialize session state
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "email" not in st.session_state:
    st.session_state.email = ""

# Sidebar for navigation or login/signup
if st.session_state.logged_in:
    st.sidebar.markdown(f"👤 **Logged in as:** {st.session_state.email}")
    menu = ["Predict", "Visualize", "Logout"]
    choice = st.sidebar.radio("Navigate", menu)

    if choice == "Predict":
        heart_disease_predict_page()
    elif choice == "Visualize":
        show_visualization()
    elif choice == "Logout":
        st.session_state.logged_in = False
        st.session_state.email = ""
        st.rerun()
else:
    st.sidebar.title("Welcome ❤️")
    menu = ["Login", "Sign Up"]
    choice = st.sidebar.selectbox("Select", menu)

    if choice == "Login":
        st.title("🔐 Login")
        email = st.text_input("Email")
        password = st.text_input("Password", type="password")
        if st.button("Login"):
            if login_user(email, password):
                st.session_state.logged_in = True
                st.session_state.email = email
                st.success("Logged in successfully!")
                st.rerun()
            else:
                st.error("Invalid credentials")

    else:  # Sign Up
        st.title("🆕 Create account")
        email = st.text_input("Email (for signup)")
        password = st.text_input("Password", type="password")
        if st.button("Sign Up"):
            if signup_user(email, password):
                st.success("Account created! Please log in.")
            else:
                st.warning("Account already exists.")
