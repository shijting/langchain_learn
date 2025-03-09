# TODO 本课程来自 程序员在囧途(www.jtthink.com) 咨询群：98514334
import sys
import os

from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate

sys.path.append(os.path.abspath(os.path.join(os.path.abspath(__file__),
                                             '../../')))
from langchain import hub
from langchain_core.runnables import RunnablePassthrough

# pip install python-docx
from langchain_community.document_loaders import UnstructuredWordDocumentLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from ai_job.utils.llm import TongyiEmbedding, QdrantVecStoreFromDocs, \
    Tongyi, Zhipu


def clearstr(s):
    filter_chars = ['\n', '\r', '\t', '\u3000', '  ']
    for char in filter_chars:
        s = s.replace(char, '')
    return s


# 使用双换行分割简历的每一项 结合rag 进行检索增强生成
def format_docs(docs):
    return "\n\n".join(clearstr(doc.page_content) for doc in docs)


# 从doc中加载简历并且
def load_doc():
    word = UnstructuredWordDocumentLoader('jianli.docx')
    docs = word.load()
    splitter = RecursiveCharacterTextSplitter(chunk_size=50,
                                              chunk_overlap=20, )
    s_docs = splitter.split_documents(docs)

    vec_store = QdrantVecStoreFromDocs(s_docs)
    llm = Zhipu()

    # 使用rag 进行检索增强生成
    prompt = hub.pull("rlm/rag-prompt")
    chain = {"context": vec_store.as_retriever() | format_docs,
             "question": RunnablePassthrough()} | prompt | llm | StrOutputParser()

    # 浓缩简历精髓
    ret = chain.invoke("请输出姓名.格式如下\n姓名: ?")
    print(ret)
    ret = chain.invoke("总结专业技能情况,内容可能包含golang、Java、redis、mq等.格式如下\n专业技能: ?")
    print(ret)
    ret = chain.invoke("根据各大公司工作过的年份总结工作经验有多少年.格式如下\n工作经验: ?年")
    print(ret)
    ret = chain.invoke("请输出教育背景.格式列表\n教育背景: ?")
    print(ret)
    ret = chain.invoke("请输出期望薪资.格式如下\n期望薪资: ?k")
    print(ret)


if __name__ == '__main__':
    load_doc()
