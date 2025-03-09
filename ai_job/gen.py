import sys
import os

from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough

sys.path.append(os.path.abspath(os.path.join(os.path.abspath(__file__),
                                             '../../')))
from langchain_core.prompts import PromptTemplate
from ai_job.utils.llm import Zhipu


# 简历生成

# 加载prompt模板
def load_prompt() -> str:
    with open(f'prompts/jianli.txt', 'r', encoding='utf-8') as f:
        return f.read()


# 加载 职位列表(可以实时抓取）
def load_jobs():
    with open(f'backup/go_jobs.txt', 'r', encoding='utf-8') as f:
        jobs_all_str = f.read()

        # 根据换行分割，获取职位列表
        jobs = jobs_all_str.split('\n\n')
        return [job for job in jobs if job.strip() != '']


def test_gen():
    prompt = PromptTemplate.from_template(load_prompt())
    llm = Zhipu()
    chain = {
                "input": RunnablePassthrough()
            } | prompt | llm | StrOutputParser()

    # 只取5个，避免token 过大
    ret = chain.invoke(load_jobs()[0:5])
    print(ret)


if __name__ == '__main__':
    test_gen()
