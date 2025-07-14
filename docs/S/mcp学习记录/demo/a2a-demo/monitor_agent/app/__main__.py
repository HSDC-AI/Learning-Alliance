import logging
import sys
import click
import httpx
import uvicorn
from a2a.server.apps import A2AStarletteApplication
from a2a.server.request_handlers import DefaultRequestHandler
from a2a.server.tasks import InMemoryPushNotifier, InMemoryTaskStore
from a2a.types import (
    AgentCapabilities,
    AgentCard,
    AgentSkill,
)
from dotenv import load_dotenv

from .agent import MonitoringDataAgent
from .agent_executor import MonitoringDataAgentExecutor


load_dotenv()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class MissingAPIKeyError(Exception):
    """Exception for missing API key."""


@click.command()
@click.option('--host', default='localhost', help='Host to bind to')
@click.option('--port', default=10000, type=int, help='Port to bind to')
# @click.option('--debug', is_flag=True, help='Enable debug mode')
def main(host, port):
    """Starts the monitor Agent server."""
    try:
        capabilities = AgentCapabilities(streaming=True, pushNotifications=True)
        skill = AgentSkill(
            id="get_monitoring_data",
            name="获取监控数据",
            description="获取指定时间范围内的监控数据",
            tags=["监控", "数据", "分析"],
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

        agent_card = AgentCard(
            name="MonitoringDataAgent",
            description="监控数据获取Agent - 从监控系统获取指定时间范围内的监控数据",
            version="1.0.0",
            author="Monitoring Team",
            license="MIT",
            homepage="https://github.com/monitoring-agents",
            url=f"http://{host}:{port}",
            defaultInputModes=MonitoringDataAgent.SUPPORTED_CONTENT_TYPES,
            defaultOutputModes=MonitoringDataAgent.SUPPORTED_CONTENT_TYPES,
            capabilities=capabilities,
            skills=[skill],
        )

        # --8<-- [start:DefaultRequestHandler]
        httpx_client = httpx.AsyncClient()
        request_handler = DefaultRequestHandler(
            agent_executor=MonitoringDataAgentExecutor(),
            task_store=InMemoryTaskStore(),
            push_notifier=InMemoryPushNotifier(httpx_client),
        )
        server = A2AStarletteApplication(
            agent_card=agent_card, http_handler=request_handler
        )

        uvicorn.run(server.build(), host=host, port=port)
        # --8<-- [end:DefaultRequestHandler]

    except MissingAPIKeyError as e:
        logger.error(f'Error: {e}')
        sys.exit(1)
    except Exception as e:
        logger.error(f'An error occurred during server startup: {e}')
        sys.exit(1)


if __name__ == '__main__':
    main()
