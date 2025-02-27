from langchain.tools import BaseTool
from typing import List, Union

import re
from langchain.prompts import StringPromptTemplate
from langchain.agents import AgentOutputParser
from langchain.schema import AgentAction, AgentFinish
from langchain_core.exceptions import OutputParserException
from tools.prompts_tpl import CustomPromptTemplate
from tools.prompts import action_template
from tools.simple_tool import AddTool, SubTool


class CustomOutputParser(AgentOutputParser):
    # AgentAction: 需要执行一个action， 如tool执行
    # AgentFinish: 判断PromptTemplate输出结果是否有Final Answer
    def parse(self, llm_output: str) -> Union[AgentAction, AgentFinish]:
        # Check if agent should finish
        if "Final Answer:" in llm_output:
            return AgentFinish(
                # Return values is generally always a dictionary with a single `output` key
                # It is not recommended to try anything else at the moment :)
                return_values={"output": llm_output.split("Final Answer:")[-1].strip()},
                log=llm_output,
            )
        # Parse out the action and action input
        # 可以用json
        regex = r"Action\s*\d*\s*:(.*?)\nAction\s*\d*\s*Input\s*\d*\s*:[\s]*(.*)"
        match = re.search(regex, llm_output, re.DOTALL)
        if not match:
            raise OutputParserException(f"Could not parse LLM output: `{llm_output}`")
        action = match.group(1).strip()
        action_input = match.group(2)
        # Return the action and action input
        return AgentAction(tool=action, tool_input=action_input.strip(" ").strip('"'), log=llm_output)


if __name__ == "__main__":
    p = CustomOutputParser()
    print(p.parse("Action 1: AddTool\nAction Input: 2,6"))

    # 对我们写的CustomOutputParser进行测试，检查action_template是否能够正确解析, 和有哪些action_template中的参数没有被解析
    mytools = [AddTool(), SubTool()]
    tpl = CustomPromptTemplate(template=action_template,
                               input_variables=["input", "agent_scratchpad", "intermediate_steps", "tools",
                                                "tool_names"],
                               tools=mytools)
    ret = tpl.invoke({"input": "2+1=?", "agent_scratchpad": "I am thinking", "intermediate_steps": [], "tools": mytools,
                "tool_names": ["AddTool", "SubTool"]})
    print(ret)