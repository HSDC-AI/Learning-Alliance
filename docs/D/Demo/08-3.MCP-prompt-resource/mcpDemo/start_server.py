#!/usr/bin/env python3
"""
启动MCP服务的脚本
"""
import sys
import os

# 添加当前目录到Python路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from demo import mcp

if __name__ == "__main__":
    print("Starting MCP Demo Server...")
    print("Server is running with prompt 'demo' and tool 'get_weather'")
    mcp.run(transport='stdio') 