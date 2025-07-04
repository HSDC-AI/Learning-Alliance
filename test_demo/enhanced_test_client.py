#!/usr/bin/env python3
"""
增强版A2A测试客户端 - 支持流式响应
展示如何在A2A系统中使用yield处理流式响应
"""

import asyncio
import uuid
import logging
import json
from typing import Dict, Any, Optional, AsyncGenerator
from datetime import datetime

import httpx
import click
from rich.console import Console
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn
from rich.live import Live
from rich.table import Table
from rich.json import JSON

# 导入A2A SDK
try:
    from a2a.client import A2ACardResolver, A2AClient
    from a2a.types import MessageSendParams, SendMessageRequest
except ImportError:
    print("❌ A2A SDK未安装，请在orchestrator目录运行：uv sync")
    exit(1)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
console = Console()

class StreamingA2AClient:
    """支持流式响应的A2A客户端"""
    
    def __init__(self, base_url: str = "http://localhost:8000"):
        self.base_url = base_url
        self.session_id = str(uuid.uuid4())
        console.print(f"🔧 流式A2A客户端初始化完成")
        console.print(f"🌐 目标URL: {base_url}")
        console.print(f"🆔 会话ID: {self.session_id}")
    
    async def stream_message_processing(self, message: str) -> AsyncGenerator[Dict[str, Any], None]:
        """
        流式处理A2A消息
        使用yield逐步返回处理状态和响应
        """
        
        # 步骤1: 初始化连接
        yield {
            "stage": "initializing",
            "progress": 0,
            "message": "🔌 正在建立A2A连接...",
            "timestamp": datetime.now().isoformat(),
            "data": {"base_url": self.base_url, "session_id": self.session_id}
        }
        
        try:
            async with httpx.AsyncClient(timeout=120.0) as client:
                
                # 步骤2: 获取Agent卡片
                yield {
                    "stage": "resolving_agent",
                    "progress": 20,
                    "message": "📋 正在获取Agent卡片...",
                    "timestamp": datetime.now().isoformat(),
                    "data": {"action": "get_agent_card"}
                }
                
                resolver = A2ACardResolver(
                    httpx_client=client,
                    base_url=self.base_url
                )
                
                agent_card = await resolver.get_agent_card()
                
                yield {
                    "stage": "agent_resolved", 
                    "progress": 40,
                    "message": f"✅ Agent卡片获取成功: {agent_card.name}",
                    "timestamp": datetime.now().isoformat(),
                    "data": {
                        "agent_name": agent_card.name,
                        "agent_description": agent_card.description,
                        "skills_count": len(agent_card.skills)
                    }
                }
                
                # 步骤3: 创建A2A客户端
                yield {
                    "stage": "creating_client",
                    "progress": 50,
                    "message": "🤝 正在创建A2A客户端...",
                    "timestamp": datetime.now().isoformat(),
                    "data": {"client_type": "A2AClient"}
                }
                
                a2a_client = A2AClient(
                    httpx_client=client,
                    agent_card=agent_card
                )
                
                # 步骤4: 构造请求
                yield {
                    "stage": "preparing_request",
                    "progress": 60,
                    "message": "📝 正在准备消息请求...",
                    "timestamp": datetime.now().isoformat(),
                    "data": {"message_length": len(message)}
                }
                
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
                
                # 步骤5: 发送消息并处理流式响应
                yield {
                    "stage": "sending_message",
                    "progress": 70,
                    "message": "🚀 正在发送消息到Orchestrator...",
                    "timestamp": datetime.now().isoformat(),
                    "data": {"request_id": request.id}
                }
                
                # 这里我们模拟流式响应的处理
                # 在真实的A2A系统中，response可能是流式的
                response = await a2a_client.send_message(request)
                
                # 步骤6: 处理响应
                yield {
                    "stage": "processing_response",
                    "progress": 90,
                    "message": "📨 正在处理Agent响应...",
                    "timestamp": datetime.now().isoformat(),
                    "data": {"response_received": response is not None}
                }
                
                if response:
                    response_dict = response.model_dump()
                    
                    # 解析响应内容
                    response_content = []
                    if 'result' in response_dict and 'parts' in response_dict['result']:
                        for part in response_dict['result']['parts']:
                            if part.get('kind') == 'text':
                                response_content.append({
                                    "type": "text",
                                    "content": part.get('text', '')
                                })
                            elif part.get('kind') == 'application/json':
                                response_content.append({
                                    "type": "json",
                                    "content": part.get('json', {})
                                })
                    
                    # 步骤7: 完成
                    yield {
                        "stage": "completed",
                        "progress": 100,
                        "message": "✅ A2A消息处理完成！",
                        "timestamp": datetime.now().isoformat(),
                        "data": {
                            "response_parts": len(response_content),
                            "response_content": response_content,
                            "full_response": response_dict
                        }
                    }
                else:
                    yield {
                        "stage": "error",
                        "progress": 90,
                        "message": "❌ 未收到Agent响应",
                        "timestamp": datetime.now().isoformat(),
                        "data": {"error": "No response received"}
                    }
                    
        except httpx.ReadTimeout:
            yield {
                "stage": "timeout",
                "progress": 80,
                "message": "⏱️ 请求超时 - 工作流可能仍在后台运行",
                "timestamp": datetime.now().isoformat(),
                "data": {"error_type": "timeout"}
            }
        except Exception as e:
            yield {
                "stage": "error",
                "progress": 0,
                "message": f"❌ 处理失败: {str(e)}",
                "timestamp": datetime.now().isoformat(),
                "data": {"error_type": type(e).__name__, "error_message": str(e)}
            }

    async def simulate_workflow_progress(self) -> AsyncGenerator[Dict[str, Any], None]:
        """
        模拟A2A工作流的进度更新
        展示复杂工作流中的yield使用
        """
        
        workflow_steps = [
            {"name": "资源分析", "duration": 3, "progress_start": 0, "progress_end": 25},
            {"name": "图像处理", "duration": 5, "progress_start": 25, "progress_end": 70},
            {"name": "资源替换", "duration": 2, "progress_start": 70, "progress_end": 100}
        ]
        
        overall_start_time = datetime.now()
        
        for step in workflow_steps:
            step_start_time = datetime.now()
            
            # 步骤开始
            yield {
                "type": "step_start",
                "step_name": step["name"],
                "progress": step["progress_start"],
                "message": f"🚀 开始 {step['name']}...",
                "timestamp": step_start_time.isoformat(),
                "data": {
                    "step_duration_estimate": step["duration"],
                    "overall_elapsed": (step_start_time - overall_start_time).total_seconds()
                }
            }
            
            # 步骤进行中 - 多次yield更新
            step_progress_steps = 5  # 每个步骤分5次更新
            progress_increment = (step["progress_end"] - step["progress_start"]) / step_progress_steps
            
            for i in range(step_progress_steps):
                await asyncio.sleep(step["duration"] / step_progress_steps)
                
                current_progress = step["progress_start"] + (i + 1) * progress_increment
                
                yield {
                    "type": "step_progress",
                    "step_name": step["name"],
                    "progress": int(current_progress),
                    "message": f"⚙️ {step['name']} 进行中... ({i+1}/{step_progress_steps})",
                    "timestamp": datetime.now().isoformat(),
                    "data": {
                        "step_completion": (i + 1) / step_progress_steps * 100,
                        "substep": i + 1,
                        "total_substeps": step_progress_steps
                    }
                }
            
            # 步骤完成
            step_end_time = datetime.now()
            yield {
                "type": "step_complete",
                "step_name": step["name"],
                "progress": step["progress_end"],
                "message": f"✅ {step['name']} 完成",
                "timestamp": step_end_time.isoformat(),
                "data": {
                    "step_duration": (step_end_time - step_start_time).total_seconds(),
                    "overall_elapsed": (step_end_time - overall_start_time).total_seconds()
                }
            }
        
        # 工作流完成
        overall_end_time = datetime.now()
        yield {
            "type": "workflow_complete",
            "step_name": "完成",
            "progress": 100,
            "message": "🎉 整个A2A工作流完成！",
            "timestamp": overall_end_time.isoformat(),
            "data": {
                "total_duration": (overall_end_time - overall_start_time).total_seconds(),
                "completed_steps": len(workflow_steps)
            }
        }

