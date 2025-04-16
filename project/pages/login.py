import streamlit as st
from db_config import verify_user, add_user

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

# ✅ Use an online background image
set_background_from_url("https://images.unsplash.com/photo-1542281286-9e0a16bb7366")

# ✅ Initialize session state
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

# 🚀 Login UI
st.markdown("<h1 style='text-align: center; color: white;'>🔐 Login Page</h1>", unsafe_allow_html=True)

option = st.radio("Select an option:", ["Login", "Sign Up"])

if option == "Login":
    username = st.text_input("Username:", key="login_username")
    password = st.text_input("Password:", type="password", key="login_password")

    if st.button("Login"):
        if verify_user(username, password):
            st.session_state.authenticated = True
            st.session_state.username = username
            st.success("✅ Login successful!")
            st.info("👉 Now click **Dashboard** from the sidebar to continue.")
        else:
            st.error("❌ Invalid username or password")

elif option == "Sign Up":
    new_username = st.text_input("Create Username:", key="signup_username")
    new_password = st.text_input("Create Password:", type="password", key="signup_password")

    if st.button("Sign Up"):
        if add_user(new_username, new_password):
            st.success("✅ Account created successfully! Please login.")
        else:
            st.error("⚠️ Username already exists. Choose a different one.")

# ✅ Optional message after login
if st.session_state.authenticated:
    st.markdown("✅ You are logged in as **{}**.".format(st.session_state.username))
    st.info("👉 Click on **Dashboard** in the sidebar to proceed.")
