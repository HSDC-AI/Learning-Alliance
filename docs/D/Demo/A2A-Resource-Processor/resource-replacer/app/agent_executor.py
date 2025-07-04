"""
Resource Replacer Agent Executor - A2A AgentExecutor实现
"""

import asyncio
import logging
import json

from a2a.server.agent_execution import AgentExecutor, RequestContext
from a2a.server.events import EventQueue
from a2a.utils import new_agent_text_message, new_data_artifact
import json

from .agent import ResourceReplacer

logger = logging.getLogger(__name__)


class ResourceReplacerAgentExecutor(AgentExecutor):
    """资源替换器Agent执行器"""
    
    def __init__(self):
        self.replacer = ResourceReplacer()
        logger.info("📁 ResourceReplacerAgentExecutor 初始化完成")
    
    async def execute(
        self,
        context: RequestContext,
        event_queue: EventQueue,
    ) -> None:
        """执行资源替换任务"""
        logger.info(f"📨 收到资源替换任务: {context.task_id}")
        
        try:
            # 获取用户消息
            user_message = ""
            if context.request.params.message and context.request.params.message.parts:
                user_message = " ".join([
                    part.text for part in context.request.params.message.parts 
                    if hasattr(part, 'text')
                ])
            
            logger.info(f"📝 替换请求: {user_message}")
            
            # 发送开始消息
            await event_queue.enqueue_event(
                new_agent_text_message("📁 开始替换资源文件，正在创建备份...")
            )
            
            # 发送进度更新
            await event_queue.enqueue_event(
                new_agent_text_message("🔄 正在执行文件替换操作...")
            )
            
            # 执行资源替换
            result = await self.replacer.replace_resources(user_message)
            
            # 发送替换完成消息
            summary = result.get("summary", {})
            summary_text = f"""
📁 **资源替换完成:**
- 📄 总文件数: {summary.get('total_files', 0)}
- ✅ 替换成功: {summary.get('replaced_files', 0)}
- 🗂️ 备份文件: {summary.get('backed_up_files', 0)}
- ❌ 替换失败: {summary.get('failed_files', 0)}
- ⏱️ 替换时间: {summary.get('replacement_time', 0):.2f} 秒
- 📁 备份目录: {result.get('backup_directory', 'N/A')}
            """.strip()
            
            await event_queue.enqueue_event(
                new_agent_text_message(summary_text)
            )
            
            # 发送详细结果
            if summary.get("errors"):
                error_text = "⚠️ **替换过程中遇到的问题:**\n" + "\n".join(summary["errors"])
                await event_queue.enqueue_event(
                    new_agent_text_message(error_text)
                )
            
            # 发送替换细节
            if result.get("replacement_details"):
                details_text = "📋 **替换详情:**\n"
                for i, detail in enumerate(result["replacement_details"][:5]):  # 只显示前5个
                    status = "✅" if detail.get("success") else "❌"
                    original = detail.get("original_file", f"文件{i+1}")
                    backup_status = "🗂️" if detail.get("backed_up") else "⚠️"
                    details_text += f"{status} {original} {backup_status}\n"
                
                if len(result["replacement_details"]) > 5:
                    details_text += f"... 还有 {len(result['replacement_details']) - 5} 个文件"
                
                await event_queue.enqueue_event(
                    new_agent_text_message(details_text)
                )
            
            # 发送操作历史
            if result.get("operations"):
                ops_text = "📝 **执行的操作:**\n"
                for op in result["operations"]:
                    op_name = op.get("operation", "未知操作")
                    op_status = "✅" if op.get("success") else "❌"
                    ops_text += f"{op_status} {op_name}\n"
                
                await event_queue.enqueue_event(
                    new_agent_text_message(ops_text)
                )
            
            # 发送JSON结果
            await event_queue.enqueue_event(
                new_agent_text_message(f"📁 替换结果:\n```json\n{json.dumps(result, indent=2, ensure_ascii=False)}\n```")
            )
            
        except Exception as e:
            logger.error(f"❌ 资源替换失败: {e}")
            await event_queue.enqueue_event(
                new_agent_text_message(f"❌ 资源替换失败: {str(e)}")
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
        """取消资源替换任务"""
        logger.info(f"🛑 取消资源替换任务: {context.task_id}")
        await event_queue.enqueue_event(
            new_agent_text_message("🛑 资源替换任务已取消")
        ) 