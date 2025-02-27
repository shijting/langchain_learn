import os

from langchain_openai import ChatOpenAI

from langchain.chains.conversation.memory import ConversationSummaryMemory
from spider import spider_telegram

if __name__ == "__main__":
    kv = spider_telegram()
    # 测试，为了防止耗费token过多，只取前两个
    kv = kv[:1]

    openai = ChatOpenAI(
        model="moonshot-v1-8k",
        base_url='https://api.moonshot.cn/v1',
        api_key=os.environ.get("KIMI_API_KEY")
    )

    mem = ConversationSummaryMemory(llm=openai)
    for item in kv:
        mem.save_context({"input": item["key"]}, {"output": item["value"]})

    print(mem.buffer)

