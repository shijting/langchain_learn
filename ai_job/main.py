import sys
import os

from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnablePassthrough
from ai_job.utils.llm import Tongyi
from ai_job.spider.spider import get_list_by_keyword

sys.path.append(os.path.abspath(os.path.join(os.path.abspath(__file__), '../../')))


def load_prompt_file() -> str:
    with open("prompts/test1.txt", 'r') as f:
        return f.read()


def test():
    llm = Tongyi()

    prompt_tpl = load_prompt_file()
    prompt = PromptTemplate.from_template(prompt_tpl)
    chain = {
                "job_list": RunnablePassthrough(),
            } | prompt | llm | StrOutputParser()
    ret = chain.invoke(get_list_by_keyword("golang"))
    print(ret)


if __name__ == '__main__':
    test()
