# 🛡️ VulnScout — Autonomous AI Security Agent

> An AI-powered security agent that researches CVEs, scores severity, maps MITRE ATT&CK techniques, runs code, and generates PDF reports — all autonomously. Runs 100% locally or via free cloud API. Zero cost.

![Python](https://img.shields.io/badge/Python-3.11-blue?style=flat-square&logo=python)
![LangChain](https://img.shields.io/badge/LangChain-0.3.25-green?style=flat-square)
![Streamlit](https://img.shields.io/badge/Streamlit-UI-red?style=flat-square&logo=streamlit)
![Groq](https://img.shields.io/badge/Groq-LLM-orange?style=flat-square)
![License](https://img.shields.io/badge/License-MIT-yellow?style=flat-square)

---

## 📌 What is VulnScout?

VulnScout is a **mini Security Operations Center (SOC) assistant** powered by AI. Instead of a SOC analyst spending hours manually researching threats, VulnScout does it autonomously in seconds.

Give it a task like:
> *"Search for CVE-2024-3094, score its severity, map it to MITRE ATT&CK, and generate a PDF report"*

VulnScout will:
1. 🔍 Search the web for real threat intelligence
2. 📊 Score the CVE severity (LOW / MEDIUM / HIGH / CRITICAL)
3. 🎯 Map it to MITRE ATT&CK technique IDs
4. 📄 Generate a professional PDF report
5. 💻 Write and execute code if needed

All autonomously. No human intervention.

---

## ✨ Features

| Feature | Description |
|---|---|
| 🔍 **Web Search** | Real-time threat intelligence via Tavily API |
| 💻 **Code Runner** | Writes and executes Python code in a local sandbox |
| 📊 **CVE Scorer** | Auto-rates CVE severity — LOW to CRITICAL |
| 🎯 **MITRE ATT&CK Mapper** | Maps threats to T-codes (T1566, T1190, etc.) |
| 📄 **PDF Report Generator** | Generates professional security reports |
| 📁 **File Reader/Writer** | Reads uploaded files, saves reports locally |
| 🔄 **ReAct Loop** | Agent reasons, acts, observes, and iterates |
| 🖥️ **Streamlit UI** | Clean web interface with live thought stream |

---

## 🏗️ Architecture

```
User Task
    │
    ▼
┌─────────────────────┐
│   Agent Brain       │  ← Llama 4 via Groq API
│   (ReAct Loop)      │
└────────┬────────────┘
         │ thinks → picks tool → observes → repeats
         ▼
┌─────────────────────────────────────────────┐
│              Tool Library                   │
│  web_search │ code_runner │ cve_scorer      │
│  mitre_mapper │ pdf_generator │ file_reader │
└─────────────────────────────────────────────┘
         │
         ▼
┌─────────────────────┐
│   Streamlit UI      │  ← localhost:8501
│   Live thought log  │
└─────────────────────┘
```

---

## 🛠️ Tech Stack

| Area | Technology |
|---|---|
| Language | Python 3.11 |
| Agent Framework | LangChain 0.3.25 |
| LLM | Llama 4 Scout via Groq API (free) |
| Web Search | Tavily API (free tier) |
| UI | Streamlit |
| PDF Generation | ReportLab |
| Local LLM (optional) | Ollama |
| Vector Memory | ChromaDB |

---

## 🚀 Getting Started

### Prerequisites
- Python 3.11+
- Free [Groq API key](https://console.groq.com) 
- Free [Tavily API key](https://app.tavily.com)

### Installation

**1. Clone the repo**
```bash
git clone https://github.com/Sai-teja-007/vulnscout.git
cd vulnscout
```

**2. Create virtual environment**
```bash
python -m venv venv
venv\Scripts\activate  # Windows
```

**3. Install dependencies**
```bash
pip install -r requirements.txt
```

**4. Add your API keys**

Open `agent/brain.py` and add your Groq key:
```python
api_key="your_groq_key_here"
```

Open `tools/web_search.py` and add your Tavily key:
```python
api_key="your_tavily_key_here"
```

**5. Run VulnScout**
```bash
python -m streamlit run app.py
```

Open `http://localhost:8501` in your browser.

---

## 💡 Example Tasks

```
Search for CVE-2024-3094 and explain how dangerous it is
```
```
Use code_runner to write a Python port scanner for localhost
```
```
Search for CVE-2024-3094, score severity, map to MITRE, generate PDF report
```
```
Write a Python function to detect SQL injection patterns and test it
```

---

## 📁 Project Structure

```
vulnscout/
├── app.py                  # Streamlit UI
├── requirements.txt        # Dependencies
├── .env                    # Environment variables
├── agent/
│   ├── brain.py            # LLM + ReAct agent loop
│   └── __init__.py
├── tools/
│   ├── web_search.py       # Tavily web search
│   ├── code_runner.py      # Python sandbox executor
│   ├── cve_scorer.py       # CVE severity scorer
│   ├── mitre_mapper.py     # MITRE ATT&CK mapper
│   ├── pdf_generator.py    # PDF report generator
│   └── file_reader.py      # File read/write
├── uploads/                # User uploaded files
└── reports/                # Generated PDF reports
```

---

## 🔒 Privacy & Security

- **Local execution** — all code runs on your machine
- **No data stored** — nothing is saved to external servers
- **Offline mode** — switch to Ollama for fully air-gapped usage
- **Open source** — full transparency, no hidden logic

---

## 🗺️ Roadmap

- [ ] Multi-agent mode with CrewAI
- [ ] Real-time CVE feed monitoring
- [ ] Slack/email alerting
- [ ] Docker deployment
- [ ] NVD API direct integration

---

## 👨‍💻 Author

**SAITEJA**  
GitHub: [@Sai-teja-007](https://github.com/Sai-teja-007)

---

## 📄 License

MIT License — free to use, modify, and distribute.

---

> ⭐ If you found this useful, give it a star on GitHub!
