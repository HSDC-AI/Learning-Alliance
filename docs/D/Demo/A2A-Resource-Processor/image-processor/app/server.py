"""
Image Processor Server - A2A服务器创建和配置
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

from .agent_executor import ImageProcessorAgentExecutor

logger = logging.getLogger(__name__)


def create_image_processor_server(host: str = "localhost", port: int = 8002) -> A2AStarletteApplication:
    """创建图片处理器A2A服务器"""
    
    logger.info(f"🎨 创建图片处理器服务器: {host}:{port}")
    
    # 创建Agent卡片
    agent_card = AgentCard(
        name="Image Processor",
        description="图片处理器 - 图片主题色识别、颜色替换处理、批量图片操作",
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
                id="image_color_processing",
                name="图像颜色处理",
                description="图片颜色主题替换和处理",
                tags=["图像", "颜色", "处理"],
                parameters={
                    "type": "object",
                    "properties": {
                        "image_paths": {
                            "type": "array",
                            "items": {"type": "string"},
                            "description": "要处理的图片文件路径列表"
                        },
                        "target_color": {
                            "type": "string",
                            "description": "目标主题色（默认为红色）",
                            "default": "red"
                        },
                        "output_directory": {
                            "type": "string",
                            "description": "输出目录路径（可选）"
                        },
                        "enhance_quality": {
                            "type": "boolean",
                            "description": "是否增强图片质量（默认启用）",
                            "default": True
                        }
                    },
                    "required": ["image_paths"]
                }
            ),
            AgentSkill(
                id="batch_image_processing",
                name="批量图像处理",
                description="批量图片处理和转换",
                tags=["批量", "图像", "转换"],
                parameters={
                    "type": "object",
                    "properties": {
                        "source_directory": {
                            "type": "string",
                            "description": "源图片目录"
                        },
                        "filter_patterns": {
                            "type": "array",
                            "items": {"type": "string"},
                            "description": "文件过滤模式（如 *.jpg, *.png）"
                        },
                        "processing_options": {
                            "type": "object",
                            "description": "处理选项配置"
                        }
                    },
                    "required": ["source_directory"]
                }
            ),
            AgentSkill(
                id="color_analysis",
                name="颜色分析",
                description="图片颜色分析和主题色提取",
                tags=["颜色", "分析", "提取"],
                parameters={
                    "type": "object",
                    "properties": {
                        "image_path": {
                            "type": "string",
                            "description": "图片文件路径"
                        },
                        "analysis_depth": {
                            "type": "string",
                            "enum": ["basic", "detailed", "comprehensive"],
                            "description": "分析深度（默认基础）",
                            "default": "basic"
                        }
                    },
                    "required": ["image_path"]
                }
            )
        ]
    )
    
    # 创建任务存储
    task_store = InMemoryTaskStore()
    
    # 创建Agent执行器
    agent_executor = ImageProcessorAgentExecutor()
    
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
    
    logger.info("✅ 图片处理器服务器创建完成")
    logger.info(f"📝 Agent名称: {agent_card.name}")
    logger.info(f"🔧 支持技能: {len(agent_card.skills)} 个")
    
    return app 