import streamlit as st
import sys
import os
import requests
from pathlib import Path
from langchain_core.messages import HumanMessage, AIMessage

# ==================== 第一部分：环境变量全流程异常捕获 ====================
try:
    # 1. 捕获dotenv依赖缺失异常
    from dotenv import load_dotenv
except ImportError:
    print(" 依赖缺失：请先安装 python-dotenv，执行命令：pip install python-dotenv")
    sys.exit(1)

try:
    # 2. 加载.env文件，捕获文件不存在/格式错误异常
    load_result = load_dotenv(encoding="utf-8")
    if not load_result:
        print("  警告：未在项目根目录找到 .env 配置文件")
    
    # 3. 提取并校验核心配置项
    DASHSCOPE_API_KEY = os.getenv("DASHSCOPE_API_KEY")
    USER_ID = os.getenv("USER_ID")

    if not DASHSCOPE_API_KEY or DASHSCOPE_API_KEY.strip() == "":
        raise ValueError("DASHSCOPE_API_KEY 未配置或为空，请在 .env 文件中填写有效的通义千问API密钥")
    
    if not USER_ID or USER_ID.strip() == "":
        raise ValueError("USER_ID 未配置或为空，请在 .env 文件中填写用户唯一标识")

    # 4. 校验通过，注入全局环境变量
    os.environ["DASHSCOPE_API_KEY"] = DASHSCOPE_API_KEY.strip()
    os.environ["USER_ID"] = USER_ID.strip()
    print(" 环境变量加载校验成功")

except Exception as e:
    error_msg = f"环境配置失败：{str(e)}"
    print(f" {error_msg}")
    
    # 适配Streamlit界面可视化报错
    try:
        st.error(error_msg)
    except:
        pass
    sys.exit(1)

# 读取用户专属ID（已在上面校验过，这里直接取）
USER_ID = os.getenv("USER_ID")

# ==================== 第二部分：导入Agent核心 ====================
try:
    from agent import graph
except Exception as e:
    st.error(f"导入Agent失败：{str(e)}，请检查 agent.py 文件是否存在且无语法错误")
    st.stop()

# ==================== 第三部分：页面配置与初始化 =====================
st.set_page_config(
    page_title="AI 技术学习助手",
    layout="wide"
)

if "messages" not in st.session_state:
    st.session_state.messages = []

st.title("AI 技术学习助手")
st.markdown("---")

# 显示历史对话
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# ==================== 第四部分：核心对话逻辑（含通用异常捕获） ====================
if prompt := st.chat_input("输入你的问题..."):
    # 1. 显示用户输入
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # 2. 调用 Agent（含异常捕获）
    with st.chat_message("assistant"):
        with st.spinner("正在思考..."):
            config = {
                "configurable": {
                    "user_id": USER_ID,
                    "thread_id": "thread1"
                }
            }
            
            response_placeholder = st.empty()
            full_response = ""

            try:
                # 【原有核心流式调用逻辑，完整保留】
                for chunk in graph.stream(
                    {"messages": [HumanMessage(content=prompt)]},
                    config=config
                ):
                    for node, data in chunk.items():
                        if data and isinstance(data, dict) and "messages" in data:
                            last_msg = data["messages"][-1]
                            if isinstance(last_msg, AIMessage) and last_msg.content:
                                full_response += last_msg.content
                                response_placeholder.markdown(full_response + "▌")

                # 最终显示完整回复
                response_placeholder.markdown(full_response)

            # 【通用异常捕获（兼容所有版本，不依赖特定导入）】
            except Exception as e:
                error_str = str(e).lower()
                error_tips = {
                    "invalidapikey": "API密钥无效，请检查 .env 中的 DASHSCOPE_API_KEY 是否正确",
                    "apikeyexpired": "API密钥已过期，请前往阿里云控制台更换密钥",
                    "insufficientquota": "API配额/余额不足，请查看控制台剩余额度",
                    "throttling": "请求被限流，请稍后再试",
                    "modelnotfound": "模型名称配置错误，请检查模型参数",
                    "connection": "网络连接失败，请检查网络环境、代理设置",
                    "timeout": "请求超时，请稍后重试"
                }

                final_tip = "对话处理失败，请稍后重试"
                for key, tip in error_tips.items():
                    if key in error_str:
                        final_tip = tip
                        break
                
                if final_tip == "对话处理失败，请稍后重试":
                    final_tip = f"对话处理失败：{str(e)}"

                response_placeholder.error(final_tip)
                full_response = f"[请求失败] {final_tip}"
                print(f"对话异常详情：{str(e)}")
        
    # 3. 保存回复到会话状态
    st.session_state.messages.append({"role": "assistant", "content": full_response})


    # 终端输入测试  streamlit run app.py