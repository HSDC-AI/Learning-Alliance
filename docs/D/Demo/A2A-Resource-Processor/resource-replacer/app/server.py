"""
Resource Replacer Server - A2A服务器创建和配置
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

from .agent_executor import ResourceReplacerAgentExecutor

logger = logging.getLogger(__name__)


def create_resource_replacer_server(host: str = "localhost", port: int = 8003) -> A2AStarletteApplication:
    """创建资源替换器A2A服务器"""
    
    logger.info(f"📁 创建资源替换器服务器: {host}:{port}")
    
    # 创建Agent卡片
    agent_card = AgentCard(
        name="Resource Replacer",
        description="资源替换器 - 文件备份、安全替换、版本控制管理",
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
            vision=False,
            tool_calling=False,
            streaming=True
        ),
        skills=[
            AgentSkill(
                id="file_replacement",
                name="文件替换",
                description="安全的文件替换操作",
                tags=["文件", "替换", "安全"],
                parameters={
                    "type": "object",
                    "properties": {
                        "file_mappings": {
                            "type": "array",
                            "items": {
                                "type": "object",
                                "properties": {
                                    "source": {"type": "string", "description": "源文件路径"},
                                    "target": {"type": "string", "description": "目标文件路径"}
                                },
                                "required": ["source", "target"]
                            },
                            "description": "文件映射关系列表"
                        },
                        "backup_enabled": {
                            "type": "boolean",
                            "description": "是否创建备份（默认启用）",
                            "default": True
                        },
                        "backup_directory": {
                            "type": "string",
                            "description": "自定义备份目录（可选）"
                        }
                    },
                    "required": ["file_mappings"]
                }
            ),
            AgentSkill(
                id="backup_management",
                name="备份管理",
                description="备份文件管理和恢复",
                tags=["备份", "管理", "恢复"],
                parameters={
                    "type": "object",
                    "properties": {
                        "operation": {
                            "type": "string",
                            "enum": ["create", "list", "restore", "cleanup"],
                            "description": "备份操作类型"
                        },
                        "backup_directory": {
                            "type": "string",
                            "description": "备份目录路径"
                        },
                        "target_file": {
                            "type": "string",
                            "description": "目标文件路径（用于恢复操作）"
                        },
                        "backup_file": {
                            "type": "string",
                            "description": "备份文件路径（用于恢复操作）"
                        }
                    },
                    "required": ["operation"]
                }
            ),
            AgentSkill(
                id="version_control",
                name="版本控制",
                description="文件版本控制和历史管理",
                tags=["版本", "控制", "历史"],
                parameters={
                    "type": "object",
                    "properties": {
                        "action": {
                            "type": "string",
                            "enum": ["track", "list_versions", "compare", "rollback"],
                            "description": "版本控制操作"
                        },
                        "file_path": {
                            "type": "string",
                            "description": "文件路径"
                        },
                        "version_tag": {
                            "type": "string",
                            "description": "版本标签（可选）"
                        }
                    },
                    "required": ["action", "file_path"]
                }
            )
        ]
    )
    
    # 创建任务存储
    task_store = InMemoryTaskStore()
    
    # 创建Agent执行器
    agent_executor = ResourceReplacerAgentExecutor()
    
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
    
    logger.info("✅ 资源替换器服务器创建完成")
    logger.info(f"📝 Agent名称: {agent_card.name}")
    logger.info(f"🔧 支持技能: {len(agent_card.skills)} 个")
    
    return app 