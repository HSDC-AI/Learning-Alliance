# server.py
import logging
from a2a.server.apps import A2AStarletteApplication
from a2a.server.request_handlers import DefaultRequestHandler
from a2a.server.tasks import InMemoryTaskStore
from a2a.types import AgentCapabilities, AgentCard, AgentSkill

from agent_executor import CoordinatorAgentExecutor

logger = logging.getLogger(__name__)

def create_coordinator_server(host: str = "0.0.0.0", port: int = 8001) -> A2AStarletteApplication:
    """创建协调A2A服务器"""
    logger.info(f"🚀 启动协调服务器: {host}:{port}")

    # 创建Agent卡片
    agent_card = AgentCard(
        name="CoordinatorAgent",
        description="协调Agent - 负责协调多个专业Agent完成监控突刺分析",
        version="1.0.0",
        author="Monitoring Analysis Team",
        license="MIT",
        homepage="https://github.com/coordinator-agents",
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
                id="monitoring_spike_analysis",
                name="监控突刺分析",
                description="分析监控数据中的突刺现象",
                tags=["监控", "分析", "协调"],
                parameters={
                    "type": "object",
                    "properties": {
                        "start_time": {
                            "type": "string",
                            "description": "开始时间，格式 YYYY-MM-DD HH:MM"
                        },
                        "end_time": {
                            "type": "string",
                            "description": "结束时间，格式 YYYY-MM-DD HH:MM"
                        }
                    },
                    "required": ["start_time", "end_time"]
                }
            )
        ],
        # 明确声明支持扩展卡片
        supportsAuthenticatedExtendedCard=True
    )

    # 创建任务存储
    task_store = InMemoryTaskStore()

    # 创建Agent执行器
    agent_executor = CoordinatorAgentExecutor()

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

    logger.info("✅ 协调服务器创建完成")
    return app