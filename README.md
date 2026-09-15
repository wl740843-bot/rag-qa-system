# RAG 文档问答系统

基于向量检索的 PDF 智能问答系统。上传 PDF，用自然语言提问，系统自动检索相关片段并生成回答。

## 技术栈

- Python 3
- pdfplumber（PDF 解析）
- sentence-transformers（向量嵌入）
- faiss（向量检索）
- DeepSeek API（大模型生成）

## 快速开始

```bash
pip install pdfplumber sentence-transformers faiss-cpu requests
# 编辑 retriever.py 填入你的 DeepSeek API Key
python retriever.py