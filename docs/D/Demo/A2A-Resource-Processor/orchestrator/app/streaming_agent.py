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


class StreamingResourceProcessorOrchestrator:
    """流式资源处理编排器 - 在Agent内部使用yield"""
    
    def __init__(self):
        # Agent注册表
        self.agent_registry = {
            "resource_analyzer": os.getenv("RESOURCE_ANALYZER_URL", "http://localhost:8001"),
            "image_processor": os.getenv("IMAGE_PROCESSOR_URL", "http://localhost:8002"),
            "resource_replacer": os.getenv("RESOURCE_REPLACER_URL", "http://localhost:8003")
        }
        
        logger.info("🎭 StreamingResourceProcessorOrchestrator 初始化完成")
    
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
                "step_name": "resource_analysis",
                "message": "📊 步骤1/3: 开始分析资源目录",
                "progress": 10,
                "timestamp": datetime.now().isoformat(),
                "data": {"target_agent": "resource_analyzer"}
            }
            
            # 调用资源分析Agent - 这里也会有子进度
            async for sub_progress in self._call_agent_stream("resource_analyzer", user_message, session_id):
                # 将子Agent的进度转换为整体进度 (10-30%)
                overall_progress = 10 + (sub_progress.get("progress", 0) * 0.2)
                
                yield {
                    "type": "sub_agent_progress",
                    "step_name": "resource_analysis", 
                    "agent_name": "resource_analyzer",
                    "message": f"📊 资源分析: {sub_progress.get('message', '')}",
                    "progress": int(overall_progress),
                    "timestamp": datetime.now().isoformat(),
                    "data": sub_progress.get("data", {})
                }
            
            # 分析完成
            analysis_result = {"files_found": 15, "images": 7, "directories": 2}  # 模拟结果
            
            yield {
                "type": "step_complete",
                "step_name": "resource_analysis",
                "message": "✅ 资源分析完成",
                "progress": 30,
                "timestamp": datetime.now().isoformat(),
                "data": {
                    "analysis_result": analysis_result,
                    "next_step": "image_processing"
                }
            }
            
            # 步骤2: 图像处理 (30-70%)  
            yield {
                "type": "step_start",
                "step_name": "image_processing",
                "message": "🎨 步骤2/3: 开始处理图像文件",
                "progress": 35,
                "timestamp": datetime.now().isoformat(),
                "data": {
                    "target_agent": "image_processor",
                    "images_to_process": analysis_result["images"]
                }
            }
            
            # 图像处理 - 模拟批量处理
            for i in range(analysis_result["images"]):
                await asyncio.sleep(0.5)  # 模拟处理时间
                
                image_progress = 35 + ((i + 1) / analysis_result["images"] * 35)
                
                yield {
                    "type": "batch_progress",
                    "step_name": "image_processing",
                    "message": f"🖼️ 处理图片 {i+1}/{analysis_result['images']}: image_{i+1}.png",
                    "progress": int(image_progress),
                    "timestamp": datetime.now().isoformat(),
                    "data": {
                        "current_image": f"image_{i+1}.png",
                        "completed": i + 1,
                        "total": analysis_result["images"],
                        "batch_completion": (i + 1) / analysis_result["images"] * 100
                    }
                }
            
            processing_result = {"processed_images": analysis_result["images"], "success_rate": 100}
            
            yield {
                "type": "step_complete", 
                "step_name": "image_processing",
                "message": "✅ 图像处理完成",
                "progress": 70,
                "timestamp": datetime.now().isoformat(),
                "data": {
                    "processing_result": processing_result,
                    "next_step": "resource_replacement"
                }
            }
            
            # 步骤3: 资源替换 (70-100%)
            yield {
                "type": "step_start",
                "step_name": "resource_replacement",
                "message": "📁 步骤3/3: 开始替换原始文件",
                "progress": 75,
                "timestamp": datetime.now().isoformat(),
                "data": {
                    "target_agent": "resource_replacer",
                    "files_to_replace": processing_result["processed_images"],
                    "backup_enabled": True
                }
            }
            
            # 资源替换进度
            for i in range(processing_result["processed_images"]):
                await asyncio.sleep(0.3)  # 模拟替换时间
                
                replace_progress = 75 + ((i + 1) / processing_result["processed_images"] * 20)
                
                yield {
                    "type": "file_operation",
                    "step_name": "resource_replacement",
                    "message": f"🔄 替换文件 {i+1}/{processing_result['processed_images']}: 备份并替换",
                    "progress": int(replace_progress),
                    "timestamp": datetime.now().isoformat(),
                    "data": {
                        "file_name": f"image_{i+1}.png",
                        "operation": "backup_and_replace",
                        "backup_path": f"backup/image_{i+1}.png.bak",
                        "completed": i + 1,
                        "total": processing_result["processed_images"]
                    }
                }
            
            replacement_result = {"replaced_files": processing_result["processed_images"], "backups_created": processing_result["processed_images"]}
            
            yield {
                "type": "step_complete",
                "step_name": "resource_replacement", 
                "message": "✅ 资源替换完成",
                "progress": 95,
                "timestamp": datetime.now().isoformat(),
                "data": {
                    "replacement_result": replacement_result
                }
            }
            
            # 工作流完成
            end_time = datetime.now()
            duration = (end_time - start_time).total_seconds()
            
            final_result = {
                "workflow_id": workflow_id,
                "status": "success",
                "duration": duration,
                "analysis_result": analysis_result,
                "processing_result": processing_result,
                "replacement_result": replacement_result,
                "summary": {
                    "total_files_analyzed": analysis_result["files_found"],
                    "images_processed": processing_result["processed_images"],
                    "files_replaced": replacement_result["replaced_files"]
                }
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
        self.processor = StreamingResourceProcessorOrchestrator()
    
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