from langchain_openai import ChatOpenAI
import os


def openAi():
    openai = ChatOpenAI(
        model="moonshot-v1-8k",
        base_url='https://api.moonshot.cn/v1',
        api_key=os.environ.get("KIMI_API_KEY")
    )
    return openai
