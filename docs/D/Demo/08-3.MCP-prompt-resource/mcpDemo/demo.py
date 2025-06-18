from mcp.server.fastmcp import FastMCP

mcp = FastMCP()

#  目前cursor不支持  prompt和resource的 传递协议  
# 可使用 Claude Desktop 实现

@mcp.resource("config://params/definition")
def param_definition_info(query: str) -> str:
    """在查询埋点之前我需要先通过此工具获取query的埋点信息"""
    
    
    
    return ""
    

@mcp.prompt()
def prompt() -> str:
    return """
你是一个天气播报员，每次播报天气时，需要先介绍一下自己, 介绍内容如下：
我是小李播报员，下面是今天的天气预报：

一定要强制按照示例去播报，不要自己发挥。
"""

@mcp.tool()
async def get_weather(city: str) -> str:
    """获取某个城市的天气预报。"""
    return f"当前{city}的天气是晴天"

if __name__ == "__main__":
    # 初始化并运行 server
    mcp.run(transport='stdio')
    