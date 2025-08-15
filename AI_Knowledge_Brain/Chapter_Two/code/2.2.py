from ollama import Client
import numpy as np
 
client = Client(host='http://localhost:11434')
 
def get_embedding(text, model="dengcao/Qwen3-Embedding-8B:Q5_K_M"):
    response = client.embeddings(model=model, prompt=text)
    return np.array(response['embedding'], dtype=np.float32)
 
# 批量处理
texts = ["这是一个embedding的示例"]
embeddings = [get_embedding(text) for text in texts]
print(embeddings)