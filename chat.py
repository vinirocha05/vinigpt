import streamlit as st
import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")

client = OpenAI(api_key=api_key)


if "openai_model" not in st.session_state:
    st.session_state["openai_model"] = "gpt-4.1-mini"

st.set_page_config(layout="wide")
st.title("Vini GPT")

if "messages" not in st.session_state:
    st.session_state["messages"] = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("O que você gostaria de perguntar? "):
    with st.chat_message("user"):
        st.markdown(prompt)

    st.session_state.messages.append({"role": "user", "content": prompt})

    with st.chat_message("assistant"):
        response = client.chat.completions.create(
            model=st.session_state["openai_model"],
            messages=[
                {"role": m["role"], "content": m["content"]}
                for m in st.session_state.messages
            ],
        )
        resposta_assistente = response.choices[0].message.content
        st.markdown(resposta_assistente)

    st.session_state.messages.append(
        {"role": "assistant", "content": resposta_assistente}
    )
