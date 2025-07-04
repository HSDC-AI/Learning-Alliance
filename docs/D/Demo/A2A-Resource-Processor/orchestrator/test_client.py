#!/usr/bin/env python3
"""
Orchestrator Agent 测试客户端
用于测试编排器Agent的功能

使用方法:
python test_client.py --message "帮我分析一下 ./test_images 目录中的所有资源，并替换所有资源图片的主题色为红色"
"""

import asyncio
import uuid
import logging
import json
from typing import Dict, Any, Optional

import httpx
import click
from rich.console import Console
from rich.text import Text
from rich.panel import Panel
from rich.spinner import Spinner
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.json import JSON

from a2a.client import A2ACardResolver, A2AClient
from a2a.types import MessageSendParams, SendMessageRequest

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

console = Console()

class OrchestratorTestClient:
    """编排器Agent测试客户端"""
    
    def __init__(self, base_url: str = "http://localhost:8000"):
        self.base_url = base_url
        self.session_id = str(uuid.uuid4())
        console.print(f"🔧 测试客户端初始化完成")
        console.print(f"🌐 目标URL: {base_url}")
        console.print(f"🆔 会话ID: {self.session_id}")
    
    async def test_agent_card(self) -> Optional[Dict[str, Any]]:
        """测试获取Agent卡片"""
        console.print("\n📋 测试1: 获取Agent卡片")
        
        try:
            async with httpx.AsyncClient(timeout=10.0) as client:
                resolver = A2ACardResolver(
                    httpx_client=client,
                    base_url=self.base_url
                )
                
                agent_card = await resolver.get_agent_card()
                
                # 显示Agent卡片信息
                console.print(Panel(
                    f"✅ Agent卡片获取成功\n"
                    f"📛 名称: {agent_card.name}\n"
                    f"📝 描述: {agent_card.description}\n"
                    f"🔗 URL: {agent_card.url}\n"
                    f"🎯 版本: {agent_card.version}\n"
                    f"⚡ 技能数量: {len(agent_card.skills)}",
                    title="Agent Information",
                    style="green"
                ))
                
                if agent_card.skills:
                    console.print("\n🛠️ 可用技能:")
                    for skill in agent_card.skills:
                        console.print(f"  • {skill.name}: {skill.description}")
                        if skill.examples:
                            console.print("    示例:")
                            for example in skill.examples[:2]:  # 显示前2个示例
                                console.print(f"      - {example}")
                
                return agent_card.model_dump()
                
        except Exception as e:
            console.print(f"❌ 获取Agent卡片失败: {e}", style="red")
            return None
    
    async def test_send_message(self, message: str) -> Optional[Dict[str, Any]]:
        """测试发送消息"""
        console.print(f"\n📨 测试2: 发送消息")
        console.print(f"📝 消息内容: {message}")
        
        try:
            async with httpx.AsyncClient(timeout=120.0) as client:
                # 获取Agent卡片
                resolver = A2ACardResolver(
                    httpx_client=client,
                    base_url=self.base_url
                )
                
                agent_card = await resolver.get_agent_card()
                
                # 创建A2A客户端
                a2a_client = A2AClient(
                    httpx_client=client,
                    agent_card=agent_card
                )
                
                # 创建发送消息请求
                request = SendMessageRequest(
                    id=str(uuid.uuid4()),
                    params=MessageSendParams(
                        message={
                            'role': 'user',
                            'parts': [{'kind': 'text', 'text': message}],
                            'messageId': str(uuid.uuid4()),
                        },
                        sessionId=self.session_id
                    )
                )
                
                # 发送消息并显示进度
                with Progress(
                    SpinnerColumn(),
                    TextColumn("[progress.description]{task.description}"),
                    console=console,
                    transient=True
                ) as progress:
                    task = progress.add_task("🚀 发送消息到编排器...", total=None)
                    
                    response = await a2a_client.send_message(request)
                    
                    progress.update(task, description="✅ 消息发送完成")
                
                # 处理响应
                if response:
                    console.print(Panel(
                        "✅ 消息发送成功!",
                        title="Success",
                        style="green"
                    ))
                    
                    # 显示响应内容
                    response_dict = response.model_dump()
                    if 'result' in response_dict:
                        result = response_dict['result']
                        if 'parts' in result:
                            console.print("\n📋 响应内容:")
                            for part in result['parts']:
                                if part.get('kind') == 'text':
                                    console.print(part.get('text', ''))
                                elif part.get('kind') == 'application/json':
                                    console.print("\n📊 JSON数据:")
                                    json_data = part.get('json', {})
                                    try:
                                        # 确保json_data可以被JSON序列化
                                        if isinstance(json_data, str):
                                            json_data = json.loads(json_data)
                                        serializable_data = json.loads(json.dumps(json_data, default=str, ensure_ascii=False))
                                        console.print(JSON(serializable_data))
                                    except Exception as e:
                                        console.print(f"⚠️ JSON显示失败，使用文本格式: {e}")
                                        console.print(str(json_data))
                    
                    return response_dict
                else:
                    console.print("❌ 未收到响应", style="red")
                    return None
                    
        except httpx.ReadTimeout:
            console.print("⏱️ 请求超时 - 工作流可能仍在后台运行", style="yellow")
            return None
        except Exception as e:
            console.print(f"❌ 发送消息失败: {e}", style="red")
            return None
    
    async def test_health_check(self) -> bool:
        """测试健康检查"""
        console.print("\n🏥 健康检查")
        
        try:
            async with httpx.AsyncClient(timeout=5.0) as client:
                # 尝试获取Agent卡片作为健康检查
                response = await client.get(f"{self.base_url}/.well-known/agent.json")
                
                if response.status_code == 200:
                    console.print("✅ 编排器Agent运行正常", style="green")
                    return True
                else:
                    console.print(f"❌ 健康检查失败: HTTP {response.status_code}", style="red")
                    return False
                    
        except Exception as e:
            console.print(f"❌ 健康检查失败: {e}", style="red")
            return False
    
    async def run_full_test(self, message: str) -> Dict[str, Any]:
        """运行完整测试套件"""
        console.print("🧪 开始运行编排器Agent完整测试")
        
        results = {
            "health_check": False,
            "agent_card": None,
            "message_response": None,
            "overall_success": False
        }
        
        # 1. 健康检查
        results["health_check"] = await self.test_health_check()
        
        if not results["health_check"]:
            console.print("❌ 健康检查失败，跳过后续测试", style="red")
            return results
        
        # 2. 获取Agent卡片
        results["agent_card"] = await self.test_agent_card()
        
        if not results["agent_card"]:
            console.print("❌ 获取Agent卡片失败，跳过消息测试", style="red")
            return results
        
        # 3. 发送消息测试
        results["message_response"] = await self.test_send_message(message)
        
        # 评估整体成功
        results["overall_success"] = (
            results["health_check"] and 
            results["agent_card"] is not None and 
            results["message_response"] is not None
        )
        
        # 显示最终结果
        if results["overall_success"]:
            console.print(Panel(
                "🎉 所有测试通过!\n"
                "编排器Agent运行正常，可以处理资源处理工作流。",
                title="Test Summary",
                style="green"
            ))
        else:
            console.print(Panel(
                "⚠️ 部分测试失败\n"
                "请检查编排器Agent的运行状态和配置。",
                title="Test Summary",
                style="yellow"
            ))
        
        return results

