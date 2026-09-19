"""
chunker.py 测试 —— 第一个 pytest 练习项目（软件测试方向第 1 周）

本文件用到的知识点（对照你的笔记）：
- @pytest.mark.parametrize : 数据驱动，一套代码跑多组数据
- @pytest.mark.unit / .io   : 自定义标记（已在 pytest.ini 注册），可用 pytest -m unit 单独跑
- monkeypatch              : mock 掉 pdfplumber，不依赖真实 PDF 文件就能测 load_pdf
- 边界值分析               : 空输入 / 短于块 / 恰好等于 / 多 1 个字 / 典型多块
- 反向（异常）测试         : 空输入、空页 —— 验证程序不会直接崩
"""
import pytest
import chunker


# ========== 一、split_text 块数：边界值 + 数据驱动 ==========

@pytest.mark.unit
@pytest.mark.parametrize(
    "text, chunk_size, overlap, expected_count",
    [
        pytest.param("", 300, 60, 0, id="空输入→0块（反向测试）"),
        pytest.param("短文本", 300, 60, 1, id="短于步长→1块"),
        # 步长 = chunk_size - overlap = 240，真正的边界是步长，不是块大小 300
        pytest.param("x" * 240, 300, 60, 1, id="恰好=步长240→1块"),
        pytest.param("x" * 241, 300, 60, 2, id="步长241→触发第2块（真正边界值）"),
        pytest.param("x" * 600, 300, 60, 3, id="600字→3块"),
        pytest.param("x" * 301, 300, 0, 2, id="overlap=0，多1字→2块"),
    ],
)
def test_chunk_count(text, chunk_size, overlap, expected_count):
    chunks = chunker.split_text(text, chunk_size, overlap)
    assert len(chunks) == expected_count


# ========== 二、短文本：切出来的内容应该原样保留 ==========

@pytest.mark.unit
def test_short_text_kept_verbatim():
    chunks = chunker.split_text("Hello世界", chunk_size=300, overlap=60)
    assert chunks == ["Hello世界"]


# ========== 三、相邻块之间：应该有 overlap 个字符重叠 ==========

@pytest.mark.unit
def test_overlap_between_adjacent_chunks():
    text = "x" * 600
    chunks = chunker.split_text(text, chunk_size=300, overlap=60)
    assert len(chunks) == 3
    # 第 1 块结尾 60 个字符，应该等于第 2 块开头 60 个字符（重叠区）
    assert chunks[0][-60:] == chunks[1][:60]


# ========== 四、load_pdf：mock 掉 pdfplumber，验证多页拼接 ==========
# 不依赖真实 PDF 文件，用假对象模拟 pdfplumber 的返回，这就是 mock 的思路。

class FakePage:
    """模拟 pdfplumber 的一页"""

    def __init__(self, text):
        self._text = text

    def extract_text(self):
        return self._text


class FakePdf:
    """模拟 pdfplumber.open() 返回的上下文管理器"""

    def __init__(self, pages):
        self.pages = pages

    def __enter__(self):
        return self

    def __exit__(self, *args):
        return False


@pytest.mark.io
def test_load_pdf_concatenates_pages(monkeypatch):
    fake = FakePdf([FakePage("第一页"), FakePage("第二页")])
    # 把 chunker 模块里的 pdfplumber.open 换成我们的假返回
    monkeypatch.setattr(chunker.pdfplumber, "open", lambda path: fake)
    result = chunker.load_pdf("随便写个文件名.pdf")
    assert result == "第一页第二页"


@pytest.mark.io
def test_load_pdf_skips_empty_pages(monkeypatch):
    # None（扫描页/无文字）和空字符串都应该被跳过
    fake = FakePdf([FakePage("有内容"), FakePage(None), FakePage("")])
    monkeypatch.setattr(chunker.pdfplumber, "open", lambda path: fake)
    result = chunker.load_pdf("随便写个文件名.pdf")
    assert result == "有内容"


# ===== 自己动手写的三个用例 =====
@pytest.mark.unit
def test_my_empty():
    result = chunker.split_text("", 300, 60)
    assert len(result) == 0

@pytest.mark.unit
def test_my_short():
    result = chunker.split_text("我在学软件测试", 300, 60)
    assert len(result) == 1
    assert result == ["我在学软件测试"]  # 校验分片内容

@pytest.mark.unit
def test_my_len500():
    result = chunker.split_text("x" * 500, 300, 60)
    assert len(result) == 3
    assert result[0][-60:] == result[1][:60]  # 校验重叠

