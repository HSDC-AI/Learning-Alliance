# agent_executor.py
import logging
import json
import asyncio
import uuid
import re

from a2a.server.agent_execution import AgentExecutor, RequestContext
from a2a.server.events import EventQueue
from a2a.utils import new_agent_text_message

from agent import CoordinatorAgent

logger = logging.getLogger(__name__)

class CoordinatorAgentExecutor(AgentExecutor):
    """协调Agent执行器"""

    def __init__(self):
        self.agent = CoordinatorAgent()
        logger.info("🧠 CoordinatorAgentExecutor 初始化完成")

    async def execute(
            self,
            context: RequestContext,
            event_queue: EventQueue,
    ) -> None:
        """执行监控突刺分析任务"""
        logger.info(f"📨 收到监控突刺分析任务: {context.task_id}")
        try:
            # 获取用户消息
            user_message = ""
            # if context.request.params.message and context.request.params.message.parts:
            #     user_message = " ".join([
            #         part.text for part in context.request.params.message.parts
            #         if hasattr(part, 'text') and part.text
            #     ])

            # 使用请求中的session_id或生成新的
            session_id = str(uuid.uuid4())
            logger.info(f"📝 用户请求: {user_message}")
            logger.info(f"🔖 会话ID: {session_id}")

            # 发送开始消息
            await event_queue.enqueue_event(
                new_agent_text_message("🎭 编排器已启动，开始协调资源处理工作流...")
            )

            # 提取时间范围
            start_time, end_time = self._extract_time_range(user_message)

            if not start_time or not end_time:
                # 尝试从消息中提取时间范围
                start_time, end_time = self._parse_time_range(user_message)

            if not start_time or not end_time:
                raise ValueError("无法从消息中提取有效的时间范围，请提供开始时间和结束时间")

            await event_queue.enqueue_event(
                new_agent_text_message(f"⏱️ 分析时间范围: {start_time} 至 {end_time}")
            )

            # 执行工作流
            result = await self.agent.process_resources(start_time, end_time, session_id)

            print(result)

            if result.get("status") == "success":
                # 成功完成
                await event_queue.enqueue_event(
                    new_agent_text_message("✅ 资源处理工作流已完成！")
                )

                # 发送详细结果
                summary = result.get("summary", {})
                summary_text = f"""
                    🎯 **处理结果总结:**
                    - 📁 工作流ID: {summary.get('workflow_id', 'N/A')}
                    - 🕐 开始时间: {summary.get('start_time', 'N/A')}
                    - 🕛 结束时间: {summary.get('end_time', 'N/A')}
                    - 📊 结果: {json.dumps(summary.get('results', {}), ensure_ascii=False)[:200]}...
                """.strip()

                await event_queue.enqueue_event(
                    new_agent_text_message(summary_text)
                )

            else:
                # 处理失败
                error_msg = result.get("error", "未知错误")
                await event_queue.enqueue_event(
                    new_agent_text_message(f"❌ 监控突刺分析失败: {error_msg}")
                )

        except Exception as e:
            logger.exception(f"❌ 监控突刺分析失败")
            await event_queue.enqueue_event(
                new_agent_text_message(f"❌ 监控突刺分析失败: {str(e)}")
            )

    def _extract_time_range(self, message: str) -> tuple:
        """从上下文中提取时间范围"""
        # 这里可以根据实际上下文获取时间范围
        # 示例中返回固定值
        return ("2025-06-30 12:00", "2025-06-30 13:00")

    def _parse_time_range(self, message: str) -> tuple:
        """从消息中解析时间范围"""
        # 简单的正则匹配示例
        pattern = r"(\d{4}-\d{2}-\d{2} \d{2}:\d{2})"
        matches = re.findall(pattern, message)

        if len(matches) >= 2:
            return matches[0], matches[1]
        return None, None

    async def cancel(
            self,
            context: RequestContext,
            event_queue: EventQueue
    ) -> None:
        """取消监控突刺分析任务"""
        logger.info(f"🛑 取消监控突刺分析任务: {context.task_id}")
        await event_queue.enqueue_event(
            new_agent_text_message("🛑 监控突刺分析任务已取消")
        )