@click.command()
@click.option('--url', default='http://localhost:8000', help='编排器Agent URL')
@click.option('--message', default='帮我分析一下 ./test_images 目录中的所有资源，并替换所有资源图片的主题色为红色', help='测试消息')
@click.option('--health-only', is_flag=True, help='只执行健康检查')
def main(url: str, message: str, health_only: bool):
    """编排器Agent测试客户端"""
    
    async def run_test():
        # 显示欢迎信息
        console.print(Panel(
            "🎭 Orchestrator Agent 测试客户端\n"
            "用于测试A2A资源处理编排器的功能",
            title="Welcome",
            style="blue"
        ))
        
        # 创建测试客户端
        test_client = OrchestratorTestClient(url)
        
        if health_only:
            # 只执行健康检查
            await test_client.test_health_check()
        else:
            # 运行完整测试
            results = await test_client.run_full_test(message)
            
            # 显示详细结果
            console.print("\n📊 详细测试结果:")
            try:
                # 确保results可以被JSON序列化
                json_results = json.loads(json.dumps(results, default=str, ensure_ascii=False))
                console.print(JSON(json_results))
            except Exception as e:
                console.print(f"⚠️ JSON显示失败，使用文本格式: {e}")
                console.print(str(results))
    
    # 运行异步测试
    try:
        asyncio.run(run_test())
    except KeyboardInterrupt:
        console.print("\n⏹️ 测试被用户中断", style="yellow")
    except Exception as e:
        console.print(f"\n❌ 测试运行错误: {e}", style="red")

if __name__ == "__main__":
    main() 