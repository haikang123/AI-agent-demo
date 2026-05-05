import streamlit as st
import sys
from pathlib import Path
import os
# 加载 .env 配置
from dotenv import load_dotenv
load_dotenv()

#读取用户专属ID
USER_ID = os.getenv("USER_ID", "user_default")
# ==================== 关键：导入你的 agent.py 里的核心对象 ====================
# 这里假设 agent.py 和 app.py 在同一个文件夹
from agent import graph, HumanMessage, AIMessage

# ==================== 页面配置 ====================
st.set_page_config(
    page_title="AI 技术学习助手",
    page_icon="",
    layout="wide"
)

# ==================== 初始化会话状态（仅保留对话历史显示）====================
if "messages" not in st.session_state:
    st.session_state.messages = []

# ==================== 页面标题 ====================
st.title(" AI 技术学习助手")
st.markdown("---")

# ==================== 显示历史对话 ====================
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# ==================== 核心：用户输入 , 调用Agent ====================
if prompt := st.chat_input("输入你的问题..."):
    # 1. 显示用户输入
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # 2. 调用 Agent
    with st.chat_message("assistant"):
        with st.spinner("正在思考..."):
            config = {
                "configurable": {
                    "user_id": USER_ID,  # 使用你的专属ID
                    "thread_id": "thread1"
                }
            }
            
            # 初始化占位符，用于流式显示
            response_placeholder = st.empty()
            full_response = ""

            # 调用 agent
            for chunk in graph.stream(
                {"messages": [HumanMessage(content=prompt)]},
                config=config
            ):
                # 解析流式输出
                for node, data in chunk.items():
                    # 先判断 data 是否存在且不为空
                    if data and isinstance(data, dict) and "messages" in data:
                        last_msg = data["messages"][-1]
                        if isinstance(last_msg, AIMessage) and last_msg.content:
                            full_response += last_msg.content
                            response_placeholder.markdown(full_response + "▌")

            # 最终显示完整回复（去掉光标）
            response_placeholder.markdown(full_response)
    
    # 3. 保存回复到会话状态（仅用于前端显示，记忆实际已存向量库）
    st.session_state.messages.append({"role": "assistant", "content": full_response})

# 终端输入测试  streamlit run app.py