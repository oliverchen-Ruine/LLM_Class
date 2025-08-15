from ollama import Client
import numpy as np
import faiss

client = Client(host='http://localhost:11434')
 
def get_embedding(text, model="dengcao/Qwen3-Embedding-8B:Q5_K_M"):
    response = client.embeddings(model=model, prompt=text)
    return np.array(response['embedding'], dtype=np.float32)

# 创建索引
dimension = 4096 
index = faiss.IndexFlatL2(dimension)

# 准备向量数据
knowledge =["神经网络原理", "深度学习框架", "大模型训练"]
knowledge_vectors = np.array([get_embedding(k) for k in knowledge], dtype='float32')
# 添加向量
index.add(knowledge_vectors)
print("数据库中共有向量：", index.ntotal)
 
# 查询相似度
query = "AI模型训练"
query_vec = get_embedding(query)
distances, indices = index.search(np.array([query_vec]), k=2)
print("查询向量：", query)
for i,j in enumerate(indices[0]):
    print("相似向量：{} \t 相似距离为：{}".format(knowledge[j],distances[0][i]))
