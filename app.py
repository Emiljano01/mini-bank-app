import streamlit as st
import pandas as pd
import plotly.express as px
from database import (
    init_db, create_user, check_login, get_balance,
    update_balance, add_transaction, get_transactions,
    get_user_id_by_username
)

# Inicializo bazën e të dhënave
init_db()

st.set_page_config(page_title="Mini Bank", page_icon="🏦", layout="centered")

# ---- Session state për të mbajtur user-in e loguar ----
if "user_id" not in st.session_state:
    st.session_state.user_id = None
    st.session_state.username = None


def logout():
    st.session_state.user_id = None
    st.session_state.username = None


# ---- FAQJA: LOGIN / REGJISTRIM ----
def login_page():
    st.title("🏦 Mini Bank")
    tab1, tab2 = st.tabs(["Login", "Regjistrohu"])

    with tab1:
        st.subheader("Hyr në llogari")
        username = st.text_input("Username", key="login_user")
        password = st.text_input("Password", type="password", key="login_pass")
        if st.button("Login"):
            user_id = check_login(username, password)
            if user_id:
                st.session_state.user_id = user_id
                st.session_state.username = username
                st.rerun()
            else:
                st.error("Username ose password gabim!")

    with tab2:
        st.subheader("Krijo llogari të re")
        new_username = st.text_input("Username i ri", key="reg_user")
        new_password = st.text_input("Password i ri", type="password", key="reg_pass")
        if st.button("Regjistrohu"):
            if len(new_username) < 3:
                st.error("Username duhet të ketë të paktën 3 karaktere.")
            elif len(new_password) < 4:
                st.error("Password duhet të ketë të paktën 4 karaktere.")
            else:
                success = create_user(new_username, new_password)
                if success:
                    st.success("U regjistrove me sukses! Tani bëj Login.")
                else:
                    st.error("Ky username ekziston tashmë.")


# ---- FAQJA: DASHBOARD (pas login) ----
def dashboard_page():
    user_id = st.session_state.user_id
    username = st.session_state.username

    st.sidebar.title(f"👤 {username}")
    if st.sidebar.button("Dil (Logout)"):
        logout()
        st.rerun()

    st.title("🏦 Dashboard")

    balance = get_balance(user_id)
    st.metric("Bilanci aktual", f"{balance:.2f} €")

    st.divider()

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("💰 Depozitë")
        deposit_amount = st.number_input("Shuma për depozitim", min_value=0.0, step=10.0, key="dep")
        if st.button("Depozito"):
            if deposit_amount > 0:
                new_balance = balance + deposit_amount
                update_balance(user_id, new_balance)
                add_transaction(user_id, "Depozitë", deposit_amount)
                st.success(f"U depozituan {deposit_amount:.2f} €")
                st.rerun()
            else:
                st.error("Shuma duhet të jetë më e madhe se 0.")

    with col2:
        st.subheader("💸 Tërheqje")
        withdraw_amount = st.number_input("Shuma për tërheqje", min_value=0.0, step=10.0, key="wd")
        if st.button("Tërhiq"):
            if withdraw_amount <= 0:
                st.error("Shuma duhet të jetë më e madhe se 0.")
            elif withdraw_amount > balance:
                st.error("Nuk ke fonde të mjaftueshme!")
            else:
                new_balance = balance - withdraw_amount
                update_balance(user_id, new_balance)
                add_transaction(user_id, "Tërheqje", -withdraw_amount)
                st.success(f"U tërhoqën {withdraw_amount:.2f} €")
                st.rerun()

    st.divider()
    st.subheader("🔁 Transfertë te një përdorues tjetër")
    recipient = st.text_input("Username i marrësit")
    transfer_amount = st.number_input("Shuma për transfer", min_value=0.0, step=10.0, key="tr")
    if st.button("Transfero"):
        recipient_id = get_user_id_by_username(recipient)
        if not recipient_id:
            st.error("Ky përdorues nuk ekziston.")
        elif recipient_id == user_id:
            st.error("Nuk mund t'i transferosh vetes.")
        elif transfer_amount <= 0:
            st.error("Shuma duhet të jetë më e madhe se 0.")
        elif transfer_amount > balance:
            st.error("Nuk ke fonde të mjaftueshme!")
        else:
            update_balance(user_id, balance - transfer_amount)
            add_transaction(user_id, f"Transfer → {recipient}", -transfer_amount)

            recipient_balance = get_balance(recipient_id)
            update_balance(recipient_id, recipient_balance + transfer_amount)
            add_transaction(recipient_id, f"Transfer ← {username}", transfer_amount)

            st.success(f"U transferuan {transfer_amount:.2f} € te {recipient}")
            st.rerun()

    st.divider()
    st.subheader("📊 Historia e transaksioneve")
    transactions = get_transactions(user_id)
    if transactions:
        df = pd.DataFrame(transactions, columns=["Lloji", "Shuma", "Data"])
        st.dataframe(df, use_container_width=True)

        df["Data"] = pd.to_datetime(df["Data"])
        df = df.sort_values("Data")
        df["Bilanci kumulativ"] = df["Shuma"].cumsum() + (balance - df["Shuma"].sum())

        fig = px.line(df, x="Data", y="Bilanci kumulativ", title="Ndryshimi i bilancit nëpër kohë", markers=True)
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("Nuk ka transaksione ende.")


# ---- ROUTER KRYESOR ----
if st.session_state.user_id is None:
    login_page()
else:
    dashboard_page()