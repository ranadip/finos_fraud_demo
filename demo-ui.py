import streamlit as st
import requests
import json

# Streamlit UI
st.title("Open Source in Finance Forum London 2025")
st.header("Fraud Handler Agentic Application Demo")

json_input = st.text_area("JSON Input", 
    '{"prompt": "fraudType: Credit Card Fraud, transactionAmt: USD 10000, transactionDate: 2025.01.25, customerId: 231145, cardId: 42423, customerName: Steven Ahmad, originatingCountry: Zimbabwe"}')
trigger_button = st.button("Simulate Fraud Detection application")
next_steps_text = st.empty()

# REST Endpoint URL
REST_ENDPOINT = "http://localhost:8601/next_steps"  # Assuming Streamlit runs on default port

# Function to send JSON payload
def send_json(payload):
    try:
        response = requests.post(REST_ENDPOINT, json=payload)
        response.raise_for_status()  # Raise HTTPError for bad responses (4xx or 5xx)
        return response.json()
    except requests.exceptions.RequestException as e:
        return {"error": str(e)}

# Function to update next_steps_text
def update_next_steps(data):
    print(json.dumps(data, indent=4))
    next_steps_text.markdown(data)

# Trigger POST request on button click
if trigger_button:
    try:
        payload = json.loads(json_input)
        response_data = send_json(payload)
        # response_data = """Here are the steps to take based on the SOP for Credit Card Fraud:\n\n1.  **Log Incident:** Log the card fraud report/alert in the IMS with a unique case ID. Gather customer and card details, and specifics of disputed transactions.\n2.  **Verify Customer & Initial Assessment:** Securely verify the customer's identity. Review recent transaction history for suspicious patterns.\n3.  **Alert Card Fraud Team & SOC (if applicable):** Escalate to the dedicated Card Fraud Investigation Unit. Alert SOC if a wider system compromise related to card data is suspected.\n4.  **Block Access (Block the Card):** Immediately block the reported compromised/lost/stolen credit or debit card to prevent any further authorizations on that card number.\n5.  **Preserve Evidence:** Secure transaction records, merchant information, fraud alerts, and customer communications.\n6.  **Conduct Investigation:**\n    *   Assign an investigator.\n    *   Analyze disputed transactions, comparing them to legitimate spending patterns.\n    *   Perform CPP analysis if multiple reports emerge.\n    *   Investigate potential skimming or CNP fraud vectors.\n7.  **Victim Communication & Support:**\n"""

        # st.write("Response from service:", response_data)
        update_next_steps(response_data)  # Update next_steps_text with response
    except json.JSONDecodeError as e:
        st.error(f"Invalid JSON: {e}")
    except requests.exceptions.RequestException as e:
        st.error(f"Request Error: {e}")
