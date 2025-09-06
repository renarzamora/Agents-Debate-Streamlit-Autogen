# 🤖 Agents Debate (Streamlit + AutoGen)

An interactive application that simulates a **debate between three AI agents**:  
- **Jane** (moderator/host)  
- **John** (supports the topic)  
- **Jack** (criticizes the topic)  

The interface is built with **Streamlit**, and team coordination is handled using **Microsoft AutoGen**.  
Each debate consists of 3 rounds and ends automatically when the host says **TERMINATE**.

---

## 🚀 Demo
https://www.youtube.com/watch?v=4WiN47BeDLs  

---

## 📦 Installation

Clone the repo and enter the directory:

```bash
git clone https://github.com/yourusername/agents-debate.git
cd agents-debate

---

Create a virtual environment (optional but recommended):
python3.12 -m venv .venv
source .venv/bin/activate

Install dependencies:
ip install -r requirements.txt

---

🔑 Configuration
Copy the example environment file and add your OpenAI API key:

bash
cp .env.example .env

Edit .env:

env
OPENAI_API_KEY=sk-xHEARxYOURxOPENAIxAPIxKEY

---

▶️ Usage
Run the app:

bash
streamlit run app.py

---

📂 Project Structure
Code
agents-debate/
├── app.py              # Streamlit UI
├── debate.py           # Agent setup and debate logic
├── requirements.txt    # Dependencies
├── .env.example        # Environment variable template
├── .gitignore
└── README.md

---

🛠️ Technologies
Streamlit – Fast Python UI

AutoGen – AI agent framework

OpenAI GPT-4o – Language model

---
app.py
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


---

📌 Roadmap(for you,go ahead!)
Save debate transcript in JSON/TXT

Allow model selection (gpt-4o, gpt-4.1, etc.)

Adjust temperature and response length

Add more agents (jury, audience, fact-checker)

---

📜 License
MIT

📄 .env.example
bash
# OpenAI API Key
OPENAI_API_KEY=sk-xHEARxYOURxOPENAIxAPIxKEY

---

📄 requirements.txt
Stable and recent versions (adjust if needed for compatibility):

txt
streamlit==1.37.0
python-dotenv==1.0.1
autogen-agentchat==0.2.25
autogen-ext==0.2.25
autogen-core==0.2.25

---

📄 .gitignore
txt
# Python
__pycache__/
*.pyc
*.pyo
*.pyd
.venv/
env/
venv/

# Streamlit
.streamlit/

# Secrets
.env

--- 
I hope you really enjoy it! - Renar
watch my git profile here https://www.linkedin.com/in/renar-arnoldo-zamora-54bb9024/
