import os

from langchain_openai import ChatOpenAI
from langchain.chains.conversation.memory import ConversationSummaryMemory

from rag_learn.cls_spider import get_cls_data


#  对财联社电报进行摘要总结
def sum_cls(keyword: str):
    llm = ChatOpenAI(
        model="moonshot-v1-8k",
        base_url='https://api.moonshot.cn/v1',
        api_key=os.environ.get("KIMI_API_KEY")
    )

    data = get_cls_data(keyword)

    mem = ConversationSummaryMemory(llm=llm)
    for item in data:
        mem.save_context({"input": item["key"]}, {"output": item["value"]})

    return mem.buffer


def sum_f10(code: str):
    # 使用通义千问大模型语言
    # llm =
    llm = ChatOpenAI(
        model="moonshot-v1-8k",
        base_url='https://api.moonshot.cn/v1',
        api_key=os.environ.get("KIMI_API_KEY")
    )

    data = get_cls_data(code)

    mem = ConversationSummaryMemory(llm=llm)
    for item in data:
        mem.save_context({"input": item["key"]}, {"output": item["value"]})

    return mem.buffer