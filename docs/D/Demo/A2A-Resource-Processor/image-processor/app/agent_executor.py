"""
Image Processor Agent Executor - A2A AgentExecutor实现
"""

import asyncio
import logging
import json

from a2a.server.agent_execution import AgentExecutor, RequestContext
from a2a.server.events import EventQueue
from a2a.utils import new_agent_text_message, new_data_artifact
import json

from .agent import ImageProcessor

logger = logging.getLogger(__name__)


class ImageProcessorAgentExecutor(AgentExecutor):
    """图片处理器Agent执行器"""
    
    def __init__(self):
        self.processor = ImageProcessor()
        logger.info("🎨 ImageProcessorAgentExecutor 初始化完成")
    
    async def execute(
        self,
        context: RequestContext,
        event_queue: EventQueue,
    ) -> None:
        """执行图片处理任务"""
        logger.info(f"📨 收到图片处理任务: {context.task_id}")
        
        try:
            # 获取用户消息
            user_message = ""
            if context.request.params.message and context.request.params.message.parts:
                user_message = " ".join([
                    part.text for part in context.request.params.message.parts 
                    if hasattr(part, 'text')
                ])
            
            logger.info(f"📝 处理请求: {user_message}")
            
            # 发送开始消息
            await event_queue.enqueue_event(
                new_agent_text_message("🎨 开始处理图片，正在应用红色主题...")
            )
            
            # 发送进度更新
            await event_queue.enqueue_event(
                new_agent_text_message("🔄 正在分析图片颜色信息...")
            )
            
            # 执行图片处理
            result = await self.processor.process_images(user_message)
            
            # 发送处理完成消息
            summary = result.get("summary", {})
            summary_text = f"""
🎨 **图片处理完成:**
- 🖼️ 总图片数: {summary.get('total_images', 0)}
- ✅ 处理成功: {summary.get('processed_images', 0)}
- ❌ 处理失败: {summary.get('failed_images', 0)}
- ⏱️ 处理时间: {summary.get('processing_time', 0):.2f} 秒
- 🎯 目标颜色: {result.get('target_color', {}).get('hex', '#FF0000')}
- 📁 输出目录: {result.get('output_directory', 'N/A')}
            """.strip()
            
            await event_queue.enqueue_event(
                new_agent_text_message(summary_text)
            )
            
            # 发送详细结果
            if summary.get("errors"):
                error_text = "⚠️ **处理过程中遇到的问题:**\n" + "\n".join(summary["errors"])
                await event_queue.enqueue_event(
                    new_agent_text_message(error_text)
                )
            
            # 发送处理细节
            if result.get("processing_details"):
                details_text = "📋 **处理详情:**\n"
                for i, detail in enumerate(result["processing_details"][:5]):  # 只显示前5个
                    status = "✅" if detail.get("success") else "❌"
                    name = detail.get("image_name", f"图片{i+1}")
                    details_text += f"{status} {name}\n"
                
                if len(result["processing_details"]) > 5:
                    details_text += f"... 还有 {len(result['processing_details']) - 5} 个图片"
                
                await event_queue.enqueue_event(
                    new_agent_text_message(details_text)
                )
            
            # 发送JSON结果
            await event_queue.enqueue_event(
                new_agent_text_message(f"🎨 处理结果:\n```json\n{json.dumps(result, indent=2, ensure_ascii=False)}\n```")
            )
            
        except Exception as e:
            logger.error(f"❌ 图片处理失败: {e}")
            await event_queue.enqueue_event(
                new_agent_text_message(f"❌ 图片处理失败: {str(e)}")
            )
            
            error_result = {
                "status": "error",
                "error": str(e),
                "task_id": context.task_id
            }
            await event_queue.enqueue_event(
                new_agent_text_message(f"❌ 错误详情:\n```json\n{json.dumps(error_result, indent=2, ensure_ascii=False)}\n```")
            )
    
    async def cancel(
        self, 
        context: RequestContext, 
        event_queue: EventQueue
    ) -> None:
        """取消图片处理任务"""
        logger.info(f"🛑 取消图片处理任务: {context.task_id}")
        await event_queue.enqueue_event(
            new_agent_text_message("🛑 图片处理任务已取消")
        ) 