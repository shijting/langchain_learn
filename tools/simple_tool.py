from langchain.tools import tool, BaseTool


class AddTool(BaseTool):
    name: str = "AddTool"
    description: str = """
    Use this tool to perform addition operations
    example:
    2+6=?
    then Action Input: 2,6  
    """

    def _run(self, add_expr: str) -> int:
        """执行加法运算"""
        a, b = add_expr.split(',')  # 暂不支持多参数
        if len(a) == 0 or len(b) == 0:
            return "Please input two numbers"
        return int(a) + int(b)


class SubTool(BaseTool):
    name: str = "SubTool"
    description: str = """
    Use this tool to perform subtraction operations
    example:
    6-2=?
    then Action Input: 6,2  
    """

    def _run(self, sub_expr: str) -> int:
        """执行减法运算"""
        a, b = sub_expr.split(',')
        if len(a) == 0 or len(b) == 0:
            return "Please input two numbers"
        return int(a) - int(b)
