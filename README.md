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

## 🛠️ 技术栈

| 模块 | 技术 | 说明 |
|---|---|---|
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

###2. 配置 API Key
编辑 retriever.py，第 13 行填入你的 DeepSeek API Key：
