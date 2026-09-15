import pdfplumber

def load_pdf(path: str) -> str:
    """读取PDF全部文字"""
    full_text = ""
    with pdfplumber.open(path) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text()
            if page_text:
                full_text += page_text
    return full_text

def split_text(text: str, chunk_size=300, overlap=60) -> list[str]:
    """文本切块，带重叠"""
    chunks = []
    start = 0
    while start < len(text):
        end = start + chunk_size
        chunk = text[start:end]
        chunks.append(chunk)
        start += chunk_size - overlap
    return chunks

if __name__ == "__main__":
    text = load_pdf("test.pdf")
    chunks = split_text(text)
    print(f"一共切出 {len(chunks)} 个文本块")
    for c in chunks[:3]:
        print(c)
        print("-"*30)
