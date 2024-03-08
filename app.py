import streamlit as st
from openai import OpenAI
import os 


openai_api_key = os.environ["Ope"]
client = OpenAI(api_key=openai_api_key)


def get_response(prompt):
    completion = client.chat.completions.create(
        model="gpt-4-0125-preview",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt}
        ]
    )
    return completion.choices[0].message.content

# Streamlit app layout
st.title("Chat with GPT-4 Turbo")

# Session state to store chat history
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []

# Function to update chat history
def update_chat_history():
    user_input = st.session_state.user_input_sidebar  # Use session state variable
    if user_input.strip():  # Ensure input is not just whitespace
        # Make both user input and model response bold for display
        formatted_user_input = f"**You:** {user_input}"
        st.session_state.chat_history.append(formatted_user_input)
        model_response = get_response(user_input)
        formatted_model_response = f"**GPT-4 Turbo:** {model_response}"
        st.session_state.chat_history.append(formatted_model_response)
        st.session_state.user_input_sidebar = ""  # Clear input box after sending

# Function to manually trigger chat update without duplication
def manual_send():
    if st.session_state.user_input_sidebar.strip():  # Check if there's text to send
        update_chat_history()

# Function to delete chat history
def delete_chat_history():
    st.session_state.chat_history = []

# Sidebar for input and buttons
with st.sidebar:
    # User input in sidebar

    st.text_area("Enter your message here:", key="user_input_sidebar", height=200)
    # st.text_input("Enter your message here:", key="user_input_sidebar", on_change=None)
    
    # Send button - triggers manual send
    send_button = st.button("Send", on_click=manual_send)
    
    # Button to clear chat history
    delete_button = st.button("Delete chat", on_click=delete_chat_history)

# Display chat history in the main page area
for message in st.session_state.chat_history:
    st.markdown(message, unsafe_allow_html=True)
