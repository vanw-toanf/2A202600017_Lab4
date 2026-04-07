import sys
import os
import re

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from typing import Annotated
from pathlib import Path
from typing_extensions import TypedDict
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from langgraph.prebuilt import ToolNode, tools_condition
from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage
from tools.tool import search_flights, search_hotels, calculate_budget
from dotenv import load_dotenv

load_dotenv()

# 1. Đọc System Prompt
ROOT_DIR = Path(__file__).resolve().parent.parent
with open(ROOT_DIR / "system_prompt.txt", "r", encoding="utf-8") as f:
    SYSTEM_PROMPT = f.read()

# 2. Khai báo State
class AgentState(TypedDict):
    messages: Annotated[list, add_messages]

# 3. Khởi tạo LLM và Tools
tools_list = [search_flights, search_hotels, calculate_budget]
llm = ChatOpenAI(model="gpt-4o-mini")
llm_with_tools = llm.bind_tools(tools_list)


def _message_content_to_text(content) -> str:
    if isinstance(content, str):
        return content
    if isinstance(content, list):
        parts = []
        for item in content:
            if isinstance(item, dict) and item.get("type") == "text":
                parts.append(str(item.get("text", "")))
            else:
                parts.append(str(item))
        return " ".join(parts)
    return str(content)


def _latest_user_text(messages: list) -> str:
    for message in reversed(messages):
        if isinstance(message, tuple) and len(message) >= 2:
            role = str(message[0]).lower()
            if role in {"human", "user"}:
                return str(message[1])

        message_type = getattr(message, "type", "")
        if message_type in {"human", "user"}:
            return _message_content_to_text(getattr(message, "content", ""))
    return ""


def _is_budget_related(text: str) -> bool:
    if not text:
        return False
    normalized = text.lower().strip()
    patterns = [
        r"\bbudget\b",
        r"\bbuget\b",
        r"ngân\s*sách",
        r"chi\s*phí",
        r"tổng\s*chi",
        r"bao\s*nhiêu\s*tiền",
        r"vượt\s*ngân\s*sách",
    ]
    return any(re.search(pattern, normalized) for pattern in patterns)


def _has_tool_call(response, tool_name: str) -> bool:
    return any(tool_call.get("name") == tool_name for tool_call in (response.tool_calls or []))

# 4. Agent Node
def agent_node(state: AgentState):
    messages = state.get("messages", [])
    if not messages:
        return {"messages": []}

    if not isinstance(messages[0], SystemMessage):
        messages = [SystemMessage(content=SYSTEM_PROMPT)] + messages
    
    latest_user_text = _latest_user_text(messages)
    response = llm_with_tools.invoke(messages)

    if _is_budget_related(latest_user_text) and not _has_tool_call(response, "calculate_budget"):
        force_budget_instruction = SystemMessage(
            content=(
                "Yêu cầu bắt buộc: nếu người dùng đề cập ngân sách/chi phí (kể cả viết sai như 'buget'), "
                "bạn phải gọi tool calculate_budget trước khi trả lời cuối. "
                "Nếu thiếu dữ liệu thành phần, hãy gọi tool cần thiết để lấy dữ liệu rồi gọi calculate_budget."
            )
        )
        response = llm_with_tools.invoke(messages + [force_budget_instruction])
    
    # === LOGGING ===
    if response.tool_calls:
        for tc in response.tool_calls:
            print(f"Gọi tool: {tc['name']}({tc['args']})")
    else:
        print(f"Trả lời trực tiếp")
        
    return {"messages": [response]}

# 5. Xây dựng Graph
builder = StateGraph(AgentState)
builder.add_node("agent", agent_node)

tool_node = ToolNode(tools_list)
builder.add_node("tools", tool_node)

# TODO: Sinh viên khai báo edges
builder.add_edge(START, "agent")
builder.add_conditional_edges("agent", tools_condition, {"tools": "tools", "__end__": END})
builder.add_edge("tools", "agent")

graph = builder.compile()

# 6. Chat loop
if __name__ == "__main__":
    print("=" * 60)
    print("TravelBuddy – Trợ lý Du lịch Thông minh")
    print("      Gõ 'quit' để thoát")
    print("=" * 60)
    
    while True:
        user_input = input("\nBạn: ").strip()
        if user_input.lower() in ("quit", "exit", "q"):
            break
            
        print("\nTravelBuddy đang suy nghĩ...")
        result = graph.invoke({"messages": [("human", user_input)]})
        final = result["messages"][-1]
        print(f"\nTravelBuddy: {final.content}")

