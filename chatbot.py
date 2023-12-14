import streamlit as st
import numpy as np
from streamlit_chat import message
from streamlit.components.v1 import html

#Initialize chat history
if "messages" not in st.session_state:
  print("intializing messages")
  st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

with st.chat_message("assistant"):
  st.write("Hello human")
  st.bar_chart(np.random.randn(30, 3))
  st.session_state.messages.append({"role": "assistant", "content": "Hello human"}) 

def on_submit_callback():
  print("on_submit_callback")
  print(st.session_state.messages)  

# React to user input
st.chat_input("What is up?", on_submit=on_submit_callback)

#   # Display user message in chat message container
#   with st.chat_message("user"):
#       st.write(prompt)
#   # Add user message to chat history
#   st.session_state.messages.append({"role": "user", "content": prompt})

#   response = f"Echo: {prompt}"
#   # Display assistant response in chat message container
#   with st.chat_message("assistant"):
#       st.write(response)
#   # Add assistant response to chat history
#   st.session_state.messages.append({"role": "assistant", "content": response})


# if prompt := st.chat_input("What is up?"):
#   message(prompt, is_user=True)
#   message(f"Echo: {prompt}")
