import streamlit as st
import requests

# API base URL. Update this if you run the frontend outside Docker.
BASE_URL = "http://api:8000"

st.set_page_config(
    page_title="AgriVision AI",
    page_icon="AI",
    layout="centered",
)


# Validate the token and fetch the current user profile.
def get_user_info(token):
    headers = {"Authorization": f"Bearer {token}"}
    try:
        response = requests.get(f"{BASE_URL}/auth/me", headers=headers)
        if response.status_code == 200:
            return response.json()
    except Exception:
        return None
    return None


# ==========================================
# 1. Authentication
# ==========================================
if "token" not in st.session_state:
    st.title("AgriVision AI")
    st.write(
        "Welcome to the smart agriculture prediction platform. "
        "Please sign in to continue."
    )

    tab1, tab2 = st.tabs(["Sign In", "Create Account"])

    with tab1:
        email_login = st.text_input("Email", key="l_email")
        pass_login = st.text_input("Password", type="password", key="l_pass")
        if st.button("Sign In", use_container_width=True):
            res = requests.post(
                f"{BASE_URL}/auth/login",
                json={"email": email_login, "password": pass_login},
            )
            if res.status_code == 200:
                st.session_state.token = res.json()["access_token"]
                st.success("Signed in successfully.")
                st.rerun()
            else:
                st.error("Invalid email or password.")

    with tab2:
        new_name = st.text_input("Full Name")
        new_email = st.text_input("Email")
        new_pass = st.text_input("Password", type="password")
        confirm_pass = st.text_input("Confirm Password", type="password")
        if st.button("Create Account", use_container_width=True):
            if new_pass != confirm_pass:
                st.error("Passwords do not match.")
            else:
                reg_res = requests.post(
                    f"{BASE_URL}/auth/register",
                    json={
                        "full_name": new_name,
                        "email": new_email,
                        "password": new_pass,
                    },
                )
                if reg_res.status_code == 200:
                    st.success(
                        "Account created successfully. "
                        "You can now sign in from the Sign In tab."
                    )
                else:
                    st.error(f"Registration failed: {reg_res.json().get('detail')}")
    st.stop()


# ==========================================
# 2. Main prediction interface
# ==========================================
user_info = get_user_info(st.session_state.token)

if not user_info:
    del st.session_state.token
    st.rerun()

with st.sidebar:
    st.write(f"User: **{user_info['full_name']}**")
    st.divider()
    if st.button("Sign Out", use_container_width=True):
        del st.session_state.token
        st.rerun()

st.title("Predict Crop Yield")
st.write("Enter the agricultural data below to get an estimated crop yield.")

with st.container(border=True):
    col1, col2 = st.columns(2)
    with col1:
        country = st.text_input("Country", "United Kingdom")
        crop = st.text_input("Crop", "Potatoes")
        year = st.number_input("Year", 1990, 2035, 2024)
    with col2:
        temp = st.number_input("Average Temperature (C)", value=12.4)
        rain = st.number_input("Rainfall (mm)", value=1220.0)
        pest = st.number_input("Pesticides (tonnes)", value=18000.0)

    st.divider()

    if st.button("Calculate Prediction", use_container_width=True, type="primary"):
        payload = {
            "country": country,
            "crop": crop,
            "year": year,
            "avg_temp": temp,
            "rainfall": rain,
            "pesticides": pest,
        }

        with st.spinner("Analyzing data..."):
            res = requests.post(f"{BASE_URL}/predict-yield/", json=payload)

            if res.status_code == 200:
                result = res.json()
                st.success("Prediction generated successfully.")

                st.markdown(
                    f"""
                    <div style="text-align: center; padding: 20px; border-radius: 10px; background-color: #1e1e1e; border: 1px solid #4caf50;">
                        <h2 style="color: #4caf50; margin: 0;">Expected Yield</h2>
                        <h1 style="font-size: 50px; margin: 10px 0;">{result['predicted_yield']:,.2f}</h1>
                        <p style="color: #888;">hg/ha (hectograms per hectare)</p>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )
            else:
                st.error(
                    "Unable to connect to the prediction service. "
                    "Make sure the API is running."
                )
