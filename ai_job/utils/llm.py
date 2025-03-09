from typing import List

from langchain_openai import ChatOpenAI
from langchain_community.embeddings import DashScopeEmbeddings
from langchain_qdrant import QdrantVectorStore
import os
# 智普
from langchain_community.chat_models import ChatZhipuAI


# LLM的创建，方便引用


# 智普
def Zhipu():
    return ChatZhipuAI(
        model="glm-4-flash",
        api_key=os.environ.get("ZHIPU_API_KEY"),
        base_url="https://open.bigmodel.cn/api/paas/v4/chat/completions",
        temperature=0.5,
    )


# moonshot Kimi
def Kim():
    return ChatOpenAI(
        model="moonshot-v1-8k",
        api_key=os.environ.get("KIMI_API_KEY"),
        base_url="https://api.moonshot.cn/v1"
    )


# 通义千问
def Tongyi():
    return ChatOpenAI(
        # model="qwen-max",
        model="qwen-max-0403",
        api_key=os.environ.get("TONGYI_API_KEY"),  # 自行搞定  你的秘钥
        base_url="https://dashscope.aliyuncs.com/compatible-mode/v1"
    )


# 通义千问的向量模型
def TongyiEmbedding() -> DashScopeEmbeddings:
    api_key = os.environ.get("TONGYI_API_KEY")
    return DashScopeEmbeddings(dashscope_api_key=api_key,
                               model="text-embedding-v1")


# 将文档转化为向量
def QdrantVecStoreFromDocs(docs):
    eb = TongyiEmbedding()
    return QdrantVecStore.from_documents(documents=docs, embedding=eb)

def QdrantVecStore(eb: DashScopeEmbeddings, collection_name: str):
    return QdrantVectorStore. \
        from_existing_collection(embedding=eb,
                                 url="http://113.31.126.191:6333",
                                 collection_name=collection_name)
