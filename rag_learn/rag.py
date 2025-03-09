import os

from rag_learn.vec import qdrant_store
from langchain_community.embeddings import DashScopeEmbeddings
from langchain_openai import ChatOpenAI
from langchain import hub

from langchain_qdrant import QdrantVectorStore
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser


def format_docs(docs):
    return "\n\n".join(doc.page_content for doc in docs)


if __name__ == "__main__":
    qdrant_store()
    api_key = os.environ.get("TONGYI_API_KEY")

    eb = DashScopeEmbeddings(dashscope_api_key=api_key, model="text-embedding-v1")
    # 使用通义千问大模型语言
    # llm =
    llm = ChatOpenAI(
        model="moonshot-v1-8k",
        base_url='https://api.moonshot.cn/v1',
        api_key=os.environ.get("KIMI_API_KEY")
    )

    eb = DashScopeEmbeddings(dashscope_api_key=api_key, model="text-embedding-v1")
    vec_store = QdrantVectorStore.from_existing_collection(embedding=eb, url="127.0.0.1:6333", collection_name="golang")
    # https://smith.langchain.com/hub/
    prompt = hub.pull("rlm/rag-prompt")

    chain = {"context": vec_store.as_retriever() | format_docs,
             "question": RunnablePassthrough()} | prompt | llm | StrOutputParser()

    res = chain.invoke("golang程序员工资待遇如何")
    print(res)
