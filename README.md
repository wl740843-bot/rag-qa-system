# RAG 文档问答系统

> 基于向量检索 + 大模型生成的 PDF 智能问答工具，支持中文文档理解与精准回答。

## 📖 项目简介

这是一个轻量级的 RAG（Retrieval-Augmented Generation，检索增强生成）系统。用户上传 PDF 文档后，可以用自然语言提问，系统会自动从文档中检索相关片段，并结合大模型生成准确、有依据的回答。

**核心价值：** 解决大模型"幻觉"问题 —— 所有回答都严格基于原文，不凭空编造。

## ✨ 核心功能

- **PDF 文本提取**：使用 `pdfplumber` 逐页解析 PDF，保留文字内容
- **滑动窗口切片**：按 300 字符切块，60 字符重叠，防止语义断裂
- **向量化嵌入**：使用 `sentence-transformers` 多语言模型，将文本转为向量
- **语义检索**：使用 FAISS 索引，毫秒级找到最相关的 Top-K 片段
- **大模型生成**：调用 DeepSeek API，基于检索到的原文生成简答
- **防幻觉机制**：Prompt 中强制要求"严格依据参考资料"，无相关内容时返回提示

## ️ 技术栈

| 模块 | 技术 | 说明 |
| :--- | :--- | :--- |
| PDF 解析 | pdfplumber | 逐页提取纯文本 |
| 文本切片 | 自定义滑动窗口 | chunk_size=300, overlap=60 |
| 向量嵌入 | sentence-transformers | paraphrase-multilingual-MiniLM-L12-v2 |
| 向量检索 | faiss-cpu | IndexFlatIP（内积相似度） |
| 大模型 | DeepSeek Chat API | temperature=0.1，保证回答稳定 |
| 网络加速 | hf-mirror.com | HuggingFace 国内镜像，解决下载超时 |

## 🚀 快速开始

### 1. 环境准备

```bash
# Python 3.8+
pip install pdfplumber sentence-transformers faiss-cpu requests
2. 配置 API Key
编辑 retriever.py，第 13 行填入你的 DeepSeek API Key：

python
复制
DEEPSEEK_API_KEY = "sk-xxxxxxxxxxxx"
3. 放入 PDF 文档
将你要问答的 PDF 文件命名为 test.pdf，放在项目根目录。

4. 修改问题并运行
编辑 retriever.py 第 85 行左右，修改你想问的问题：

python
复制
question = "++a 和 a++ 的区别"
然后运行：

bash
复制
python retriever.py
📊 输出示例
text
复制
PDF一共切出 42 个文本块

=======检索到的PDF原文片段=======

【片段1】
自增运算符 ++ 有两种形式：前缀 ++a 和后缀 a++。
前缀形式先自增再使用值，后缀形式先使用值再自增。
例如：int a=5; b=++a; 则 b=6, a=6；
      int a=5; b=a++; 则 b=5, a=6。

【片段2】
...（省略）

=======大模型整理答案=======
++a 是前缀自增，先加后用；a++ 是后缀自增，先用后加。
两者最终都会使变量值加1，但表达式的返回值不同。
🏗️ 工作流程
text
复制
用户提问
   ↓
向量嵌入 (sentence-transformers)
   ↓
FAISS 检索 (找到 Top-3 最相似片段)
   ↓
拼接 Prompt (问题 + 检索到的原文 + 防幻觉指令)
   ↓
DeepSeek 生成 (temperature=0.1)
   ↓
输出答案
📁 项目结构
text
复制
rag-qa-system/
├── chunker.py          # PDF 解析 + 滑动窗口切片逻辑
├── parser.py           # 辅助解析工具
├── retriever.py        # 主程序：向量检索 + 大模型问答
├── test.pdf             # 测试用 PDF 文档（C语言复习资料）
├── tests/
│   └── test_chunker.py # pytest 单元测试（13 条用例）
├── pytest.ini          # pytest 配置与自定义标记注册
├── requirements.txt   # 依赖清单
├── .gitignore          # Git 忽略规则
└── README.md           # 项目说明文档
## 🧪 单元测试

本项目使用 `pytest` 对核心模块 `chunker.py`（文本切分）编写了单元测试。

### 怎么跑

```bash
pip install -r requirements.txt
python -m pytest -v
```

### 覆盖的测试场景

| 场景 | 用例数 | 说明 |
| --- | --- | --- |
| 块数边界值 | 6 | 空输入 / 短文本 / 恰好步长 / 多 1 字 / 典型多块 / overlap=0 |
| 内容与重叠校验 | 2 | 短文本原样保留、相邻块 overlap 重叠 |
| PDF 解析（mock） | 2 | 多页拼接、空页跳过（monkeypatch 替换 pdfplumber） |
| 自设计用例 | 3 | 空输入 / 短文本 / 500 字长文本 |

### 用到的测试技术

- `@pytest.mark.parametrize`：数据驱动，一套代码跑多组数据
- `@pytest.mark.unit / .io`：自定义标记，可按 `-m unit` 筛选执行
- `monkeypatch`：mock 外部依赖（pdfplumber），不依赖真实 PDF 文件
- 边界值分析 / 反向（异常）测试思维

### 测试结果

```
============================= 13 passed in 0.72s =============================
```

⚠️ 注意事项
API Key 安全：请勿将真实 API Key 提交到公开仓库。本项目已移除硬编码 Key，使用前请自行配置。
首次运行较慢：首次运行会自动下载 Embedding 模型（约 120MB），后续运行会缓存。
国内网络优化：代码中已配置 HF_ENDPOINT=https://hf-mirror.com，解决 HuggingFace 下载超时问题。
PDF 质量影响效果：扫描版 PDF（图片型）无法提取文字，仅支持文字型 PDF。
切片大小可调：chunker.py 中的 chunk_size 和 overlap 可根据文档类型调整。
🔧 可改进方向
 支持 Web UI（Gradio / Streamlit）
 支持多种文档格式（Word、Markdown）
 引入重排序模型（Reranker）提升检索精度
 支持多轮对话，记住上下文
 添加评估模块，量化回答准确率
