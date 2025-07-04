"""
Resource Analyzer Agent Executor - A2A AgentExecutor实现
"""

import asyncio
import logging
import json
from typing import Optional

from a2a.server.agent_execution import AgentExecutor, RequestContext
from a2a.server.events import EventQueue
from a2a.utils import new_agent_text_message, new_data_artifact
import json

from .agent import ResourceAnalyzer

logger = logging.getLogger(__name__)


class ResourceAnalyzerAgentExecutor(AgentExecutor):
    """资源分析器Agent执行器"""
    
    def __init__(self):
        self.analyzer = ResourceAnalyzer()
        logger.info("🔍 ResourceAnalyzerAgentExecutor 初始化完成")
    
    async def execute(
        self,
        context: RequestContext,
        event_queue: EventQueue,
    ) -> None:
        """执行资源分析任务"""
        logger.info(f"📨 收到资源分析任务: {context.task_id}")
        
        try:
            # 获取用户消息
            user_message = ""
            if context.request.params.message and context.request.params.message.parts:
                user_message = " ".join([
                    part.text for part in context.request.params.message.parts 
                    if hasattr(part, 'text')
                ])
            
            logger.info(f"📝 分析请求: {user_message}")
            
            # 发送开始消息
            await event_queue.enqueue_event(
                new_agent_text_message("🔍 开始分析资源目录，正在扫描文件结构...")
            )
            
            # 提取目录路径
            directory_path = self._extract_directory_path(user_message)
            
            if not directory_path:
                await event_queue.enqueue_event(
                    new_agent_text_message("⚠️ 未找到有效的目录路径，使用模拟分析...")
                )
                # 使用模拟路径
                directory_path = "./demo_resources"
            
            # 发送进度更新
            await event_queue.enqueue_event(
                new_agent_text_message(f"📂 正在分析目录: {directory_path}")
            )
            
            # 执行分析
            result = await self.analyzer.analyze_directory(directory_path, user_message)
            
            # 发送分析完成消息
            summary = result.get("summary", {})
            summary_text = f"""
📊 **资源分析完成:**
- 📁 目录: {result.get('directory_path', 'N/A')}
- 📄 总文件数: {summary.get('total_files', 0)}
- 🖼️ 图片文件: {summary.get('image_files', 0)}
- 📂 子目录数: {summary.get('total_directories', 0)}
- 💾 总大小: {self._format_file_size(summary.get('total_size', 0))}
- 🎨 需要处理的图片: {len([img for img in result.get('image_analysis', []) if img.get('needs_processing')])}
            """.strip()
            
            await event_queue.enqueue_event(
                new_agent_text_message(summary_text)
            )
            
            # 发送详细结果
            if summary.get("errors"):
                error_text = "⚠️ **分析过程中遇到的问题:**\n" + "\n".join(summary["errors"])
                await event_queue.enqueue_event(
                    new_agent_text_message(error_text)
                )
            
            # 发送JSON结果
            await event_queue.enqueue_event(
                new_agent_text_message(f"📊 分析结果:\n```json\n{json.dumps(result, indent=2, ensure_ascii=False)}\n```")
            )
            
        except Exception as e:
            logger.error(f"❌ 资源分析失败: {e}")
            await event_queue.enqueue_event(
                new_agent_text_message(f"❌ 资源分析失败: {str(e)}")
            )
            
            error_result = {
                "status": "error",
                "error": str(e),
                "task_id": context.task_id
            }
            await event_queue.enqueue_event(
                new_agent_text_message(f"❌ 错误详情:\n```json\n{json.dumps(error_result, indent=2, ensure_ascii=False)}\n```")
            )
    
    def _extract_directory_path(self, message: str) -> Optional[str]:
        """从消息中提取目录路径"""
        import re
        
        # 常见的路径模式
        path_patterns = [
            r'["\']([^"\']+)["\']',  # 引号包围的路径
            r'目录[：:\s]+([^\s]+)',  # "目录: path"
            r'路径[：:\s]+([^\s]+)',  # "路径: path"
            r'分析\s+([^\s]+)',      # "分析 path"
            r'处理\s+([^\s]+)',      # "处理 path"
            r'(/[^\s]+)',           # Unix绝对路径
            r'([A-Za-z]:[^\s]+)',   # Windows路径
            r'(\./[^\s]+)',         # 相对路径
            r'(~/[^\s]+)'           # 用户目录路径
        ]
        
        for pattern in path_patterns:
            matches = re.findall(pattern, message)
            if matches:
                return matches[0].strip()
        
        # 如果没有找到路径，返回None
        return None
    
    def _format_file_size(self, size_bytes: int) -> str:
        """格式化文件大小"""
        if size_bytes == 0:
            return "0 B"
        
        size_names = ["B", "KB", "MB", "GB", "TB"]
        size_bytes = float(size_bytes)
        i = 0
        
        while size_bytes >= 1024.0 and i < len(size_names) - 1:
            size_bytes /= 1024.0
            i += 1
        
        return f"{size_bytes:.1f} {size_names[i]}"
    
    async def cancel(
        self, 
        context: RequestContext, 
        event_queue: EventQueue
    ) -> None:
        """取消资源分析任务"""
        logger.info(f"🛑 取消资源分析任务: {context.task_id}")
        await event_queue.enqueue_event(
            new_agent_text_message("🛑 资源分析任务已取消")
        ) 