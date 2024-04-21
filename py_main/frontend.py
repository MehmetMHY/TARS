import streamlit as st
import os
import main
from openai import OpenAI
import time

client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])
st.set_page_config(page_title="MEDUSA DEMO")
st.title('MEDUSA DEMO')
expect = ""
pingus = False
sys_prompt = "Pending..."

os.environ['WEBSITE'] = st.sidebar.text_input('Enter website to test here')

st.image(image="bingus.webp")
with st.form('my_form'):
    text = st.text_area('ASK THE TOOL TO RUN AN ATTACK!:', 'Enter text here')
    submitted = st.form_submit_button('Submit')  # This will return True when the form is submitted
    if submitted:  # Only run the following code if the form is submitted
        if not os.environ['WEBSITE']:
            st.warning('ENTER A WEBSITE BEFORE ATTEMPTING!', icon='⚠')
        else:
            pingus = True
            expect = main.npmgod.kickoff()
            st.warning("PROCESS HAS FINISHED:" + expect)  # Now this only runs when the form is submitted
            print(os.environ["WEBSITE"])
            sys_prompt = "You are a helpful cybersecurity analyst. Help the user understand the following network log output:" + expect


if "openai_model" not in st.session_state:
    st.session_state["openai_model"] = "gpt-4-turbo"

if "messages" not in st.session_state:
    st.session_state.messages = []
time.sleep(0.5)
st.session_state.messages.append({"role": "system", "content": sys_prompt})

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Ask about the commands executed"):
    
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        stream = client.chat.completions.create(
            model=st.session_state["openai_model"],
            messages=[
                {"role": m["role"], "content": m["content"]}
                for m in st.session_state.messages
            ],
            stream=True,
        )
        response = st.write_stream(stream)
    st.session_state.messages.append({"role": "assistant", "content": response})
      

 