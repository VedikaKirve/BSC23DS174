import streamlit as st
import json
from datetime import datetime
import os

# JSON file to store the records
FILENAME = 'mobile_recharge_ledger.json'

# Ensure the ledger file exists
def initialize_ledger():
    if not os.path.exists(FILENAME):
        with open(FILENAME, 'w') as f:
            json.dump([], f)

# Load records from JSON
def load_records():
    with open(FILENAME, 'r') as f:
        return json.load(f)

# Save records to JSON
def save_records(records):
    with open(FILENAME, 'w') as f:
        json.dump(records, f, indent=4)

# Add a new record
def add_recharge_record(record):
    records = load_records()
    records.append(record)
    save_records(records)

# Streamlit UI
def main():
    st.title("📒 Mobile Recharge Records Ledger")

    initialize_ledger()

    menu = ["Add Recharge Record", "View All Records"]
    choice = st.sidebar.selectbox("Menu", menu)

    if choice == "Add Recharge Record":
        st.subheader("Add New Recharge Entry")

        with st.form("recharge_form"):
            date = datetime.now().strftime('%Y-%m-%d')
            mobile_number = st.text_input("Mobile Number")
            operator = st.selectbox("Operator", ["Airtel", "Jio", "Vi", "BSNL", "Other"])
            amount = st.number_input("Amount (₹)", min_value=0)
            payment_mode = st.selectbox("Payment Mode", ["UPI", "Cash", "Credit Card", "Net Banking"])
            txn_id = st.text_input("Transaction ID (or N/A)")
            status = st.selectbox("Status", ["Success", "Failed", "Pending"])
            remarks = st.text_area("Remarks")

            submitted = st.form_submit_button("Submit")

            if submitted:
                record = {
                    "Date": date,
                    "Mobile Number": mobile_number,
                    "Operator": operator,
                    "Amount": f"₹{amount}",
                    "Mode of Payment": payment_mode,
                    "Transaction ID": txn_id,
                    "Status": status,
                    "Remarks": remarks
                }
                add_recharge_record(record)
                st.success("Recharge record added successfully!")

    elif choice == "View All Records":
        st.subheader("All Recharge Records")
        records = load_records()
        if records:
            st.dataframe(records)
        else:
            st.info("No records found.")

if __name__ == '__main__':
    main()
