import os
from _md5 import md5

from langchain_community.embeddings import DashScopeEmbeddings
from langchain_community.vectorstores import FAISS, Chroma
# 加载文本，还有pdf，word等等
from langchain_community.document_loaders import TextLoader
# 切割文本
from langchain.text_splitter import CharacterTextSplitter

# qdrant
from qdrant_client import QdrantClient, models
from qdrant_client.models import Distance, VectorParams
from langchain_qdrant import QdrantVectorStore


def faiss_test():
    api_key = os.environ.get("TONGYI_API_KEY")
    eb = DashScopeEmbeddings(dashscope_api_key=api_key, model="text-embedding-v1")
    # print(eb.embed_query("今天天气怎么样"))

    # 数组里的内容可以理解为我们放在数据库里的内容，或者理解为我们的知识库
    # f = FAISS.from_texts(["今天天气是晴天", "明天星期三"], eb)
    # 我们的提问： 今天天气怎么样，得到欧氏距离越小越相似
    # print(f.similarity_search_with_score("今天天气怎么样"))

    # 从文本中加载数据
    text_loader = TextLoader(file_path="./resource/golang.txt").load()
    # chunk_overlap 重叠的部分, 最好大于0, 实际开发中需要我们自己去调，否则搜索出来的结果不是很准。
    # chunk_size 切割的大小
    doc = CharacterTextSplitter(chunk_size=200, chunk_overlap=0).split_documents(text_loader)
    # print(cts)
    f = FAISS.from_documents(doc, eb)
    print(f.similarity_search_with_score("程序员工资如何"))


def chroma_store():
    api_key = os.environ.get("TONGYI_API_KEY")
    eb = DashScopeEmbeddings(dashscope_api_key=api_key, model="text-embedding-v1")
    # 从文本中加载数据
    text_loader = TextLoader(file_path="./resource/golang.txt").load()
    # chunk_overlap 重叠的部分, 最好大于0, 实际开发中需要我们自己去调，否则搜索出来的结果不是很准。
    # chunk_size 切割的大小
    doc = CharacterTextSplitter(chunk_size=200, chunk_overlap=0).split_documents(text_loader)
    # print(cts)
    # 将分割后的文本存储到chroma中, 目前是存储到本地文件，当然也可以存储到手工安装的chroma 数据库中或者在其他云厂商托管的chroma数据库中
    db = (Chroma(collection_name="golang", embedding_function=eb, persist_directory="./datadir/chroma")
          .from_documents(doc, eb))
    # 返回一堆id
    ids = db.add_documents(doc)
    print(ids)


def chroma_search():
    api_key = os.environ.get("TONGYI_API_KEY")
    eb = DashScopeEmbeddings(dashscope_api_key=api_key, model="text-embedding-v1")
    db = Chroma(collection_name="golang", embedding_function=eb, persist_directory="./datadir/chroma")
    res = db.similarity_search_with_score("golang 程序员工资如何")
    print(res)


def qdrant_store():
    api_key = os.environ.get("TONGYI_API_KEY")
    eb = DashScopeEmbeddings(dashscope_api_key=api_key, model="text-embedding-v1")
    # 从文本中加载数据
    text_loader = TextLoader(file_path="./resource/golang.txt").load()
    # chunk_overlap 重叠的部分, 最好大于0, 实际开发中需要我们自己去调，否则搜索出来的结果不是很准。
    # chunk_size 切割的大小
    docs = CharacterTextSplitter(chunk_size=200, chunk_overlap=0).split_documents(text_loader)
    client = QdrantClient(host="localhost", port=6333)
    # 创建一个collection, 也可以理解为一个数据库表
    collection_name = "golang"
    if not client.collection_exists(collection_name):
        res = client.create_collection(collection_name=collection_name,
                                       vectors_config=VectorParams(size=eb.embedding_dimensions,  # 向量的维度,通义千问事1536
                                                                   distance=Distance.COSINE))  # distance距离计算方式
        if not res:
            raise Exception("创建collection失败")
    store = QdrantVectorStore(client=client, collection_name=collection_name, embedding=eb)
    # 防止重复插入
    s_doc_new = []
    s_doc_ids = []
    for doc in docs:
        doc.id = md5(doc.page_content)
        s_doc_new.append(doc)
        s_doc_ids.append(doc.id)

    added_ids = store.add_documents(s_doc_new, ids=s_doc_ids)
    print(added_ids)


if __name__ == "__main__":
    # 第一次运行时候需要运行chroma_store()，将文本存储到chroma中, 后续可以直接运行chroma_search()
    chroma_store()
    chroma_search()
