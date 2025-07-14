# agent.py
import asyncio
import logging
import uuid
import os
import json
from datetime import datetime
from typing import Dict, Any, AsyncGenerator, Optional

import httpx
from a2a.client import A2ACardResolver, A2AClient
from a2a.utils import new_agent_text_message
from a2a.types import MessageSendParams, SendMessageRequest, Part, Message

logger = logging.getLogger(__name__)

PUBLIC_AGENT_CARD_PATH = '/.well-known/agent.json'
EXTENDED_AGENT_CARD_PATH = '/agent/authenticatedExtendedCard'

class CoordinatorAgent:
    """监控突刺分析协调器核心逻辑"""

    def __init__(self):
        # Agent注册表
        self.agent_registry = {
            "data_collector": os.getenv("DATA_COLLECTOR_URL", "http://localhost:10000"),
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

        logger.info("🧠 CoordinatorAgent 初始化完成")
        for name, url in self.agent_registry.items():
            logger.info(f"  📍 {name}: {url}")

    async def process_resources(self, start_time: str, end_time: str, session_id: str) -> Dict[str, Any]:
        """执行完整的资源处理工作流"""
        logger.info(f"🚀 开始执行突刺分析处理工作流: {start_time} - {end_time}")
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
            # 构造结构化查询消息
            query = {
                "start_time": start_time,
                "end_time": end_time
            }
            query_message = json.dumps(query)


            # 步骤1: 监控数据分析
            logger.info("📊 执行步骤1: 监控数据分析")
            self.workflow_state["current_step"] = "analyzing_monitor_data"
            self.workflow_state["progress"] = 100

            analysis_result = await self._call_agent(
                "data_collector",
                query_message,
                session_id
            )

            if not analysis_result or "error" in analysis_result:
                error_msg = analysis_result.get("error", "未知错误") if isinstance(analysis_result, dict) else str(analysis_result)
                raise Exception(f"资源分析失败: {error_msg}")

            self.workflow_state["results"]["analysis"] = analysis_result
            logger.info("✅ 监控数据分析完成")

            return {
                "status": "success",
                "workflow_id": workflow_id,
                "workflow_state": self.workflow_state,
                "summary": self._create_workflow_summary()
            }

        except Exception as e:
            logger.exception(f"❌ 工作流执行失败")
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
        logger.info(f"📞 调用Agent: {agent_name} @ {agent_url}")

        try:
            async with httpx.AsyncClient(timeout=60.0) as client:
                # 获取Agent卡片
                resolver = A2ACardResolver(
                    httpx_client=client,
                    base_url=agent_url
                )

                # 先尝试获取公共卡片
                try:
                    agent_card = await resolver.get_agent_card()
                    logger.info(f"✅ 获取到{agent_name}的公共Agent卡片")
                except Exception as e:
                    logger.error(f"❌ 获取公共AgentCard失败 {agent_name}: {e}")
                    return {"error": f"Agent {agent_name} 不可用: {e}"}

                # 如果支持扩展卡片，尝试获取
                if agent_card.supportsAuthenticatedExtendedCard:
                    try:
                        auth_headers_dict = {'Authorization': 'Bearer dummy-token-for-extended-card'}
                        extended_card = await resolver.get_agent_card(
                            relative_card_path=EXTENDED_AGENT_CARD_PATH,
                            http_kwargs={'headers': auth_headers_dict}
                        )
                        agent_card = extended_card
                        logger.info(f"✅ 获取到{agent_name}的扩展Agent卡片")
                    except Exception as e:
                        logger.warning(f"⚠️ 获取扩展AgentCard失败，使用公共卡片: {e}")

                # 创建A2A客户端
                a2a_client = A2AClient(
                    httpx_client=client,
                    agent_card=agent_card
                )

                # 创建结构化消息
                message_parts = [Part(kind="text", text=message)]
                agent_message = Message(role="user", parts=message_parts, messageId=str(uuid.uuid4()))

                # 发送消息
                send_params = MessageSendParams(
                    message=agent_message,
                    session_id=session_id
                )

                send_request = SendMessageRequest(
                    id=session_id,
                    params=send_params
                )

                # 发送请求并获取响应
                response = await a2a_client.send_message(send_request)
                # 处理响应
                response_text = ""
                for part in response.model_dump(mode='json', exclude_none=False)["result"].get("artifacts", []):
                    for info in part.get('parts'):
                        if info.get('kind') == "text":
                            response_text += json.dumps(info.get('text'))
                        elif info.get('kind') == "json":
                            try:
                                # 尝试解析JSON响应
                                return json.loads(info.get('text'))
                            except:
                                response_text += str(info.json)

                logger.info(f"📨 Agent {agent_name} 响应: {response_text[:200]}{'...' if len(response_text) > 200 else ''}")

                # 尝试解析整个响应为JSON
                try:
                    return json.loads(response_text)
                except:
                    return {"response": response_text}

        except Exception as e:
            logger.exception(f"❌ 调用Agent失败 {agent_name}")
            return {"error": f"调用失败: {str(e)}"}

    def _create_workflow_summary(self) -> Dict[str, Any]:
        """创建工作流总结"""
        return {
            "workflow_id": self.workflow_state.get("workflow_id"),
            "status": self.workflow_state.get("current_step"),
            "progress": self.workflow_state.get("progress"),
            "start_time": self.workflow_state.get("start_time"),
            "end_time": self.workflow_state.get("end_time"),
            "results": self.workflow_state.get("results"),
            "error": self.workflow_state.get("error")
        }