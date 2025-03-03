import os

from langchain_community.embeddings import DashScopeEmbeddings
from langchain_community.vectorstores import FAISS

def test():
    api_key = os.environ.get("TONGYI_API_KEY")
    eb = DashScopeEmbeddings(dashscope_api_key=api_key, model="text-embedding-v1")
    # print(eb.embed_query("今天天气怎么样"))
    # 数组里的内容可以理解为我们放在数据库里的内容，或者理解为我们的知识库
    f = FAISS.from_texts(["今天天气是晴天"], eb)
    # 我们的提问： 今天天气怎么样，得到欧氏距离越小越相似
    print(f.similarity_search_with_score("今天天气怎么样"))

if __name__ == "__main__":
    test()