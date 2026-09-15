import os
# 关闭symlink的蓝色警告
os.environ["HF_HUB_DISABLE_SYMLINKS_WARNING"] = "1"
# HuggingFace国内镜像，解决下载超时
os.environ['HF_ENDPOINT'] = 'https://hf-mirror.com'

from sentence_transformers import SentenceTransformer
import faiss
import numpy as np
import requests

# ===================== DeepSeek API 配置，这里填你的key =====================
DEEPSEEK_API_KEY = "你的DeepSeek API Key"  # 请填入你自己的 Key
DEEPSEEK_URL = "https://api.deepseek.com/v1/chat/completions"
# ==========================================================================

# 中文多语言Embedding模型，适配你的C语言复习PDF
model = SentenceTransformer('paraphrase-multilingual-MiniLM-L12-v2')

class VectorRetriever:
    def __init__(self, embed_model):
        self.embed_model = embed_model
        self.index = None
        self.chunks = []

    def build_index(self, text_chunks: list[str]):
        self.chunks = text_chunks
        embeddings = self.embed_model.encode(text_chunks, convert_to_numpy=True, normalize_embeddings=True)
        dim = embeddings.shape[1]
        self.index = faiss.IndexFlatIP(dim)
        self.index.add(embeddings)

    def search(self, query: str, top_k=3):
        query_emb = self.embed_model.encode([query], convert_to_numpy=True, normalize_embeddings=True)
        scores, ids = self.index.search(query_emb, top_k)
        result = [self.chunks[i] for i in ids[0]]
        return result


def llm_answer(question, context_text):
    """调用DeepSeek，根据检索到的文档片段回答问题"""
    prompt = f"""
你是C语言考试助教，请**严格依据下面参考资料内容**回答用户问题。
如果资料没有相关内容，直接回答：文档中没有该知识点。
回答简洁，适合简答题作答。

【参考资料】
{context_text}

【用户问题】
{question}
"""
    headers = {
        "Authorization": f"Bearer {DEEPSEEK_API_KEY}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": "deepseek-chat",
        "messages": [
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.1
    }
    resp = requests.post(DEEPSEEK_URL, headers=headers, json=payload)
    res_json = resp.json()
    return res_json["choices"][0]["message"]["content"]


if __name__ == "__main__":
    from chunker import load_pdf, split_text
    retriever = VectorRetriever(model)

    # 读取test.pdf
    pdf_text = load_pdf("test.pdf")
    test_chunks = split_text(pdf_text)
    print(f"PDF一共切出 {len(test_chunks)} 个文本块\n")

    retriever.build_index(test_chunks)

    # =========在这里修改你的C语言提问=========
    question = "++a 和 a++ 的区别"
    # question = "break和continue区别"
    # question = "指针p和*p的区别"

    # 1.向量检索
    chunks_res = retriever.search(question, top_k=3)
    print("=======检索到的PDF原文片段=======")
    all_context = ""
    for idx, c in enumerate(chunks_res, 1):
        print(f"\n【片段{idx}】")
        print(c)
        print("-" * 60)
        all_context += c + "\n"

    # 2.交给大模型生成简答答案
    print("\n=======大模型整理答案=======")
    ans = llm_answer(question, all_context)
    print(ans)
