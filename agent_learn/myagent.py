from tools.prompts_tpl import CustomPromptTemplate
from tools.prompts import action_template
from tools.simple_tool import AddTool, SubTool
from tools.parsers import CustomOutputParser
from langchain.agents import create_react_agent, AgentExecutor
from langchain import hub

from utils.llm import openAi

if __name__ == "__main__":
    p = CustomOutputParser()
    print(p.parse("Action 1: AddTool\nAction Input: 2,6"))

    # 对我们写的CustomOutputParser进行测试，检查action_template是否能够正确解析, 和有哪些action_template中的参数没有被解析
    mytools = [AddTool(), SubTool()]

    # 这种string template 主要用于回答单问题的，后面的聊天式的使用chat template
    # 手动创建的prompt 模板
    # tpl = CustomPromptTemplate(template=action_template,
    #                            input_variables=["input", "agent_scratchpad", "intermediate_steps", "tools",
    #                                             "tool_names"],
    #                            tools=mytools)

    # 使用hub 自动拉取的模板
    tpl = hub.pull("hwchase17/react")

    # ret = tpl.invoke({"input": "2+1=?", "agent_scratchpad": "I am thinking", "intermediate_steps": [], "tools": mytools,
    #             "tool_names": ["AddTool", "SubTool"]})
    # print(ret)
    llm = openAi()
    agent = create_react_agent(llm=llm, tools=mytools, prompt=tpl, output_parser=p)

    # return_intermediate_steps=True 会返回中间步骤,也就是打开中间推理过程
    # max_iterations=2 限制最大迭代次数2次, 默认15次
    agent_execute = AgentExecutor(agent=agent, tools=mytools, return_intermediate_steps=True, verbose=True,
                                  max_iterations=2)
    ret = agent_execute.invoke({"input": "10-3=多少"})
    print(ret)
