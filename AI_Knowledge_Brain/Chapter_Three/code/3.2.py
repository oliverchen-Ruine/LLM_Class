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