#  AI 技术学习助手 | AI Agent Demo
基于 **LangGraph + 通义千问** 构建的智能对话 Agent，内置 **RAG 知识库**、**长期记忆** 能力，搭配 **Streamlit** 可视化前端界面，开箱即用。

---

##  核心功能亮点
-  **智能对话 Agent**：基于 LangGraph 状态图构建的可观测 Agent 流程，支持自动工具调用
-  **RAG 知识库问答**：基于 Chroma 向量库，支持 PDF 等文档的知识库检索，精准回答深度学习等相关AI专业问题
-  **长期记忆系统**：自动提取对话记忆，持久化存储到向量库，跨对话保留用户偏好与历史信息
-  **流式输出体验**：打字机效果，实时展示 AI 回复，支持工具调用状态可视化
-  **简洁可视化界面**：基于 Streamlit 搭建的聊天界面，零门槛上手使用

---

##  环境准备
- Python 3.10+
- 阿里云通义千问 API 密钥（获取地址：https://dashscope.console.aliyun.com/）

---

##  快速启动

### 1. 克隆项目
```
git clone https://github.com/haikang123/AI-agent-demo.git
cd AI-agent-demo
```

### 2. 安装依赖
```
pip install -r requirements.txt
```

### 2. 安装依赖
```
pip install -r requirements.txt
```

### 3. 配置说明
在项目根目录新建 .env 文件，填写：
```
DASHSCOPE_API_KEY="你的API密钥"
```

### 4. 项目启动
```
streamlit run app.py
```

### 5. 项目结构
```
AI-agent-demo/
├── agent.py            # Agent 核心逻辑
├── app.py              # Streamlit 前端界面
├── requirements.txt    # 项目依赖列表
├── .gitignore          # Git 忽略配置
├── .env                # 环境变量配置（自行创建）
├── docs/               # RAG 知识库文档目录
├── chroma_rag_db/      # RAG 向量库（自动生成）
├── chroma_memory_db/   # 长期记忆向量库（自动生成）
└── cache/              # 向量嵌入缓存（自动生成）
```
