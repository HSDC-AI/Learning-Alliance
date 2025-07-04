"""
Orchestrator Agent Executor - A2A AgentExecutor实现
"""

import asyncio
import logging
import json

from a2a.server.agent_execution import AgentExecutor, RequestContext
from a2a.server.events import EventQueue
from a2a.utils import new_agent_text_message, new_data_artifact
import json

from .agent import ResourceProcessorOrchestrator

logger = logging.getLogger(__name__)


class OrchestratorAgentExecutor(AgentExecutor):
    """编排器Agent执行器"""
    
    def __init__(self):
        self.orchestrator = ResourceProcessorOrchestrator()
        logger.info("🎭 OrchestratorAgentExecutor 初始化完成")
    
    async def execute(
        self,
        context: RequestContext,
        event_queue: EventQueue,
    ) -> None:
        """执行编排任务"""
        logger.info(f"📨 收到编排任务: {context.task_id}")
        
        try:
            # 获取用户消息
            user_message = ""
            if context.request.params.message and context.request.params.message.parts:
                user_message = " ".join([
                    part.text for part in context.request.params.message.parts 
                    if hasattr(part, 'text')
                ])
            
            session_id = context.request.params.session_id or context.task_id
            logger.info(f"📝 用户请求: {user_message}")
            logger.info(f"🔖 会话ID: {session_id}")
            
            # 发送开始消息
            await event_queue.enqueue_event(
                new_agent_text_message("🎭 编排器已启动，开始协调资源处理工作流...")
            )
            
            # 发送进度更新
            await event_queue.enqueue_event(
                new_agent_text_message("📊 步骤1/3: 正在分析资源目录...")
            )
            
            # 执行工作流
            result = await self.orchestrator.process_resources(user_message, session_id)
            
            if result.get("status") == "success":
                # 成功完成
                await event_queue.enqueue_event(
                    new_agent_text_message("✅ 资源处理工作流已完成！")
                )
                
                # 发送详细结果
                summary = result.get("summary", {})
                summary_text = f"""
🎯 **处理结果总结:**
- 📁 分析文件: {summary.get('total_files_analyzed', 0)} 个
- 🎨 处理图片: {summary.get('images_processed', 0)} 个  
- 🔄 替换文件: {summary.get('files_replaced', 0)} 个
- ⏱️ 工作流ID: {summary.get('workflow_id', 'N/A')}
- 🕐 开始时间: {summary.get('start_time', 'N/A')}
- 🕕 结束时间: {summary.get('end_time', 'N/A')}
                """.strip()
                
                await event_queue.enqueue_event(
                    new_agent_text_message(summary_text)
                )
                
                # 发送JSON结果
                await event_queue.enqueue_event(
                    new_agent_text_message(f"📊 详细结果:\n```json\n{json.dumps(result, indent=2, ensure_ascii=False)}\n```")
                )
                
            else:
                # 处理失败
                error_msg = result.get("error", "未知错误")
                await event_queue.enqueue_event(
                    new_agent_text_message(f"❌ 工作流执行失败: {error_msg}")
                )
                
                await event_queue.enqueue_event(
                    new_agent_text_message(f"❌ 错误详情:\n```json\n{json.dumps(result, indent=2, ensure_ascii=False)}\n```")
                )
            
        except Exception as e:
            logger.error(f"❌ 编排任务执行失败: {e}")
            await event_queue.enqueue_event(
                new_agent_text_message(f"❌ 编排器执行失败: {str(e)}")
            )
            
            error_result = {
                "status": "error",
                "error": str(e),
                "task_id": context.task_id
            }
            await event_queue.enqueue_event(
                new_agent_text_message(f"❌ 异常详情:\n```json\n{json.dumps(error_result, indent=2, ensure_ascii=False)}\n```")
            )
    
    async def cancel(
        self, 
        context: RequestContext, 
        event_queue: EventQueue
    ) -> None:
        """取消编排任务"""
        logger.info(f"🛑 取消编排任务: {context.task_id}")
        await event_queue.enqueue_event(
            new_agent_text_message("🛑 编排任务已取消")
        ) 