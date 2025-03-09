# 一些简单的帮助函数
from langchain.output_parsers.json import parse_json_markdown

import re  # 正则
import hashlib


def md5(input) -> str:
    return hashlib.md5(input.encode()).hexdigest()


def get_action(text: str):
    text = text.strip()
    # 定义匹配正则
    action_pattern = r'"action":\s*"([^"]*)"'
    action_input_pattern = r'"action_input":\s*["|`]([^"]*)["|`]'
    # 提取出匹配到的action值
    action = re.search(action_pattern, text)
    action_input = re.search(action_input_pattern, text)
    action_value, action_input_value = "", ""

    if action:
        action_value = action.group(1)
    if action_input:
        action_input_value = action_input.group(1)

    if action_value and action_input_value:
        return action_value, action_input_value
    else:
        response = parse_json_markdown(text)
        return response["action"], response["action_input"]
