"""
修改版的 AgentExecutor - 集成yield流式处理
展示如何在现有A2A系统中正确使用yield
"""

import asyncio
import logging
import json

from a2a.server.agent_execution import AgentExecutor, RequestContext
from a2a.server.events import EventQueue
from a2a.utils import new_agent_text_message, new_data_artifact

from .streaming_agent import StreamingResourceProcessorOrchestrator

logger = logging.getLogger(__name__)


class StreamingOrchestratorAgentExecutor(AgentExecutor):
    """
    使用yield的编排器Agent执行器
    这是在A2A系统中正确使用yield的方式
    """
    
    def __init__(self):
        # 使用流式处理器
        self.streaming_processor = StreamingResourceProcessorOrchestrator()
        logger.info("🎭 StreamingOrchestratorAgentExecutor 初始化完成")
    
    async def execute(
        self,
        context: RequestContext,
        event_queue: EventQueue,
    ) -> None:
        """
        执行编排任务 - 使用yield实现流式响应
        这是Agent内部正确使用yield的关键方法
        """
        logger.info(f"📨 收到编排任务: {context.task_id}")
        
        try:
            # 解析用户消息
            user_message = ""
            if context.request.params.message and context.request.params.message.parts:
                user_message = " ".join([
                    part.text for part in context.request.params.message.parts 
                    if hasattr(part, 'text')
                ])
            
            session_id = context.request.params.session_id or context.task_id
            logger.info(f"📝 用户请求: {user_message}")
            logger.info(f"🔖 会话ID: {session_id}")
            
            # 🌟 关键：这里使用yield流式处理器
            # 每次yield都会实时发送状态给客户端
            async for update in self.streaming_processor.process_resources_stream(user_message, session_id):
                
                # 根据更新类型决定如何发送给客户端
                await self._handle_stream_update(update, event_queue)
                
                # 可选：记录详细日志
                logger.info(f"流式更新: {update['type']} - {update['message']} ({update.get('progress', 'N/A')}%)")
            
            logger.info(f"✅ 编排任务完成: {context.task_id}")
            
        except Exception as e:
            logger.error(f"❌ 编排任务执行失败: {e}")
            
            # 发送错误消息
            await event_queue.enqueue_event(
                new_agent_text_message(f"❌ 编排器执行失败: {str(e)}")
            )
            
            # 发送错误详情
            error_result = {
                "status": "error",
                "error": str(e),
                "error_type": type(e).__name__,
                "task_id": context.task_id
            }
            
            await event_queue.enqueue_event(
                new_data_artifact(
                    data=error_result,
                    artifact_type="application/json",
                    title="error_details"
                )
            )
    
    async def _handle_stream_update(self, update: dict, event_queue: EventQueue) -> None:
        """
        处理流式更新 - 将yield的结果转换为客户端消息
        这展示了yield在Agent内部的实际应用
        """
        
        update_type = update.get("type")
        message = update.get("message", "")
        progress = update.get("progress", 0)
        data = update.get("data", {})
        
        # 1. 发送进度消息
        if update_type in [
            "workflow_start", 
            "step_start", 
            "step_complete", 
            "workflow_complete",
            "workflow_error"
        ]:
            # 重要里程碑 - 总是发送
            progress_text = f"[{progress}%] {message}" if progress >= 0 else message
            await event_queue.enqueue_event(
                new_agent_text_message(progress_text)
            )
            
        elif update_type in [
            "sub_agent_progress", 
            "batch_progress", 
            "file_operation"
        ]:
            # 详细进度 - 选择性发送（避免消息过多）
            if progress > 0 and progress % 20 == 0:  # 每20%发送一次
                progress_text = f"[{progress}%] {message}"
                await event_queue.enqueue_event(
                    new_agent_text_message(progress_text)
                )
        
        # 2. 发送结构化数据
        if update_type in ["step_complete", "workflow_complete"] and data:
            # 发送JSON结果数据
            try:
                await event_queue.enqueue_event(
                    new_data_artifact(
                        data=data,
                        artifact_type="application/json",
                        title=f"{update.get('step_name', 'result')}_data"
                    )
                )
            except Exception as e:
                logger.warning(f"⚠️ 发送数据失败: {e}")
        
        # 3. 特殊处理
        if update_type == "workflow_complete":
            # 工作流完成 - 发送最终总结
            summary = data.get("summary", {})
            if summary:
                summary_text = f"""
🎯 **最终处理结果:**
• 📁 分析文件: {summary.get('total_files_analyzed', 0)} 个
• 🎨 处理图片: {summary.get('images_processed', 0)} 个  
• 🔄 替换文件: {summary.get('files_replaced', 0)} 个
• ⏱️ 工作流ID: {data.get('workflow_id', 'N/A')}
• 🕐 处理时间: {data.get('duration', 0):.2f} 秒
                """.strip()
                
                await event_queue.enqueue_event(
                    new_agent_text_message(summary_text)
                )
        
        elif update_type == "workflow_error":
            # 错误处理 - 发送错误详情
            if data:
                await event_queue.enqueue_event(
                    new_data_artifact(
                        data=data,
                        artifact_type="application/json", 
                        title="error_details"
                    )
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


# 简化的单一功能Agent示例，展示yield的基本使用
class SimpleStreamingAgent:
    """
    简单的流式Agent示例
    展示yield在单一Agent中的基本使用模式
    """
    
    async def process_files(self, file_paths: list) -> dict:
        """
        处理文件列表 - 使用yield提供实时进度
        这是Agent内部使用yield的最基本模式
        """
        
        total_files = len(file_paths)
        processed_files = []
        
        for i, file_path in enumerate(file_paths):
            # 模拟文件处理
            await asyncio.sleep(0.5)
            
            # 🌟 关键：yield当前进度
            progress = int((i + 1) / total_files * 100)
            
            yield {
                "type": "file_progress",
                "message": f"正在处理文件: {file_path}",
                "progress": progress,
                "current_file": file_path,
                "completed": i + 1,
                "total": total_files
            }
            
            # 处理完成
            processed_files.append({
                "file_path": file_path,
                "status": "success",
                "size": len(file_path) * 100  # 模拟文件大小
            })
        
        # 最终结果
        yield {
            "type": "completion",
            "message": "所有文件处理完成",
            "progress": 100,
            "result": {
                "total_processed": len(processed_files),
                "files": processed_files
            }
        }


class SimpleStreamingAgentExecutor(AgentExecutor):
    """
    简单的流式AgentExecutor示例
    展示yield的最基本集成方式
    """
    
    def __init__(self):
        self.agent = SimpleStreamingAgent()
    
    async def execute(
        self,
        context: RequestContext,
        event_queue: EventQueue,
    ) -> None:
        """执行简单的流式处理"""
        
        # 模拟文件列表
        file_paths = [
            "image1.png", "image2.jpg", "document.pdf", 
            "video.mp4", "audio.mp3"
        ]
        
        # 🌟 使用Agent的yield方法
        async for update in self.agent.process_files(file_paths):
            
            # 发送进度消息
            message_text = f"[{update['progress']}%] {update['message']}"
            await event_queue.enqueue_event(
                new_agent_text_message(message_text)
            )
            
            # 完成时发送结果数据
            if update["type"] == "completion":
                await event_queue.enqueue_event(
                    new_data_artifact(
                        data=update["result"],
                        artifact_type="application/json",
                        title="processing_result"
                    )
                )
    
    async def cancel(
        self, 
        context: RequestContext, 
        event_queue: EventQueue
    ) -> None:
        """取消处理"""
        await event_queue.enqueue_event(
            new_agent_text_message("🛑 处理已取消")
        ) 