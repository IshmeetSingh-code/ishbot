import streamlit as st
from config import PAGE_TITLE, PAGE_ICON, PERSONAS, DEFAULT_PERSONA
from core import router, chat, code, search

st.set_page_config(page_title=PAGE_TITLE, page_icon=PAGE_ICON, layout="centered")

MODE_BADGES = {
    "chat": "💬 Chat",
    "code": "🐍 Python REPL",
    "search": "🔍 Web Search",
}

with st.sidebar:
    st.title(f"{PAGE_ICON} {PAGE_TITLE}")
    persona_name = st.selectbox(
        "Persona",
        list(PERSONAS.keys()),
        index=list(PERSONAS.keys()).index(DEFAULT_PERSONA),
        format_func=lambda k: f"{PERSONAS[k]['icon']} {k} — {PERSONAS[k]['tagline']}",
    )
    persona = PERSONAS[persona_name]
    st.divider()
    st.markdown("**Tools**")
    st.markdown("🔢 Calculator &nbsp;·&nbsp; 🐍 Python REPL &nbsp;·&nbsp; 🔍 Web Search")
    st.divider()
    if st.button("🗑️ Clear Chat", use_container_width=True):
        st.session_state.messages = []
        st.session_state.chat_session = None
        st.rerun()
    st.divider()
    st.caption("Built by Ishmeet Singh")

if "messages" not in st.session_state:
    st.session_state.messages = []
if "chat_session" not in st.session_state:
    st.session_state.chat_session = None
if "active_persona" not in st.session_state:
    st.session_state.active_persona = None

if st.session_state.active_persona != persona_name:
    st.session_state.chat_session = None
    st.session_state.active_persona = persona_name

st.title(f"{persona['icon']} {persona_name}")
st.caption(persona["tagline"])

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        if msg.get("mode"):
            st.caption(MODE_BADGES.get(msg["mode"], ""))
        st.markdown(msg["content"])

if prompt := st.chat_input("Ask anything..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            mode = router.classify(prompt)
        st.caption(MODE_BADGES.get(mode, ""))
        try:
            if mode == "code":
                with st.spinner("Running code..."):
                    result = code.execute(prompt, persona["instruction"])
                response_text = ""
                if result["text"]:
                    st.markdown(result["text"])
                    response_text += result["text"]
                if result["code"]:
                    st.code(result["code"], language="python")
                    response_text += f"\n```python\n{result['code']}\n```"
                if result["output"]:
                    st.text(f"Output: {result['output']}")
                    response_text += f"\nOutput: {result['output']}"
                if not response_text:
                    response_text = "Code execution completed."
                    st.markdown(response_text)
            elif mode == "search":
                with st.spinner("Searching..."):
                    response_text = search.query(prompt, persona["instruction"])
                st.markdown(response_text)
            else:
                if st.session_state.chat_session is None:
                    st.session_state.chat_session = chat.create_session(persona["instruction"])
                response_text = st.write_stream(chat.stream(st.session_state.chat_session, prompt))
        except Exception as exc:
            response_text = f"Error: {exc}"
            st.error(response_text)
        st.session_state.messages.append({"role": "assistant", "content": response_text, "mode": mode})
