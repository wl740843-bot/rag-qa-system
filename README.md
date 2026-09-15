# RAG 文档问答系统
基于向量检索的 PDF 智能问答系统。上传 PDF，用自然语言提问，系统自动检索文档相关片段并生成回答。

## 技术栈
- Python 3
- pdfplumber：PDF文本解析
- sentence-transformers：文本向量嵌入
- faiss-cpu：向量相似度检索
- DeepSeek API：大模型答案生成

## 项目原理
本项目是一个轻量级检索增强生成（RAG）应用，完整流程：
1. **文档解析**：使用 pdfplumber 读取 PDF，提取文档内全部文本内容
2. **文本分块**：将长文本切分为固定大小的文本块，支持块重叠，避免语义被截断
3. **向量化**：通过 sentence-transformers 将文本块转为向量，存入 Faiss 内存向量库
4. **问题检索**：用户提问后，把问题转为向量，在向量库召回最相关的文本片段
5. **提示词组装**：将检索到的上下文片段 + 用户问题，构造提示词提交给 DeepSeek
6. **答案生成**：大模型基于提供的文档上下文生成答案，减少模型幻觉

## 目录结构
rag-qa-system/
├── .gitignore          # Git 忽略文件配置
├── README.md           # 项目说明文档
├── parser.py           # PDF 解析模块，提取 PDF 文本
├── chunker.py          # 文本分块模块，长文本切分
├── retriever.py        # 向量库构建、检索、调用 DeepSeek API 主逻辑
├── test.pdf            # 测试用 PDF 文件
└── .env                # 环境变量文件（存放 API 密钥，不上传 git）

## 快速开始
### 1. 安装依赖
```bash
pip install pdfplumber sentence-transformers faiss-cpu requests python-dotenv
### 2. 配置密钥

在项目根目录新建 `.env` 文件，写入 DeepSeek API Key：

```
DEEPSEEK_API_KEY=你的DeepSeek密钥
```

> 
> 密钥不会硬编码到代码中，`.env` 已加入 `.gitignore`，防止密钥泄露。

### 3. 运行项目

```
python retriever.py
```
