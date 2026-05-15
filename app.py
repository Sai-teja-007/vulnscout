import streamlit as st
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from agent.brain import build_agent
from tools.web_search import web_search
from tools.code_runner import code_runner
from tools.file_reader import file_reader
from tools.file_writer import file_writer
from tools.pdf_generator import pdf_generator
from tools.cve_scorer import cve_scorer
from tools.mitre_mapper import mitre_mapper

st.set_page_config(page_title="VulnScout", page_icon="🛡️", layout="wide")

st.title("🛡️ VulnScout")
st.caption("Autonomous AI security agent — researches CVEs, analyzes threats, scores severity, maps MITRE, generates PDFs. 100% local · zero cost")

with st.sidebar:
    st.markdown("### 🛡️ VulnScout")
    st.caption("Your local AI security analyst")
    st.divider()
    st.header("🛠️ Active Tools")
    st.success("✅ Web Search (DuckDuckGo)")
    st.success("✅ Code Runner (Python sandbox)")
    st.success("✅ File Reader")
    st.success("✅ File Writer")
    st.success("✅ PDF Report Generator")
    st.success("✅ CVE Severity Scorer")
    st.success("✅ MITRE ATT&CK Mapper")
    st.divider()
    st.header("📂 Upload a file")
    uploaded = st.file_uploader("Upload .txt, .py, .log, .csv", type=["txt","py","log","csv","md"])
    if uploaded:
        save_path = os.path.join("uploads", uploaded.name)
        os.makedirs("uploads", exist_ok=True)
        with open(save_path, "wb") as f:
            f.write(uploaded.getbuffer())
        st.success(f"Saved: uploads/{uploaded.name}")
        st.info(f"Tell the agent: 'Read the file uploads/{uploaded.name}'")

@st.cache_resource
def get_agent():
    tools = [web_search, code_runner, file_reader, file_writer, pdf_generator, cve_scorer, mitre_mapper]
    return build_agent(tools)

agent = get_agent()

if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

EXAMPLES = [
    "Search for CVE-2024-3094, score its severity, map it to MITRE, and generate a PDF report",
    "Search for the latest critical CVE and create a professional PDF report with findings",
    "Find threats related to phishing, score them, and map to MITRE ATT&CK techniques",
    "Analyze a security threat and provide MITRE technique mappings with recommendations",
]

st.markdown("**💡 Try an example task:**")
cols = st.columns(2)
for i, example in enumerate(EXAMPLES):
    if cols[i % 2].button(example, key=f"ex_{i}"):
        st.session_state["prefill"] = example

user_input = st.chat_input("Give VulnScout a task...")

if "prefill" in st.session_state and st.session_state["prefill"]:
    user_input = st.session_state.pop("prefill")

if user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    with st.chat_message("assistant"):
        with st.status("🧠 VulnScout is thinking...", expanded=True) as status:
            try:
                # Simple agent invocation without callbacks
                result = agent.invoke({"input": user_input})
                final_answer = result.get("output", "Agent did not return an answer.")
                status.update(label="✅ Done!", state="complete")

            except Exception as e:
                final_answer = f"Something went wrong:\n\n```\n{str(e)}\n```"

        st.markdown(final_answer)

    st.session_state.messages.append({"role": "assistant", "content": final_answer})