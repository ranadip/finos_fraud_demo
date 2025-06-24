import streamlit as st
import requests
import json
import asyncio
from threading import Thread
from streamlit.runtime.scriptrunner import add_script_run_ctx, get_script_run_ctx

# CSS to create a banner
st.markdown(
    """
    <style>
        .st-key-banner {
            display: flex;
            height: 100%
            width: 100%;
            position: sticky;
            background-color: #05aedc; /* Optional: Set a background color */
            align-items: center; /* Vertically center items */
        }
        .banner-left {
            width: 20%;
            padding-left: 20px; /* Add some padding */
        }
        .banner-right {
            width: 80%;
            text-align: center;
        }
        .sky-blue-svg svg {
            fill: skyblue !important;
        }
    </style>
    """,
    unsafe_allow_html=True,
)

st.sidebar.image("media/ranadip.png")
st.sidebar.markdown("<h1 style='text-align: center;'>Ranadip Chatterjee</h1>", unsafe_allow_html=True)
st.sidebar.markdown("<p style='text-align: center;'>ranadip@google.com</p>", unsafe_allow_html=True)

with st.container(key='banner'):
    # st.markdown("<div class='banner'>", unsafe_allow_html=True)
    col1, col2 = st.columns([0.2, 0.8])

    with col1:
        st.image("media/2022_OSFF_London_BLK.svg", width=None)

    with col2:
        st.markdown("<h1 style='text-align: center; color: black;'>Open Source in Finance Forum London 2025</h1>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)
st.markdown("<h2 style='text-align: center;'>Fraud Handler Agentic Application Demo</h2>", unsafe_allow_html=True)

json_input = st.text_area("JSON Input", 
    '{"prompt": "fraudType: Credit Card Fraud, transactionAmt: USD 10000, transactionDate: 2025.01.25, customerId: 231145, cardId: 42423, customerName: Steven Ahmad, originatingCountry: Zimbabwe"}')
trigger_button = st.button("Simulate Fraud Detection application")
next_steps_text = st.empty()

# REST Endpoint URL
REST_ENDPOINT = "http://localhost:8601/next_steps"  # Assuming Streamlit runs on default port
# Function to stream backend logs
def stream_logs(backend_logs):
    try:
        log_url = "http://localhost:8601/logs"
        response = requests.get(log_url, stream=True)
        response.raise_for_status()
        backend_logs.write_stream(response.iter_lines())
        # for i in response.iter_lines(chunk_size=2):
    except requests.exceptions.RequestException as e:
        st.error(f"Log stream error: {e}")

# Function to send JSON payload
async def send_json(payload):
    try:
        response = requests.post(REST_ENDPOINT, json=payload)
        response.raise_for_status()  # Raise HTTPError for bad responses (4xx or 5xx)
        return response.json()
    except requests.exceptions.RequestException as e:
        return {"error": str(e)}

# Function to update next_steps_text
async def update_next_steps(data):
    print(json.dumps(data, indent=4))
    next_steps_text.markdown(data)

class LogThread(Thread):
    def run(self):
        stream_logs(st.chat_message("logs"))

async def main():
    # Function to send JSON payload
    response_data = ""
    if trigger_button:
        try:
            with st.spinner("Waiting for agent to finish...", show_time=True):
                logthread = LogThread()
                add_script_run_ctx(logthread, get_script_run_ctx())
                logthread.start()
                payload = json.loads(json_input)
            
                response_data = await send_json(payload)
                # import time
                # time.sleep(2)
                # response_data = """Here are the steps to take based on the SOP for Credit Card Fraud:\n\n1.  **Log Incident:** Log the card fraud report/alert in the IMS with a unique case ID. Gather customer and card details, and specifics of disputed transactions.\n2.  **Verify Customer & Initial Assessment:** Securely verify the customer's identity. Review recent transaction history for suspicious patterns.\n3.  **Alert Card Fraud Team & SOC (if applicable):** Escalate to the dedicated Card Fraud Investigation Unit. Alert SOC if a wider system compromise related to card data is suspected.\n4.  **Block Access (Block the Card):** Immediately block the reported compromised/lost/stolen credit or debit card to prevent any further authorizations on that card number.\n5.  **Preserve Evidence:** Secure transaction records, merchant information, fraud alerts, and customer communications.\n6.  **Conduct Investigation:**\n    *   Assign an investigator.\n    *   Analyze disputed transactions, comparing them to legitimate spending patterns.\n    *   Perform CPP analysis if multiple reports emerge.\n    *   Investigate potential skimming or CNP fraud vectors.\n7.  **Victim Communication & Support:**\n"""

            await update_next_steps(response_data)  # Update next_steps_text with response
            logthread.join()
        except json.JSONDecodeError as e:
            st.error(f"Invalid JSON: {e}")
        except requests.exceptions.RequestException as e:
            st.error(f"Request Error: {e}")

if __name__ == "__main__":
    asyncio.run(main())
