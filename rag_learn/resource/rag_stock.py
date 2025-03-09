
import os

from langchain_community.document_loaders import AsyncHtmlLoader
from bs4 import BeautifulSoup
from langchain_community.embeddings import DashScopeEmbeddings
from langchain_openai import ChatOpenAI
from langchain_qdrant import QdrantVectorStore

if __name__=='__main__':
    api_key = os.environ.get("TONGYI_API_KEY")

    eb = DashScopeEmbeddings(dashscope_api_key=api_key, model="text-embedding-v1")
    # 使用通义千问大模型语言
    # llm =
    llm = ChatOpenAI(
        model="moonshot-v1-8k",
        base_url='https://api.moonshot.cn/v1',
        api_key=os.environ.get("KIMI_API_KEY")
    )
