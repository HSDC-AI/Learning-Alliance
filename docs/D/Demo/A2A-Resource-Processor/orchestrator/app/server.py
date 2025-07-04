"""
Orchestrator Server - A2A服务器创建和配置
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

from .agent_executor import OrchestratorAgentExecutor

logger = logging.getLogger(__name__)


def create_orchestrator_server(host: str = "localhost", port: int = 8000) -> A2AStarletteApplication:
    """创建编排器A2A服务器"""
    
    logger.info(f"🎭 创建编排器服务器: {host}:{port}")
    
    # 创建Agent卡片
    agent_card = AgentCard(
        name="Resource Processing Orchestrator",
        description="资源处理编排器 - 协调资源分析、图片处理、资源替换的完整工作流",
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
            tool_calling=True,
            streaming=True
        ),
        skills=[
            AgentSkill(
                id="resource_workflow_orchestration",
                name="资源工作流编排",
                description="编排资源处理工作流",
                tags=["编排", "工作流", "资源处理"],
                parameters={
                    "type": "object",
                    "properties": {
                        "directory_path": {
                            "type": "string",
                            "description": "要处理的资源目录路径"
                        },
                        "target_color": {
                            "type": "string", 
                            "description": "目标主题色（默认为红色）",
                            "default": "red"
                        },
                        "backup_enabled": {
                            "type": "boolean",
                            "description": "是否启用备份（默认启用）",
                            "default": True
                        }
                    },
                    "required": ["directory_path"]
                }
            ),
            AgentSkill(
                id="workflow_status_query",
                name="工作流状态查询",
                description="查询工作流执行状态",
                tags=["查询", "状态", "工作流"],
                parameters={
                    "type": "object", 
                    "properties": {
                        "workflow_id": {
                            "type": "string",
                            "description": "工作流ID"
                        }
                    },
                    "required": ["workflow_id"]
                }
            ),
            AgentSkill(
                id="agent_coordination",
                name="Agent协调",
                description="协调多个Agent间的通信和任务分配",
                tags=["协调", "通信", "任务分配"],
                parameters={
                    "type": "object",
                    "properties": {
                        "agents": {
                            "type": "array",
                            "items": {"type": "string"},
                            "description": "参与协调的Agent列表"
                        },
                        "task_type": {
                            "type": "string",
                            "description": "任务类型"
                        }
                    },
                    "required": ["agents", "task_type"]
                }
            )
        ]
    )
    
    # 创建任务存储
    task_store = InMemoryTaskStore()
    
    # 创建Agent执行器
    agent_executor = OrchestratorAgentExecutor()
    
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
    
    logger.info("✅ 编排器服务器创建完成")
    logger.info(f"📝 Agent名称: {agent_card.name}")
    logger.info(f"🔧 支持技能: {len(agent_card.skills)} 个")
    
    return app 