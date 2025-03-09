import os

from langchain_community.document_loaders import AsyncHtmlLoader
from bs4 import BeautifulSoup
from langchain_community.embeddings import DashScopeEmbeddings
from langchain_openai import ChatOpenAI
from langchain_qdrant import QdrantVectorStore

"""
rag学习(2)html抓取在线检索（初级）
"""


def get_summary(html):
    html_str = BeautifulSoup(html, 'html.parser')
    return html_str.find(name="div", attrs={"class": "article_content"}).get_text()


def qdrant_store_from_docs(docs):
    api_key = os.environ.get("TONGYI_API_KEY")
    eb = DashScopeEmbeddings(dashscope_api_key=api_key, model="text-embedding-v1")
    return QdrantVectorStore.from_documents(documents=docs, embedding=eb)


def test():
    loader = AsyncHtmlLoader(["https://blog.csdn.net/lengyue1084/article/details/108004499",
                              "https://blog.csdn.net/cjy040921/article/details/146053910"])
    docs = loader.load()
    new_docs = []
    for doc in docs:
        doc.page_content = get_summary(doc.page_content)
        new_docs.append(doc)

    return new_docs


if __name__ == '__main__':
    store = qdrant_store_from_docs(test())
    res = store.similarity_search("大学")
    print(res)
