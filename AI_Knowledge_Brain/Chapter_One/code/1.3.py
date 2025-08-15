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
excel_path = "code/data.xlsx"
print(process_excel(excel_path))