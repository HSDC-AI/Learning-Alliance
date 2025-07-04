"""
Orchestrator Core - 资源处理编排器核心逻辑
"""

import asyncio
import logging
import uuid
from typing import Dict, Any, Optional
from datetime import datetime
import os

import httpx
from a2a.client import A2ACardResolver, A2AClient
from a2a.utils import new_agent_text_message, new_data_artifact
from a2a.types import MessageSendParams, SendMessageRequest

logger = logging.getLogger(__name__)


class ResourceProcessorOrchestrator:
    """资源处理编排器核心逻辑"""
    
    def __init__(self):
        # Agent注册表 - 可通过环境变量配置
        self.agent_registry = {
            "resource_analyzer": os.getenv("RESOURCE_ANALYZER_URL", "http://localhost:8001"),
            "image_processor": os.getenv("IMAGE_PROCESSOR_URL", "http://localhost:8002"),
            "resource_replacer": os.getenv("RESOURCE_REPLACER_URL", "http://localhost:8003")
        }
        
        # 工作流状态
        self.workflow_state = {
            "current_step": "idle",
            "progress": 0,
            "start_time": None,
            "end_time": None,
            "error": None,
            "results": {}
        }
        
        logger.info("🎭 ResourceProcessorOrchestrator 初始化完成")
        for name, url in self.agent_registry.items():
            logger.info(f"  📍 {name}: {url}")
    
    async def process_resources(self, user_message: str, session_id: str) -> Dict[str, Any]:
        """执行完整的资源处理工作流"""
        logger.info(f"🚀 开始执行资源处理工作流: {user_message}")
        
        workflow_id = str(uuid.uuid4())
        self.workflow_state.update({
            "workflow_id": workflow_id,
            "current_step": "started",
            "progress": 0,
            "start_time": datetime.now().isoformat(),
            "end_time": None,
            "error": None,
            "results": {}
        })
        
        try:
            # 步骤1: 资源分析 (25% 进度)
            logger.info("📊 执行步骤1: 资源分析")
            self.workflow_state["current_step"] = "analyzing_resources"
            self.workflow_state["progress"] = 25
            
            analysis_result = await self._call_agent(
                "resource_analyzer",
                user_message,
                session_id
            )
            
            if not analysis_result or "error" in str(analysis_result):
                raise Exception(f"资源分析失败: {analysis_result}")
            
            self.workflow_state["results"]["analysis"] = analysis_result
            
            # 步骤2: 图片处理 (50% 进度)
            logger.info("🎨 执行步骤2: 图片处理")
            self.workflow_state["current_step"] = "processing_images"
            self.workflow_state["progress"] = 50
            
            # 构造图片处理任务
            image_processing_task = self._create_image_processing_task(
                analysis_result, user_message
            )
            
            processing_result = await self._call_agent(
                "image_processor",
                image_processing_task,
                session_id
            )
            
            if not processing_result or "error" in str(processing_result):
                raise Exception(f"图片处理失败: {processing_result}")
            
            self.workflow_state["results"]["processing"] = processing_result
            
            # 步骤3: 资源替换 (75% 进度)
            logger.info("📁 执行步骤3: 资源替换")
            self.workflow_state["current_step"] = "replacing_resources"
            self.workflow_state["progress"] = 75
            
            # 构造资源替换任务
            replacement_task = self._create_replacement_task(
                analysis_result, processing_result
            )
            
            replacement_result = await self._call_agent(
                "resource_replacer",
                replacement_task,
                session_id
            )
            
            if not replacement_result or "error" in str(replacement_result):
                raise Exception(f"资源替换失败: {replacement_result}")
            
            self.workflow_state["results"]["replacement"] = replacement_result
            
            # 完成 (100% 进度)
            self.workflow_state.update({
                "current_step": "completed",
                "progress": 100,
                "end_time": datetime.now().isoformat()
            })
            
            logger.info("✅ 资源处理工作流完成")
            
            return {
                "status": "success",
                "workflow_id": workflow_id,
                "workflow_state": self.workflow_state,
                "summary": self._create_workflow_summary()
            }
            
        except Exception as e:
            logger.error(f"❌ 工作流执行失败: {e}")
            self.workflow_state.update({
                "current_step": "failed",
                "end_time": datetime.now().isoformat(),
                "error": str(e)
            })
            
            return {
                "status": "failed",
                "workflow_id": workflow_id,
                "error": str(e),
                "workflow_state": self.workflow_state
            }
    
    async def _call_agent(self, agent_name: str, message: str, session_id: str) -> Optional[Dict[str, Any]]:
        """调用指定的Agent"""
        if agent_name not in self.agent_registry:
            logger.error(f"❌ Agent未注册: {agent_name}")
            return {"error": f"Agent未注册: {agent_name}"}
        
        agent_url = self.agent_registry[agent_name]
        
        try:
            logger.info(f"📞 调用Agent: {agent_name} @ {agent_url}")
            
            async with httpx.AsyncClient(timeout=60.0) as client:
                # 获取Agent卡片
                resolver = A2ACardResolver(
                    httpx_client=client,
                    base_url=agent_url
                )
                
                try:
                    agent_card = await resolver.get_agent_card()
                except Exception as e:
                    logger.error(f"❌ 获取AgentCard失败 {agent_name}: {e}")
                    return {"error": f"Agent {agent_name} 不可用: {e}"}
                
                # 创建A2A客户端
                a2a_client = A2AClient(
                    httpx_client=client,
                    agent_card=agent_card
                )
                
                # 发送消息
                send_params = MessageSendParams(
                    message=new_agent_text_message(message),
                    session_id=session_id
                )
                
                send_request = SendMessageRequest(params=send_params)
                
                response_content = []
                async for chunk in a2a_client.send_message_stream(send_request):
                    if chunk.parts:
                        for part in chunk.parts:
                            if hasattr(part, 'text'):
                                response_content.append(part.text)
                            elif hasattr(part, 'json'):
                                response_content.append(str(part.json))
                
                response_text = " ".join(response_content)
                logger.info(f"📨 Agent {agent_name} 响应: {response_text[:200]}...")
                
                # 尝试解析JSON响应
                try:
                    import json
                    return json.loads(response_text)
                except:
                    return {"response": response_text}
                
        except Exception as e:
            logger.error(f"❌ 调用Agent失败 {agent_name}: {e}")
            return {"error": f"调用失败: {str(e)}"}
    
    def _create_image_processing_task(self, analysis_result: Dict[str, Any], original_message: str) -> str:
        """创建图片处理任务描述"""
        return f"根据分析结果，将所有图片的主题色替换为红色。原始请求: {original_message}"
    
    def _create_replacement_task(self, analysis_result: Dict[str, Any], processing_result: Dict[str, Any]) -> str:
        """创建资源替换任务描述"""
        return f"将处理完成的图片替换回原始位置，请先备份原始文件。"
    
    def _create_workflow_summary(self) -> Dict[str, Any]:
        """创建工作流总结"""
        results = self.workflow_state.get("results", {})
        
        summary = {
            "workflow_id": self.workflow_state.get("workflow_id"),
            "status": self.workflow_state.get("current_step"),
            "progress": self.workflow_state.get("progress"),
            "start_time": self.workflow_state.get("start_time"),
            "end_time": self.workflow_state.get("end_time"),
            "total_files_analyzed": 0,
            "images_processed": 0,
            "files_replaced": 0,
            "errors": []
        }
        
        # 从分析结果中提取统计信息
        if "analysis" in results:
            analysis = results["analysis"]
            if isinstance(analysis, dict) and "summary" in analysis:
                summary["total_files_analyzed"] = analysis["summary"].get("total_files", 0)
        
        # 从处理结果中提取统计信息
        if "processing" in results:
            processing = results["processing"]
            if isinstance(processing, dict) and "summary" in processing:
                summary["images_processed"] = processing["summary"].get("processed_images", 0)
        
        # 从替换结果中提取统计信息
        if "replacement" in results:
            replacement = results["replacement"]
            if isinstance(replacement, dict) and "summary" in replacement:
                summary["files_replaced"] = replacement["summary"].get("replaced_files", 0)
        
        return summary 