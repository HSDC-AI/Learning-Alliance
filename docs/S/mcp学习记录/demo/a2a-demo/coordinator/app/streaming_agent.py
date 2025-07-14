"""
Streaming Resource Processor - 使用yield实现流式处理的Agent核心逻辑
展示在Agent内部如何正确使用yield
"""

import asyncio
import logging
import uuid
from typing import Dict, Any, Optional, AsyncGenerator
from datetime import datetime
import os
import httpx

from a2a.client import A2ACardResolver, A2AClient
from a2a.utils import new_agent_text_message, new_data_artifact
from a2a.types import MessageSendParams, SendMessageRequest

logger = logging.getLogger(__name__)


class StreamingCoordinatorAgent:
    """流式资源处理编排器 - 在Agent内部使用yield"""

    def __init__(self):
        # Agent注册表
        self.agent_registry = {
            "data_collector": os.getenv("DATA_COLLECTOR_URL", "http://localhost:10000"),
        }

        logger.info("🎭 StreamingCoordinatorAgent 初始化完成")

    async def process_resources_stream(self, user_message: str, session_id: str) -> AsyncGenerator[Dict[str, Any], None]:
        """
        流式处理资源的核心方法 - 这是Agent内部使用yield的正确方式
        每个处理步骤都通过yield返回状态给客户端
        """

        workflow_id = str(uuid.uuid4())
        start_time = datetime.now()

        # 步骤0: 初始化
        yield {
            "type": "workflow_start",
            "workflow_id": workflow_id,
            "message": "🎭 编排器已启动，开始协调资源处理工作流",
            "progress": 0,
            "timestamp": start_time.isoformat(),
            "data": {
                "user_message": user_message,
                "session_id": session_id,
                "available_agents": list(self.agent_registry.keys())
            }
        }

        try:
            # 步骤1: 资源分析 (0-30%)
            yield {
                "type": "step_start",
                "step_name": "analyzing_monitor_data",
                "message": "📊 步骤1: 开始监控数据分析",
                "progress": 100,
                "timestamp": datetime.now().isoformat(),
                "data": {"target_agent": "data_collector"}
            }

            # 调用资源分析Agent - 这里也会有子进度
            async for sub_progress in self._call_agent_stream("data_collector", user_message, session_id):
                # 将子Agent的进度转换为整体进度 (10-30%)
                overall_progress = 10 + (sub_progress.get("progress", 0) * 0.2)

                yield {
                    "type": "sub_agent_progress",
                    "step_name": "analyzing_monitor_data",
                    "agent_name": "data_collector",
                    "message": f"📊 资源分析: {sub_progress.get('message', '')}",
                    "progress": int(overall_progress),
                    "timestamp": datetime.now().isoformat(),
                    "data": sub_progress.get("data", {})
                }

            # 工作流完成
            end_time = datetime.now()
            duration = (end_time - start_time).total_seconds()

            final_result = {
                "workflow_id": workflow_id,
                "status": "success",
                "duration": duration
            }

            yield {
                "type": "workflow_complete",
                "step_name": "completed",
                "message": "🎉 资源处理工作流完成！",
                "progress": 100,
                "timestamp": end_time.isoformat(),
                "data": final_result
            }

        except Exception as e:
            error_time = datetime.now()
            logger.error(f"❌ 工作流执行失败: {e}")

            yield {
                "type": "workflow_error",
                "step_name": "error",
                "message": f"❌ 工作流执行失败: {str(e)}",
                "progress": -1,
                "timestamp": error_time.isoformat(),
                "data": {
                    "error_type": type(e).__name__,
                    "error_message": str(e),
                    "workflow_id": workflow_id
                }
            }

    async def _call_agent_stream(self, agent_name: str, message: str, session_id: str) -> AsyncGenerator[Dict[str, Any], None]:
        """
        调用子Agent并返回流式进度
        这展示了Agent间通信中的yield使用
        """

        if agent_name not in self.agent_registry:
            yield {
                "status": "error",
                "message": f"Agent {agent_name} 未注册",
                "progress": 0,
                "data": {"error": f"Agent {agent_name} not found"}
            }
            return

        agent_url = self.agent_registry[agent_name]

        # 连接Agent
        yield {
            "status": "connecting",
            "message": f"正在连接到 {agent_name}...",
            "progress": 10,
            "data": {"agent_url": agent_url}
        }

        try:
            async with httpx.AsyncClient(timeout=60.0) as client:
                # 获取Agent卡片
                yield {
                    "status": "resolving",
                    "message": f"正在获取 {agent_name} 的Agent卡片...",
                    "progress": 30,
                    "data": {"action": "get_agent_card"}
                }

                resolver = A2ACardResolver(
                    httpx_client=client,
                    base_url=agent_url
                )

                try:
                    agent_card = await resolver.get_agent_card()

                    yield {
                        "status": "connected",
                        "message": f"已连接到 {agent_name}: {agent_card.name}",
                        "progress": 50,
                        "data": {
                            "agent_name": agent_card.name,
                            "agent_description": agent_card.description
                        }
                    }

                except Exception as e:
                    yield {
                        "status": "connection_failed",
                        "message": f"连接 {agent_name} 失败: {str(e)}",
                        "progress": 0,
                        "data": {"error": str(e)}
                    }
                    return

                # 发送消息
                yield {
                    "status": "sending_request",
                    "message": f"正在向 {agent_name} 发送请求...",
                    "progress": 70,
                    "data": {"message_length": len(message)}
                }

                # 模拟Agent处理时间
                await asyncio.sleep(1)

                yield {
                    "status": "processing",
                    "message": f"{agent_name} 正在处理请求...",
                    "progress": 90,
                    "data": {"agent": agent_name}
                }

                await asyncio.sleep(1)

                # 模拟响应
                mock_response = {
                    "agent": agent_name,
                    "result": "success",
                    "data": f"Processed by {agent_name}"
                }

                yield {
                    "status": "completed",
                    "message": f"✅ {agent_name} 处理完成",
                    "progress": 100,
                    "data": {
                        "response": mock_response,
                        "agent": agent_name
                    }
                }

        except Exception as e:
            yield {
                "status": "error",
                "message": f"调用 {agent_name} 时发生错误: {str(e)}",
                "progress": 0,
                "data": {
                    "error_type": type(e).__name__,
                    "error_message": str(e),
                    "agent": agent_name
                }
            }


