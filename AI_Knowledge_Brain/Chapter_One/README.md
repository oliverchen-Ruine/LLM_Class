# 文本预处理：将人类文档转化为AI可用知识

## 第一章：文档处理的必要性与目标

### 为什么需要文档处理？
在当今大模型应用的知识库构建中，文档处理是至关重要的前置环节。人类日常使用的文档（PDF、Word、TXT等）对大模型构成三大挑战：

1. **格式障碍**：不同文档的复杂结构干扰模型理解
2. **冗余噪声**：格式信息、重复内容降低知识密度
3. **认知局限**：模型无法自动解析文档结构语义

### 核心处理目标
文档处理的核心目标是将非结构化文档转换为模型可理解的结构化数据：
- ✅ 移除无关内容（页眉页脚、特殊格式、噪声段落）
- ✅ 保留有价值信息（标题、段落、列表、表格数据）
- ✅ 转为模型友好格式（纯文本/结构化片段）

> **核心公式**：文档处理 = 人类可读内容 → AI可用的知识资产

---

## 第二章：文档处理的核心挑战

### 直接使用文档的四大障碍
| 障碍点 | 说明 | 影响 |
|-------|------|------|
| **格式限制** | PDF/Word等格式无法直接解析 | 模型无法识别内容结构 |
| **长度限制** | 超出上下文窗口(如128K Token) | 无法完整提取长文档知识 |
| **无结构感知** | 无法区分标题/正文/表格 | 丧失文档语义层次 |
| **无语义压缩** | 冗余信息导致模型"迷失重点" | 生成答案不准确或编造 |

### 典型文档处理流程
```mermaid
graph LR
A[原始文档] --> B[读取加载]
B --> C[内容提取]
C --> D[文本清洗]
D --> E[分段切分]
E --> F[结构化标记]
F --> G[统一格式输出]
```

1. **读取加载**：按文件类型选用不同工具库
2. **内容提取**：分离核心内容与格式噪声
3. **文本清洗**：标准化处理统一文本规范
4. **分段切分**：按语义/长度合理切分文档
5. **结构化标记**：标识内容类型（标题/正文等）
6. **格式输出**：转为标准数据结构（List/Dict）

---

## 第三章：PDF文档处理实战

### 处理挑战与解决方案
| 问题类型 | 特征 | 解决方案 |
|---------|------|----------|
| 文本型PDF | 可提取文字但含页眉页脚 | 正则表达式清洗 |
| 扫描型PDF | 文字以图片形式存储 | OCR光学字符识别 |
| 加密PDF | 访问需要密码 | 解密后处理 |

### Python处理代码
```python
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
pdf_path = "document.pdf"
raw_text = extract_pdf_text(pdf_path)
clean_text = clean_pdf_text(raw_text)
```

### 处理效果对比
```diff
- 原始文本: "第1页\n\n合同编号：XYZ-2023\n甲方：ABC公司...第2页\n1.1条款..."
+ 处理后: "合同编号：XYZ-2023 甲方：ABC公司...1.1条款..."
```

---

## 第四章：TXT文档处理实战

### 处理挑战与解决方案
| 问题 | 原因 | 解决方案 |
|------|------|----------|
| 编码错误 | UTF-8/GBK编码冲突 | 多编码尝试读取 |
| 噪声内容 | 无效空行/特殊字符 | 正则过滤清洗 |
| 结构混乱 | 缺乏自然分段 | 语义/规则分段 |

### Python处理代码
```python
import re

def read_txt_with_encoding(txt_path):
    """多编码尝试读取TXT文件"""
    encodings = ["utf-8", "gbk", "latin-1"]
    for enc in encodings:
        try:
            with open(txt_path, "r", encoding=enc) as f:
                return f.read()
        except UnicodeDecodeError:
            continue
    raise ValueError("无法识别编码")

def clean_txt_text(text):
    """清洗文本内容"""
    # 移除空行
    lines = [line.strip() for line in text.split("\n") if line.strip()]
    cleaned_text = " ".join(lines)
    # 过滤特殊字符
    cleaned_text = re.sub(r"[^\w\s\u4e00-\u9fa5]", "", cleaned_text)
    return cleaned_text

# 使用示例
txt_path = "data.txt"
raw_text = read_txt_with_encoding(txt_path)
clean_text = clean_txt_text(raw_text)
```

---

## 第五章：Word文档处理实战

### 处理挑战与解决方案
| 挑战点 | 影响 | 解决方案 |
|--------|------|----------|
| 格式样式 | 干扰内容提取 | 解析样式元数据 |
| 表格图像 | 非文本内容处理困难 | 表格转结构化数据 |
| 标题层级 | 丧失文档结构 | 识别标题样式级别 |

### Python处理代码
```python
from docx import Document

def extract_word_content(word_path):
    """提取Word结构化内容"""
    doc = Document(word_path)
    content_list = []
  
    for para in doc.paragraphs:
        para_text = para.text.strip()
        if not para_text:
            continue
          
        style_name = para.style.name
        if style_name.startswith("Heading"):
            # 标题处理
            content_list.append({
                "type": "heading",
                "level": int(style_name[-1]),
                "content": para_text
            })
        else:
            # 正文处理
            content_list.append({
                "type": "text",
                "content": para_text
            })
  
    return content_list

# 使用示例
word_path = "report.docx"
content = extract_word_content(word_path)
```

