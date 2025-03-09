import hashlib
import os
import re
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
from qdrant_client.http import models

def md5(data):
    md5_hash = hashlib.md5()
    # 更新哈希对象（需要将字符串编码为字节）
    md5_hash.update(data.encode('utf-8'))

    # 获取 MD5 哈希值（十六进制格式）
    return md5_hash.hexdigest()


def qdrant_store():
    api_key = os.environ.get("TONGYI_API_KEY")
    eb = DashScopeEmbeddings(dashscope_api_key=api_key, model="text-embedding-v1")
    # 从文本中加载数据
    text_loader = TextLoader(file_path="./resource/golang.txt").load()
    # chunk_overlap 重叠的部分, 最好大于0, 实际开发中需要我们自己去调，否则搜索出来的结果不是很准。
    # chunk_size 切割的大小
    docs = CharacterTextSplitter(chunk_size=200, chunk_overlap=0).split_documents(text_loader)
    client = QdrantClient(host="127.0.0.1", port=6333)
    # 创建一个collection, 也可以理解为一个数据库表
    collection_name = "golang"
    if not client.collection_exists(collection_name):
        res = client.create_collection(collection_name=collection_name,
                                       vectors_config=VectorParams(size=1536,  # 向量的维度,通义千问事1536
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
        tags = get_tags(doc.page_content)
        doc.metadata["tags"] = tags

    added_ids = store.add_documents(s_doc_new, ids=s_doc_ids)
    print(added_ids)



def get_tags(text: str):
    """
    获取两个# 之间的文本
    """
    # 使用正则表达式查找所有符合标签模式的字符串
    res = re.findall(r"(#)(.+?)(?=#)", text)
    # 如果找到匹配项，则提取每个匹配项的第二个分组内容（即标签内容）
    return [match[1] for match in res] if res else []



def qdrant_search():
    api_key = os.environ.get("TONGYI_API_KEY")
    eb = DashScopeEmbeddings(dashscope_api_key=api_key, model="text-embedding-v1")
    vec_store = QdrantVectorStore.from_existing_collection(embedding=eb, url="127.0.0.1:6333", collection_name="golang")
    ret = vec_store.similarity_search_with_score("golang程序员工资待遇如何")  # 最相似的应该是【工资待遇分析】而不是【golang程序员如何看待自己的工资待遇】
    print(ret)
    print("--------")
    #     相对精准搜索
    filter = models.Filter(
        must=[
            models.FieldCondition(
                key="metadata.tags[]",
                match=models.MatchValue(value="薪资"),
            )
        ]
    )
    ret = vec_store.similarity_search_with_score("golang程序员工资待遇如何", filter=filter)
    print(ret)


if __name__ == "__main__":
    qdrant_store()
    qdrant_search()
