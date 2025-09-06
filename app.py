import asyncio
import streamlit as st
from debate import TeamConfig, debate

st.set_page_config(page_title="Agents Debate!",page_icon="🤖")
st.title("Agents Debate!")

topic = st.text_input("Debate Topic","All people should have the right to own guns")

if 'running' not in st.session_state:
    st.session_state.running = False

start_col, _ = st.columns([1, 3])
with start_col:
    start = st.button("Start", type = "primary", disabled = st.session_state.running)

chat = st.container()

if start and not st.session_state.running:
    chat.empty()

    async def main():
        team = TeamConfig(topic)

        async for raw in debate(team):
            source, content = (raw.split(": ",) + [""])[:2]
            avatar = {"Jane": "🤖", "John": "👍🏼", "Jack": "👎🏼"}.get(source, "💬")
            with chat:
                with st.chat_message(name = source,avatar = avatar):
                    st.write(content)

    st.session_state.running = True
    try:
        with st.spinner("Runnging Debate..."):
            asyncio.run(main())
        st.balloons()
    except Exception as e:
        st.error(f"Error: {e}")
    finally:
        st.session_state.running = False