# 这是如何在AgentExecutor中使用上面的流式处理器
class StreamingAgentExecutor:
    """展示如何在AgentExecutor中正确使用yield"""

    def __init__(self):
        self.processor = StreamingCoordinatorAgent()

    async def execute_with_streaming(self, user_message: str, session_id: str, event_queue):
        """
        在AgentExecutor中使用yield处理器的正确方式
        这里接收yield的结果并通过event_queue发送给客户端
        """

        async for update in self.processor.process_resources_stream(user_message, session_id):
            # 将yield的每个更新转换为Agent消息发送给客户端

            if update["type"] in ["workflow_start", "step_start", "step_complete", "workflow_complete"]:
                # 重要的里程碑消息
                message_text = f"[{update['progress']}%] {update['message']}"
                await event_queue.enqueue_event(
                    new_agent_text_message(message_text)
                )

            elif update["type"] in ["sub_agent_progress", "batch_progress", "file_operation"]:
                # 详细进度消息（可选择性发送，避免消息过多）
                if update["progress"] % 10 == 0:  # 每10%发送一次
                    message_text = f"[{update['progress']}%] {update['message']}"
                    await event_queue.enqueue_event(
                        new_agent_text_message(message_text)
                    )

            elif update["type"] == "workflow_error":
                # 错误消息
                await event_queue.enqueue_event(
                    new_agent_text_message(update['message'])
                )

            # 可以选择在某些关键点发送JSON数据
            if update["type"] in ["workflow_complete", "step_complete"]:
                await event_queue.enqueue_event(
                    new_data_artifact(
                        data=update["data"],
                        artifact_type="application/json",
                        title=f"{update['step_name']}_result"
                    )
                )

            # 在真实系统中，你也可以记录日志、更新数据库等
            logger.info(f"工作流更新: {update['type']} - {update['message']} ({update['progress']}%)")