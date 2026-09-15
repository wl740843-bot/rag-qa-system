# parser.py
import pdfplumber
from docx import Document

def extract_text(file_path: str) -> str:
    """解析PDF或docx，返回全文文本"""
    text = ""
    if file_path.lower().endswith(".pdf"):
        with pdfplumber.open(file_path) as pdf:
            for page in pdf.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n"
    elif file_path.lower().endswith(".docx"):
        doc = Document(file_path)
        for para in doc.paragraphs:
            text += para.text + "\n"
    else:
        raise ValueError("仅支持 .pdf 和 .docx 文件")
    return text

if __name__ == "__main__":
    # 测试
    content = extract_text("test.pdf")
    print(content[:500])
