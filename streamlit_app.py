# CONFIG
# ========================
API_URL = "http://3.7.46.95:8000"  # replace with your FastAPI backend URL
DEFAULT_TOP_K = 5

# ========================
# STREAMLIT INTERFACE
# ========================
st.set_page_config(page_title="Business Multi-Agent Model", page_icon="🤖")

st.title("💼 Business Multi-Agent Model")

# User input
prompt = st.text_area("Enter your question:", height=100)
top_k = st.number_input("Number of results to retrieve:", min_value=1, max_>
# Send button
if st.button("Send"):
    if not prompt.strip():
        st.warning("Please enter a question!")
    else:
        # Call backend
        payload = {"question": prompt, "top_k": top_k}
        try:
            response = requests.post(f"{API_URL}/ask", json=payload)
            if response.status_code == 200:
                data = response.json()
                st.subheader("Intent Detected")
                st.info(data["intent"])
                st.subheader("Answer")
                st.success(data["answer"])
            else:
                st.error(f"Error connecting to backend. Status code: {respo>                st.json(response.json())  # show backend error
        except requests.exceptions.RequestException as e:
            st.error(f"Request failed: {e}")

