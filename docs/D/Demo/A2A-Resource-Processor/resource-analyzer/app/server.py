"""
Resource Analyzer Server - A2A服务器创建和配置
"""

import logging
from a2a.server.apps import A2AStarletteApplication
from a2a.server.request_handlers import DefaultRequestHandler
from a2a.server.tasks import InMemoryTaskStore
from a2a.types import (
    AgentCapabilities,
    AgentCard,
    AgentSkill,
)

from .agent_executor import ResourceAnalyzerAgentExecutor

logger = logging.getLogger(__name__)


def create_resource_analyzer_server(host: str = "localhost", port: int = 8001) -> A2AStarletteApplication:
    """创建资源分析器A2A服务器"""
    
    logger.info(f"🔍 创建资源分析器服务器: {host}:{port}")
    
    # 创建Agent卡片
    agent_card = AgentCard(
        name="Resource Analyzer",
        description="资源分析器 - 递归扫描目录、识别图片文件、分析颜色信息",
        version="1.0.0",
        author="A2A Resource Processor Team",
        license="MIT",
        homepage="https://github.com/a2a/resource-processor",
        url=f"http://{host}:{port}",
        defaultInputModes=["text"],
        defaultOutputModes=["text", "application/json"],
        capabilities=AgentCapabilities(
            text_generation=True,
            json_mode=True,
            vision=True,
            tool_calling=False,
            streaming=True
        ),
        skills=[
            AgentSkill(
                id="directory_analysis",
                name="目录分析",
                description="分析目录结构和文件信息",
                tags=["目录", "文件", "分析"],
                parameters={
                    "type": "object",
                    "properties": {
                        "directory_path": {
                            "type": "string",
                            "description": "要分析的目录路径"
                        },
                        "include_subdirs": {
                            "type": "boolean",
                            "description": "是否包含子目录（默认包含）",
                            "default": True
                        },
                        "file_types": {
                            "type": "array",
                            "items": {"type": "string"},
                            "description": "要分析的文件类型（默认所有类型）"
                        }
                    },
                    "required": ["directory_path"]
                }
            ),
            AgentSkill(
                id="image_color_analysis",
                name="图像颜色分析", 
                description="分析图片的颜色信息和主题色",
                tags=["图像", "颜色", "分析"],
                parameters={
                    "type": "object",
                    "properties": {
                        "image_paths": {
                            "type": "array",
                            "items": {"type": "string"},
                            "description": "图片文件路径列表"
                        },
                        "color_count": {
                            "type": "integer",
                            "description": "分析的主要颜色数量（默认5个）",
                            "default": 5
                        }
                    },
                    "required": ["image_paths"]
                }
            ),
            AgentSkill(
                id="file_information",
                name="文件信息",
                description="获取文件的详细信息（大小、类型、修改时间等）",
                tags=["文件", "信息", "元数据"],
                parameters={
                    "type": "object",
                    "properties": {
                        "file_paths": {
                            "type": "array", 
                            "items": {"type": "string"},
                            "description": "文件路径列表"
                        },
                        "include_hash": {
                            "type": "boolean",
                            "description": "是否计算文件哈希值（默认计算）",
                            "default": True
                        }
                    },
                    "required": ["file_paths"]
                }
            )
        ]
    )
    
    # 创建任务存储
    task_store = InMemoryTaskStore()
    
    # 创建Agent执行器
    agent_executor = ResourceAnalyzerAgentExecutor()
    
    # 创建请求处理器
    request_handler = DefaultRequestHandler(
        agent_executor=agent_executor,
        task_store=task_store
    )
    
    # 创建A2A应用
    app = A2AStarletteApplication(
        agent_card=agent_card,
        http_handler=request_handler
    )
    
    logger.info("✅ 资源分析器服务器创建完成")
    logger.info(f"📝 Agent名称: {agent_card.name}")
    logger.info(f"🔧 支持技能: {len(agent_card.skills)} 个")
    
    return app 