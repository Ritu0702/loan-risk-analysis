import streamlit as st
import pickle
import numpy as np
import pyodbc

# Login Credentials
conn = pyodbc.connect(
    r'DRIVER={SQL Server};'
    r'SERVER=DESKTOP-KTBMED7\SQLEXPRESS01;'
    r'DATABASE=Loan_db;'
    r'Trusted_Connection=yes;'
)


if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

# Login Page
if not st.session_state.logged_in:

    st.title("Loan Risk Analysis Login")

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):

        query = f"""
        SELECT *
        FROM app_users
        WHERE username='{username}'
        AND password='{password}'
        """

        cursor = conn.cursor()
        cursor.execute(query)

        user = cursor.fetchone()

        if user:
            st.session_state.logged_in = True
            st.success("Login Successful")
            st.rerun()
        else:
            st.error("Invalid Username or Password")

else:

    st.title("Loan Risk Prediction System")

    model = pickle.load(open("loan_risk_model.pkl", "rb"))


    age = st.number_input("Age")
    account_age = st.number_input("Account Age")
    loan_amount = st.number_input("Loan Amount")
    duration = st.number_input("Loan Duration")
    monthly_emi = st.number_input("Monthly EMI")
    total_transactions = st.number_input("Total Transactions")
    total_transaction_amount = st.number_input("Total Transaction Amount")
    avg_transaction_amount = st.number_input("Average Transaction Amount")
    avg_balance = st.number_input("Average Balance")
    max_balance = st.number_input("Maximum Balance")
    min_balance = st.number_input("Minimum Balance")

    if st.button("Predict Risk"):

        data = np.array([[age,
                          account_age,
                          loan_amount,
                          duration,
                          monthly_emi,
                          total_transactions,
                          total_transaction_amount,
                          avg_transaction_amount,
                          avg_balance,
                          max_balance,
                          min_balance]])

        prediction = model.predict(data)

        probability = model.predict_proba(data)
        st.write("Row Prediction:",prediction[0])
        st.write("Probabilities:",probability)

        if prediction[0] == 1:
            st.success(" Low Risk Customer")
            st.write("Risk Probability:", round(probability[0][1] * 100, 2), "%")
        else:
            st.error(" High Risk Customer")
            st.write("Risk Probability:", round(probability[0][0] * 100, 2), "%")