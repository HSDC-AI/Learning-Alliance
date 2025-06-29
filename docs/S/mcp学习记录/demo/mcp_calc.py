from mcp.server.fastmcp import FastMCP
import asyncio

# 初始话mcp服务器
mcp = FastMCP("calc")

@mcp.tool()
async def greet(name: str) -> str:
    """
        向用户问好
        Args：
            name： 用户名称
    """
    return f"你好，{name}"

@mcp.tool()
async def calc(expression: str) -> str:
    """
        计算器
        Args:
             expression: 数学表达式
    """
    try:
        allowed_chars = "0123456789+-*/(). "
        if not all(c in allowed_chars for c in expression):
            return "f计算出错： 出现不允许的字符"
        result = eval(expression)
        return f"计算结果 {result}"
    except Exception as e:
        return f"计算出错 {str(e)}"

async def main():
    print(await greet("张三"))
    print(await calc("1 + 2 * 3"))

if __name__ == "__main__":
    asyncio.run(main())