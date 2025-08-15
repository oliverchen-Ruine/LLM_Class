import PyPDF2
import re

def extract_pdf_text(pdf_path):
    """提取PDF文本内容"""
    text = ""
    with open(pdf_path, "rb") as file:
        reader = PyPDF2.PdfReader(file)
        for page in reader.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text
    return text

def clean_pdf_text(text):
    """清洗PDF文本"""
    # 移除页眉页脚
    cleaned_text = re.sub(r"第\s*\d+\s*页", "", text)
    # 压缩空白字符
    cleaned_text = re.sub(r"\s+", " ", cleaned_text).strip()
    return cleaned_text

# 使用示例
pdf_path = "code/document.pdf"
raw_text = extract_pdf_text(pdf_path)
print("原始文本:"+ raw_text)
print("处理后:" + clean_pdf_text(raw_text))
