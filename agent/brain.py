import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.agents import create_tool_calling_agent, AgentExecutor

load_dotenv()  # reads keys from .env file

llm = ChatGroq(
    model="meta-llama/llama-4-scout-17b-16e-instruct",
    temperature=0,
    api_key=os.getenv("GROQ_API_KEY"),
)

prompt = ChatPromptTemplate.from_messages([
    ("system", """You are VulnScout, an autonomous AI security agent.

CRITICAL RULES:
- When asked to do multiple steps, call each tool one by one.
- NEVER skip a tool. If user says use cve_scorer, call it.
- When generating PDF, write YOUR OWN analysis in findings, not raw URLs.
- Complete ALL steps, never stop early.
- ONLY generate a PDF report if the user EXPLICITLY says "generate a PDF" or "create a report".
- For simple questions just answer directly without using any tools unless necessary.

WORKFLOW FOR SECURITY ANALYSIS:
1. web_search → get information
2. cve_scorer → score severity
3. mitre_mapper → map techniques
4. pdf_generator → ONLY when user asks for it
"""),
    MessagesPlaceholder(variable_name="chat_history", optional=True),
    ("human", "{input}"),
    MessagesPlaceholder(variable_name="agent_scratchpad"),
])

def build_agent(tools: list):
    agent = create_tool_calling_agent(
        llm=llm,
        tools=tools,
        prompt=prompt,
    )
    executor = AgentExecutor(
        agent=agent,
        tools=tools,
        verbose=True,
        max_iterations=15,
        handle_parsing_errors=True,
    )
    return executor