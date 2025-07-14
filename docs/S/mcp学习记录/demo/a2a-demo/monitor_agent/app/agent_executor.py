import json
import logging

from a2a.server.agent_execution import AgentExecutor, RequestContext
from a2a.server.events import EventQueue
from a2a.server.tasks import TaskUpdater
from a2a.types import (
    InternalError,
    InvalidParamsError,
    Part,
    TextPart,
    UnsupportedOperationError,
)
from a2a.utils import (
    new_agent_text_message,
    new_task,
)
from a2a.utils.errors import ServerError

from .agent import MonitoringDataAgent


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class MonitoringDataAgentExecutor(AgentExecutor):
    """Monitor Data AgentExecutor Example."""

    def __init__(self):
        self.agent = MonitoringDataAgent()

    async def execute(
        self,
        context: RequestContext,
        event_queue: EventQueue,
    ) -> None:

        error = self._validate_request(context)
        if error:
            raise ServerError(error=InvalidParamsError())

        query = context.get_user_input()

        task = context.current_task
        if not task:
            task = new_task(context.message) # type: ignore
            await event_queue.enqueue_event(task)
        updater = TaskUpdater(event_queue, task.id, task.contextId)
        try:
            async for item in self.agent.stream(json.loads(query).get('start_time'), json.loads(query).get('end_time'), task.contextId):
                await updater.add_artifact(
                    [Part(root=TextPart(text=json.dumps(item['content'])))],
                    name='conversion_result',
                )
                await updater.complete()
                break

        except Exception as e:
            logger.error(f'An error occurred while streaming the response: {e}')
            raise ServerError(error=InternalError()) from e

    def _validate_request(self, context: RequestContext) -> bool:
        return False

    async def cancel(
        self, context: RequestContext, event_queue: EventQueue
    ) -> None:
        raise ServerError(error=UnsupportedOperationError())
