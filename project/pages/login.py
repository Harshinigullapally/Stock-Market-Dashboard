import streamlit as st
from db_config import verify_user, add_user
from streamlit_extras.switch_page_button import switch_page

# ✅ Set Background from URL
def set_background_from_url(image_url):
    css = f"""
    <style>
    .stApp {{
        background-image: url("{image_url}");
        background-size: cover;
        background-position: center;
        background-repeat: no-repeat;
    }}
    </style>
    """
    st.markdown(css, unsafe_allow_html=True)

# ✅ Use an online image (replace this URL with any image you like)
set_background_from_url("https://images.unsplash.com/photo-1542281286-9e0a16bb7366")

# ✅ Ensure session state is initialized
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

# 🚀 **Login UI Layout**
st.markdown("<h1 style='text-align: center; color: white;'>🔐 Login Page</h1>", unsafe_allow_html=True)

option = st.radio("Select an option:", ["Login", "Sign Up"])

if option == "Login":
    username = st.text_input("Username:", key="login_username")
    password = st.text_input("Password:", type="password", key="login_password")

    if st.button("Login"):
        if verify_user(username, password):
            st.session_state.authenticated = True
            st.session_state.username = username
            st.success("Login successful! Redirecting...")
            st.rerun()  # ✅ Refresh the app
        else:
            st.error("Invalid username or password")

elif option == "Sign Up":
    new_username = st.text_input("Create Username:", key="signup_username")
    new_password = st.text_input("Create Password:", type="password", key="signup_password")

    if st.button("Sign Up"):
        if add_user(new_username, new_password):
            st.success("Account created successfully! Please login.")
        else:
            st.error("Username already exists. Choose a different one.")

# ✅ If user is authenticated, show a "Go to Dashboard" button
if st.session_state.authenticated:
    st.markdown("[Go to Dashboard](app.py)")
    switch_page("app.py")
