import os
import json
import numpy as np
import faiss
from typing import List, Dict, Tuple
from dotenv import load_dotenv
from ollama import Client
from collections import deque
import requests
client = Client(host='http://localhost:11434')
 
def get_embedding(text, model="dengcao/Qwen3-Embedding-8B:Q5_K_M"):
    response = client.embeddings(model=model, prompt=text)
    return np.array(response['embedding'], dtype=np.float32)

def load_data_group(folder_path: str) -> Tuple[faiss.Index, List[Dict]]:
    files = os.listdir(folder_path)
    # 找出所有.index文件，依据命名前缀找到对应.json文件
    index_files = [f for f in files if f.endswith('.index')]

    # 结果：合并所有组的FAISS索引和对应元数据
    # 为了合并多个FAISS索引，我们这里采取一次性加载所有embedding并重建索引的方案（便于统一检索）
    all_embeddings = []
    all_metadata = []

    for idx_file in index_files:
        prefix = idx_file[:-6]  # 去掉 '.index'
        chunks_file = prefix + "_chunks.json"
        vectors_file = prefix + "_vectors.json"

        idx_path = os.path.join(folder_path, idx_file)
        chunks_path = os.path.join(folder_path, chunks_file)
        vectors_path = os.path.join(folder_path, vectors_file)

        # 检查对应文件是否存在
        if not (os.path.exists(chunks_path) and os.path.exists(vectors_path)):
            print(f"警告：文件组不完整，缺少 {chunks_file} 或 {vectors_file}，跳过 {prefix}")
            continue

        # 读取文本块
        with open(chunks_path, "r", encoding="utf-8") as f:
            chunks_data = json.load(f)

        # 读取向量数据
        with open(vectors_path, "r", encoding="utf-8") as f:
            vectors_data = json.load(f)

        # 将文本和向量对应起来，确保id对应一致
        id_to_text = {item['id']: item['text'] for item in chunks_data}

        for vec_item in vectors_data:
            vec_id = vec_item['id']
            embedding = vec_item.get('embedding')
            if embedding is None:
                print(f"警告：id={vec_id}在 {vectors_file} 中缺少embedding，跳过")
                continue
            text = id_to_text.get(vec_id, "")
            all_embeddings.append(embedding)
            all_metadata.append({
                "id": vec_id,
                "text": text,
                "source_file": vec_item.get("source_file", ""),
                "prefix": prefix
            })

    # 构建FAISS索引
    if len(all_embeddings) == 0:
        raise ValueError("没有加载到任何embedding向量，无法构建索引")

    dimension = len(all_embeddings[0])
    #print(f"总共加载向量数：{len(all_embeddings)}，向量维度：{dimension}")

    embeddings_np = np.array(all_embeddings, dtype=np.float32)

    # 创建FAISS索引，使用内积或欧式距离（这里默认L2距离）
    index = faiss.IndexFlatL2(dimension)
    index.add(embeddings_np)
    #print(f"FAISS索引构建完成，向量总数: {index.ntotal}")

    return index, all_metadata

class RAGSystem:
    def __init__(self, index_path, temperature=0.8, model_name="qwen3:8b"):
        self.index, self.metadata = load_data_group(index_path)
        self.chat_history = deque(maxlen=6)  # 保留3轮对话
        self.temperature = temperature  # 存储温度值
        self.model_name = model_name  # 生成模型名称
    
    def _retrieve(self, query: str, top_k=5):
        """向量检索"""
        emb = get_embedding(query)
        distances, indices = self.index.search(np.array([emb]), top_k)
        return [self.metadata[idx] for idx in indices[0]]
    
    def _build_prompt(self, context_docs, query):
        """知识增强的Prompt构造"""
        context = "\n\n".join(f"【知识片段 {i}】{doc['text']}" 
                             for i, doc in enumerate(context_docs))
        return f"背景知识：\n{context}\n\n问题：{query}\n回答要求：用中文回答，包含知识来源"
    
    def generate_answer(self, query, top_k):
        # 1. 检索上下文
        context_docs = self._retrieve(query,top_k)


        # 2. 构造Prompt（包含多轮历史）
        prompt = "你是有专业文档支持的助手。请根据以下知识和对话历史回答问题：\n\n"
    
        # 添加对话历史（如果有）
        if self.chat_history:
            for i, content in enumerate(self.chat_history):
                role = "用户" if i % 2 == 0 else "助手"
                prompt += f"{role}: {content}\n"
    
        # 添加当前问题和知识片段
        prompt += f"\n知识背景：\n{self._build_prompt(context_docs, query)}"
        print("=== 最终 prompt ===")
        print(prompt)
        # 3. 调用Ollama
        response = requests.post(
            "http://localhost:11434/api/generate",
            json={
                "model": self.model_name,
                "prompt": prompt,
                "stream": False,  # 明确要求非流式输出
                "options": {
                    "temperature": self.temperature  # 设置温度值
                }
            }
        )
        answer = response.json()["response"]
        
        # 4. 后处理
        clean_answer = self._postprocess(answer)
        self.chat_history.extend([query, clean_answer])
        return clean_answer


    def _postprocess(self, text):
        """答案优化"""
        last_query = self.chat_history[-2] if len(self.chat_history) >= 2 else ""
        # 学术文献添加引用
        if any(kw in last_query  for kw in ["文献", "研究"]):
            return f"{text}\n\n来源：{self.current_sources()}"
            
        # 法律文件精确条款标注
        elif "条款" in last_query :
            return re.sub(r"第([零一二三四五六七八九十百]+)条", r"【\g<0>】", text)
        
        return text.strip()


if __name__ == "__main__":
    folder = "/workspace/code/datas/output"  # 修改为你的文件夹路径
    rag_engine = RAGSystem(folder)
    
    print("欢迎使用AI知识脑(输入'退出'结束对话)\n")
    
    while True:
        try:
            # 获取用户输入
            query = input("\n用户: ")
            
            # 退出条件
            if query.lower() in ['退出', 'exit', 'quit']:
                print("\n对话结束，再见！")
                break
                
            # 空输入处理
            if not query.strip():
                print("请输入有效问题")
                continue
                
            # 生成回答
            print("\n思考中...")
            ans = rag_engine.generate_answer(query, top_k=5)
            
            # 输出回答
            print("\n=== 回答 ===\n")
            print(ans)
            
        except KeyboardInterrupt:
            print("\n对话结束，再见！")
            break
        except Exception as e:
            print(f"\n发生错误: {str(e)}")
            continue