async def demo_streaming_a2a():
    """演示流式A2A处理"""
    
    console.print(Panel(
        "🌊 A2A资源处理系统流式演示\n"
        "展示如何在A2A系统中使用 yield 实现流式响应处理",
        title="流式A2A演示",
        style="blue"
    ))
    
    client = StreamingA2AClient()
    
    # Demo 1: 流式A2A消息处理
    console.print("\n📋 Demo 1: 流式A2A消息处理")
    
    test_message = "帮我分析一下 ./test_images 目录中的所有资源，并替换所有资源图片的主题色为红色"
    
    # 创建进度表
    progress_table = Table(title="A2A消息处理进度")
    progress_table.add_column("阶段", style="cyan")
    progress_table.add_column("进度", style="green")
    progress_table.add_column("状态", style="magenta")
    progress_table.add_column("时间", style="dim")
    
    async for update in client.stream_message_processing(test_message):
        # 添加进度行
        progress_table.add_row(
            update["stage"],
            f"{update['progress']}%",
            update["message"],
            update["timestamp"].split('T')[1][:8]  # 只显示时间部分
        )
        
        # 清屏并显示更新的表格
        console.clear()
        console.print(progress_table)
        
        # 如果有响应数据，显示详细信息
        if update["stage"] == "completed" and "response_content" in update["data"]:
            console.print("\n📨 Agent响应内容:")
            for content in update["data"]["response_content"]:
                if content["type"] == "text":
                    console.print(f"📝 文本: {content['content']}")
                elif content["type"] == "json":
                    console.print("📊 JSON数据:")
                    try:
                        console.print(JSON(content["content"]))
                    except:
                        console.print(str(content["content"]))
        
        await asyncio.sleep(0.1)
    
    console.print("\n" + "="*80)
    
    # Demo 2: 模拟工作流进度
    console.print("\n📋 Demo 2: A2A工作流进度跟踪")
    
    workflow_table = Table(title="A2A工作流执行状态")
    workflow_table.add_column("步骤", style="cyan")
    workflow_table.add_column("类型", style="blue")
    workflow_table.add_column("进度", style="green")
    workflow_table.add_column("状态", style="magenta")
    workflow_table.add_column("耗时", style="yellow")
    
    async for update in client.simulate_workflow_progress():
        elapsed = update["data"].get("step_duration", update["data"].get("overall_elapsed", 0))
        
        workflow_table.add_row(
            update["step_name"],
            update["type"],
            f"{update['progress']}%",
            update["message"],
            f"{elapsed:.1f}s"
        )
        
        console.clear()
        console.print(workflow_table)
        
        # 如果是完成状态，显示总结
        if update["type"] == "workflow_complete":
            console.print(f"\n🎯 工作流总结:")
            console.print(f"• 总耗时: {update['data']['total_duration']:.1f} 秒")
            console.print(f"• 完成步骤: {update['data']['completed_steps']} 个")
            console.print(f"• 最终进度: {update['progress']}%")
        
        await asyncio.sleep(0.1)

    console.print(Panel(
        "✨ 流式A2A Demo完成！\n\n"
        "🎯 在A2A系统中使用 yield 的优势:\n"
        "• 实时反馈 - 用户可以看到每个处理阶段\n"
        "• 错误处理 - 可以在任何阶段捕获和报告错误\n"
        "• 进度跟踪 - 精确显示工作流执行进度\n"
        "• 用户体验 - 避免长时间等待的黑盒操作\n"
        "• 调试友好 - 可以看到每个Agent的响应时间\n"
        "• 资源管理 - 可以在适当时机释放资源",
        title="流式A2A总结",
        style="green"
    ))

@click.command()
@click.option('--url', default='http://localhost:8000', help='Orchestrator Agent URL')
@click.option('--demo-only', is_flag=True, help='只运行流式Demo，不连接真实Agent')
def main(url: str, demo_only: bool):
    """增强版A2A测试客户端 - 支持流式响应"""
    
    if demo_only:
        # 只运行模拟的流式Demo
        asyncio.run(demo_streaming_a2a())
    else:
        # 连接真实的Agent进行测试
        console.print("🔌 连接到真实Agent进行流式测试...")
        # 这里可以添加真实的Agent连接测试
        asyncio.run(demo_streaming_a2a())

if __name__ == "__main__":
    main() 