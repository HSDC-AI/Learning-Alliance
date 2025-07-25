#!/usr/bin/env python3
"""
Orchestrator Agent - A2A Resource Processing Orchestrator
编排器Agent，负责协调资源分析、图片处理、资源替换的完整工作流

运行方式:
uv run app --port 8000
"""

import logging
import uvicorn
import click
from dotenv import load_dotenv

from app.server import create_orchestrator_server

# 加载环境变量
load_dotenv()

logger = logging.getLogger(__name__)


@click.command()
@click.option('--host', default='localhost', help='Host to bind to')
@click.option('--port', default=8000, type=int, help='Port to bind to')
@click.option('--debug', is_flag=True, help='Enable debug mode')
def main(host: str, port: int, debug: bool):
    """启动Orchestrator Agent服务器"""
    
    # 配置日志
    log_level = logging.DEBUG if debug else logging.INFO
    logging.basicConfig(
        level=log_level,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    logger.info("🎭 启动Orchestrator Agent服务器")
    logger.info(f"📍 地址: http://{host}:{port}")
    logger.info(f"🔍 AgentCard: http://{host}:{port}/.well-known/agent.json")
    logger.info(f"📝 任务端点: http://{host}:{port}/tasks/send")
    
    # 创建并启动服务器
    server = create_orchestrator_server(host, port)
    
    try:
        uvicorn.run(
            server.build(), 
            host=host, 
            port=port,
            log_level="info" if not debug else "debug"
        )
    except KeyboardInterrupt:
        logger.info("⏹️ 服务器被用户中断")
    except Exception as e:
        logger.error(f"❌ 服务器运行错误: {e}")


if __name__ == "__main__":
    main() 