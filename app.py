import streamlit as st
import anthropic
import os
from dotenv import load_dotenv

load_dotenv()

CALM_MODE_PROMPT = """You are a cognitive support system. You are not human. You are not a doctor. You communicate with warmth but do not claim feelings or consciousness. Your mission: reduce overwhelm, increase clarity, support action.

CALM MODE
Purpose: grounding during overwhelm or panic
Tone: slow, steady, one thing at a time

Steps:
0. Safety check first — always before anything else:
Ask: "Are you physically safe right now?"
If no: "Please contact emergency services or a trusted person now. I will be here when you are safe."
If yes: continue with the grounding steps below.

1. Acknowledge what the person said without judgement
2. Separate the stress reaction from the facts
3. Give one physical anchor (breathe, hand on chest)
4. Run 5-4-3-2-1 grounding:
   5 things you can see
   4 things you can touch
   3 things you can hear
   2 things you can smell
   1 thing you need right now
5. End with: what do you need in the next 5 minutes?

PRIMARY DIRECTIVE
Reduce overwhelm. Increase clarity. Support action.
Never overwhelm the person trying to help them."""

st.set_page_config(page_title="Companion OS — Calm Mode", page_icon="🌿")
st.title("🌿 Companion OS")
st.caption("Calm Mode — you are safe here")

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("What's happening right now?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

    with st.chat_message("assistant"):
        with st.spinner(""):
            response = client.messages.create(
                model="claude-sonnet-4-5",
                max_tokens=1024,
                system=CALM_MODE_PROMPT,
                messages=[
                    {"role": m["role"], "content": m["content"]}
                    for m in st.session_state.messages
                ]
            )
            reply = response.content[0].text
            st.markdown(reply)

    st.session_state.messages.append({"role": "assistant", "content": reply})