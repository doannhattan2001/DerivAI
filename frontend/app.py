import streamlit as st
import requests
import uuid

# Backend API URL
API_URL = "http://localhost:8000/chat"

st.set_page_config(page_title="DerivAI", page_icon="🎓", layout="wide")

st.title("🎓 DerivAI")
st.markdown("Ask anything! You can also upload images of your homework.")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Initialize session ID
if "session_id" not in st.session_state:
    st.session_state.session_id = str(uuid.uuid4())

if "uploader_key" not in st.session_state:
    st.session_state.uploader_key = 0

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
        if "image" in message and message["image"]:
            st.image(message["image"], caption="Uploaded Image", use_column_width=True)

# Image uploader in the sidebar or main area
with st.sidebar:
    st.header("Upload Image")
    # Use dynamic key to allow resetting
    uploaded_file = st.file_uploader(
        "Choose an image...", 
        type=["jpg", "jpeg", "png"], 
        key=f"uploader_{st.session_state.uploader_key}"
    )

# React to user input
if prompt := st.chat_input("What is your question?"):
    # Display user message in chat message container
    with st.chat_message("user"):
        st.markdown(prompt)
        if uploaded_file:
             st.image(uploaded_file, caption="Uploaded Image", width=200)

    # Add user message to chat history
    user_msg_obj = {"role": "user", "content": prompt}
    if uploaded_file:
         # Store filename or some indicator
         user_msg_obj["image"] = uploaded_file 
    
    st.session_state.messages.append(user_msg_obj)

    # Display assistant response in chat message container
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        message_placeholder.markdown("Thinking...")
        
        try:
            files = {}
            if uploaded_file:
                 # Reset pointer to be sure
                 uploaded_file.seek(0)
                 files = {"file": (uploaded_file.name, uploaded_file, uploaded_file.type)}
            
            # Send session_id for context
            data = {
                "text": prompt,
                "session_id": st.session_state.session_id
            }
            
            response = requests.post(API_URL, data=data, files=files)
            
            if response.status_code == 200:
                answer = response.json().get("response", "No response received.")
                message_placeholder.markdown(answer)
                st.session_state.messages.append({"role": "assistant", "content": answer})
                
                # If an image was sent, reset the uploader for the next turn
                if uploaded_file:
                    st.session_state.uploader_key += 1
                    st.rerun()
            else:
                error_msg = f"Error: {response.status_code} - {response.text}"
                message_placeholder.error(error_msg)
                st.session_state.messages.append({"role": "assistant", "content": error_msg})
        
        except Exception as e:
            message_placeholder.error(f"Failed to connect to backend: {e}")
            st.session_state.messages.append({"role": "assistant", "content": f"Failed to connect to backend: {e}"})