### 结构化输出示例
```json
[
  {"type": "heading", "level": 1, "content": "项目总结报告"},
  {"type": "text", "content": "本项目自2023年1月启动..."},
  {"type": "heading", "level": 2, "content": "成果展示"},
]
```

---

## 第六章：Excel文档处理实战

### 处理挑战与解决方案
| 挑战 | 影响 | 解决方案 |
|------|------|----------|
| 复杂表格结构 | 数据错位 | pandas智能解析 |
| 公式干扰 | 无实际意义 | 提取计算结果值 |
| 多sheet管理 | 信息分散 | sheet统一处理 |

### Python处理代码
```python
import pandas as pd

def process_excel(excel_path, sheet_name=0):
    """处理Excel文件"""
    df = pd.read_excel(excel_path, sheet_name=sheet_name, skiprows=0, engine="openpyxl")
  
    # 清洗空行空列
    df = df.dropna(axis=0, how="all").dropna(axis=1, how="all")
  
    # 转换为自然语言描述
    text_content = ""
    for idx, row in df.iterrows():
        text_content += f"第{idx+1}行: "
        for col_name, value in row.items():
            text_content += f"{col_name}={value}, "
        text_content += "\n"
  
    return text_content

# 使用示例
excel_path = "data.xlsx"
content = process_excel(excel_path)
```

### 文本转换示例
```
第1行: 姓名=张三, 年龄=28, 部门=技术部
第2行: 姓名=李四, 年龄=32, 部门=市场部
```

---

## 第七章：Markdown文档处理实战

### 处理挑战与解决方案
| 挑战 | 影响 | 解决方案 |
|------|------|----------|
| 标记干扰 | #、*等符号干扰 | 正则表达式清除 |
| 结构信息 | 标题层级丢失 | 保留层级缩进 |
| 代码块 | 技术内容处理 | 特别标注保留 |

### 处理方法1：正则处理
```python
import re

def md_to_clean_text(md_content):
    """正则清洗Markdown"""
    # 清除标题标记
    text = re.sub(r'^#+\s', '', md_content, flags=re.MULTILINE)
    # 清除列表标记
    text = re.sub(r'^\s*[-*0-9.]+\s', '', text, flags=re.MULTILINE)
    # 清除链接
    text = re.sub(r'\[.*?\]\(.*?\)', '', text)
    # 清除代码块
    text = re.sub(r'```[\s\S]*?```', '', text)
    # 合并空格
    text = re.sub(r'\s+', ' ', text).strip()
    return text
```

### 处理方法2：HTML转换
```python
from bs4 import BeautifulSoup
import markdown2

def md_to_html_text(md_content):
    """通过HTML转换处理Markdown"""
    html = markdown2.markdown(md_content)
    soup = BeautifulSoup(html, 'html.parser')
    return soup.get_text(separator=' ', strip=True)
```

### 层级保留方案
```python
def md_keep_structure(md_content):
    """保留Markdown层级结构"""
    lines = md_content.split('\n')
    result = []
  
    for line in lines:
        line = line.strip()
        if line.startswith('#'):
            level = line.count('#')
            title = line.lstrip('#').strip()
            result.append(f"{'  '*(level-1)}{title}")
        elif line:
            result.append(line)
  
    return '\n'.join(result)
```

---

## 第八章：综合应用与最佳实践

### 文档预处理标准化流程
1. **格式检测**：自动识别文档格式类型
2. **路由处理**：调用对应格式处理器
3. **统一清洗**：应用通用文本清洗规则
4. **语义分段**：按主题/长度智能分段
5. **元数据标注**：添加来源/类型等元信息
6. **存储优化**：转换为向量数据库友好格式

### 通用处理函数框架
```python
def process_document(file_path):
    """统一文档处理入口"""
    file_ext = file_path.split('.')[-1].lower()
  
    if file_ext == 'pdf':
        content = extract_pdf_text(file_path)
    elif file_ext == 'docx':
        content = extract_word_content(file_path)
    elif file_ext in ['xlsx', 'xls']:
        content = process_excel(file_path)
    elif file_ext == 'md':
        content = md_to_clean_text(open(file_path).read())
    else:  # 默认为txt处理
        content = read_txt_with_encoding(file_path)
  
    # 应用通用清洗
    return clean_universal(content)

def clean_universal(text):
    """通用文本清洗"""
    text = re.sub(r'\s+', ' ', text)  # 压缩空白
    text = re.sub(r'[^\w\s\u4e00-\u9fa5.,!?;:]', '', text)  # 过滤特殊字符
    return text.strip()
```

### 最佳实践建议
1. **格式优先策略**：优先处理结构化程度高的文档（如Markdown）
2. **分阶段处理**：先提取后清洗，避免信息丢失
3. **保留原始版本**：保留一份原始文本用于错误排查
4. **分块元数据**：为每个文本块添加来源位置信息
5. **自动化流水线**：建立处理-存储-更新的自动化流程

> **文档处理是知识库构建的基石**，如同炼金术中的提纯过程，决定了最终知识的纯度与价值。