import streamlit as st
import requests
import pandas as pd
import matplotlib.pyplot as plt

BASE_URL = "http://127.0.0.1:5000"

book_url = f"{BASE_URL}/book"
member_url = f"{BASE_URL}/member"

st.set_page_config(
    page_title="Library Management System", page_icon="📚", layout="wide"
)

menu = st.sidebar.selectbox("📚 Menu", ["Login", "Register"])
 
#  CSS  
st.markdown(
    """
<style>

/* Background */
.stApp{
    background: linear-gradient(135deg,#0f172a,#1e293b,#111827);
}

/* Form Card */
.form-box{
    background:#1e293b;
    padding:20px;
    border-radius:20px;
    box-shadow:0px 10px 30px rgba(0,0,0,0.6);
    border:1px solid #334155;
}

/* Title */
.title{
    text-align:center;
    font-size:38px;
    font-weight:bold;
    color:#60a5fa;
}

/* Subtitle */
.subtitle{
    text-align:center;
    color:#cbd5e1;
    margin-bottom:25px;
}

/* Labels */
label{
    color:white !important;
    font-weight:600;
}

/* Text Inputs */
.stTextInput input,
.stTextArea textarea{
    background:#334155 !important;
    color:white !important;
    border:1px solid #475569 !important;
    border-radius:10px !important;
}

/* Placeholder */
.stTextInput input::placeholder,
.stTextArea textarea::placeholder{
    color:#94a3b8 !important;
}

/* Button */
div.stButton > button{
    width:100%;
    height:48px;
    background:#2563eb;
    color:white;
    border:none;
    border-radius:10px;
    font-size:17px;
    font-weight:bold;
    transition:0.3s;
}

div.stButton > button:hover{
    background:#1d4ed8;
    transform:scale(1.02);
}

/* Sidebar */
section[data-testid="stSidebar"]{
    background:#111827;
}

/* Success/Error */
.stSuccess{
    border-radius:10px;
}

.stError{
    border-radius:10px;
}

</style>
""",
    unsafe_allow_html=True,
)

#login
if menu == "Login":

    left, center, right = st.columns([1, 1.5, 1])

    with center:

        st.markdown("""
        <div class='form-box'>
        <div class='title'>📚 Library Login</div>
        <div class='subtitle'>Welcome Back 👋</div>""",
            unsafe_allow_html=True,
        )

        email = st.text_input("📧 Email")
        password = st.text_input("🔒 Password", type="password")

        if st.button("🚀 Login"):

            payload = {"email": email, "password": password}
            response = requests.post(f"{BASE_URL}/auth/login", json=payload)

            data = response.json()

            if response.status_code == 200:

                st.session_state["user"] = data
                st.success("✅ Login Successful")
                st.rerun()

            else:

                st.error(data.get("message"))
        st.markdown("</div>", unsafe_allow_html=True)

else:

    left, center, right = st.columns([1, 1.5, 1])

    with center:

        st.markdown("""
        <div class='form-box'>
        <div class='title'>📝 Create Account</div>
        <div class='subtitle'>Join Our Library Today</div>""",
            unsafe_allow_html=True,
        )

        name = st.text_input("👤 Name")
        email = st.text_input("📧 Email")
        password = st.text_input("🔒 Password", type="password")
        phone = st.text_input("📱 Phone")
        address = st.text_area("🏠 Address")

        if st.button("✅ Register"):

            payload = {
                "name": name,
                "email": email,
                "password": password,
                "phone_no": phone,
                "address": address,
            }

            response = requests.post(f"{BASE_URL}/auth/register", json=payload)

            data = response.json()

            if response.status_code in [200, 201]:
                st.success("🎉 Registration Successful")

            else:

                st.error(data.get("message"))

        st.markdown("</div>", unsafe_allow_html=True)
