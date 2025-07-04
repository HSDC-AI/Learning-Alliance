#!/usr/bin/env python3
"""
A2A资源处理系统流式Demo - 使用yield实现实时进度反馈
展示如何使用生成器函数提供流式响应和实时状态更新
"""

import asyncio
import time
import json
from typing import AsyncGenerator, Dict, Any
from rich.console import Console
from rich.panel import Panel
from rich.progress import Progress, BarColumn, TextColumn, TimeElapsedColumn
from rich.live import Live
from rich.table import Table

console = Console()

class StreamingWorkflowProcessor:
    """流式工作流处理器 - 演示yield的使用"""
    
    def __init__(self):
        self.current_step = ""
        self.total_steps = 0
        self.completed_steps = 0
        
    async def process_resources_stream(self, directory: str) -> AsyncGenerator[Dict[str, Any], None]:
        """
        流式处理资源的生成器函数
        使用 yield 逐步返回处理状态和结果
        """
        
        # 初始化
        yield {
            "status": "started",
            "step": "初始化",
            "progress": 0,
            "message": f"🚀 开始处理目录: {directory}",
            "data": {"directory": directory, "start_time": time.time()}
        }
        
        await asyncio.sleep(1)  # 模拟处理时间
        
        # 步骤1: 资源分析
        yield {
            "status": "analyzing", 
            "step": "资源分析",
            "progress": 25,
            "message": "📊 正在分析目录结构和文件类型...",
            "data": {"current_action": "directory_scan"}
        }
        
        # 模拟分析过程中的多个子步骤
        scan_results = []
        for i, file_type in enumerate(["图片文件", "文本文件", "子目录"]):
            await asyncio.sleep(0.5)
            scan_results.append(f"发现 {5+i*2} 个{file_type}")
            yield {
                "status": "analyzing",
                "step": "资源分析", 
                "progress": 25 + i*5,
                "message": f"📁 扫描{file_type}...",
                "data": {
                    "current_action": "file_scan",
                    "file_type": file_type,
                    "partial_results": scan_results.copy()
                }
            }
        
        # 分析完成
        analysis_result = {
            "total_files": 15,
            "image_files": 7,
            "text_files": 3,
            "subdirectories": 2,
            "scan_details": scan_results
        }
        
        yield {
            "status": "analysis_complete",
            "step": "资源分析",
            "progress": 40, 
            "message": "✅ 资源分析完成",
            "data": {
                "analysis_result": analysis_result,
                "next_step": "图像处理"
            }
        }
        
        await asyncio.sleep(1)
        
        # 步骤2: 图像处理 - 展示批量处理中的yield使用
        yield {
            "status": "processing_images",
            "step": "图像处理", 
            "progress": 50,
            "message": "🎨 开始处理图像文件...",
            "data": {"total_images": analysis_result["image_files"]}
        }
        
        processed_images = []
        for i in range(analysis_result["image_files"]):
            await asyncio.sleep(0.8)  # 模拟图像处理时间
            
            image_name = f"image_{i+1}.png"
            processed_images.append({
                "name": image_name,
                "original_color": ["blue", "green", "yellow", "purple", "orange", "cyan", "magenta"][i],
                "new_color": "red",
                "processed_at": time.time()
            })
            
            # 每处理一张图片就yield一次状态
            yield {
                "status": "processing_images",
                "step": "图像处理",
                "progress": 50 + int((i+1) / analysis_result["image_files"] * 25),
                "message": f"🖼️ 处理图片 {i+1}/{analysis_result['image_files']}: {image_name}",
                "data": {
                    "current_image": image_name,
                    "processed_count": i+1,
                    "total_count": analysis_result["image_files"],
                    "processed_images": processed_images.copy()
                }
            }
        
        # 图像处理完成 
        yield {
            "status": "images_complete",
            "step": "图像处理",
            "progress": 75,
            "message": "✅ 所有图像处理完成",
            "data": {
                "processed_images": processed_images,
                "total_processed": len(processed_images),
                "next_step": "资源替换"
            }
        }
        
        await asyncio.sleep(1)
        
        # 步骤3: 资源替换
        yield {
            "status": "replacing_resources",
            "step": "资源替换",
            "progress": 80,
            "message": "📁 开始替换原始文件...",
            "data": {"backup_enabled": True}
        }
        
        # 模拟文件替换过程
        replaced_files = []
        for i, img_data in enumerate(processed_images):
            await asyncio.sleep(0.6)
            
            backup_path = f"backup/{img_data['name']}.bak"
            replaced_files.append({
                "original": img_data['name'],
                "backup": backup_path,
                "replaced_at": time.time()
            })
            
            yield {
                "status": "replacing_resources", 
                "step": "资源替换",
                "progress": 80 + int((i+1) / len(processed_images) * 15),
                "message": f"🔄 替换文件 {i+1}/{len(processed_images)}: {img_data['name']}",
                "data": {
                    "current_file": img_data['name'],
                    "backup_path": backup_path,
                    "replaced_count": i+1,
                    "replaced_files": replaced_files.copy()
                }
            }
        
        # 最终完成
        final_result = {
            "status": "success",
            "total_files_analyzed": analysis_result["total_files"],
            "images_processed": len(processed_images),
            "files_replaced": len(replaced_files),
            "processing_time": time.time() - time.time(),  # 简化的时间计算
            "analysis_result": analysis_result,
            "processed_images": processed_images,
            "replaced_files": replaced_files
        }
        
        yield {
            "status": "completed",
            "step": "完成",
            "progress": 100,
            "message": "🎉 资源处理工作流完成！",
            "data": final_result
        }

    async def simulate_agent_communication_stream(self) -> AsyncGenerator[Dict[str, Any], None]:
        """
        模拟Agent间通信的流式过程
        展示如何用yield来处理Agent协调
        """
        
        agents = [
            {"name": "Orchestrator", "role": "编排器", "port": 8000},
            {"name": "ResourceAnalyzer", "role": "资源分析器", "port": 8001}, 
            {"name": "ImageProcessor", "role": "图像处理器", "port": 8002},
            {"name": "ResourceReplacer", "role": "资源替换器", "port": 8003}
        ]
        
        # 启动Agent
        for i, agent in enumerate(agents):
            yield {
                "type": "agent_status",
                "agent": agent["name"],
                "status": "starting",
                "message": f"🚀 启动 {agent['role']} (端口 {agent['port']})",
                "data": agent
            }
            await asyncio.sleep(0.5)
            
            yield {
                "type": "agent_status", 
                "agent": agent["name"],
                "status": "ready",
                "message": f"✅ {agent['role']} 已就绪",
                "data": agent
            }
        
        # Agent间通信
        communications = [
            {"from": "Orchestrator", "to": "ResourceAnalyzer", "action": "分析请求"},
            {"from": "ResourceAnalyzer", "to": "Orchestrator", "action": "分析结果"},
            {"from": "Orchestrator", "to": "ImageProcessor", "action": "处理请求"},
            {"from": "ImageProcessor", "to": "Orchestrator", "action": "处理结果"},
            {"from": "Orchestrator", "to": "ResourceReplacer", "action": "替换请求"},
            {"from": "ResourceReplacer", "to": "Orchestrator", "action": "替换结果"}
        ]
        
        for comm in communications:
            yield {
                "type": "agent_communication",
                "from_agent": comm["from"],
                "to_agent": comm["to"], 
                "action": comm["action"],
                "message": f"📡 {comm['from']} → {comm['to']}: {comm['action']}",
                "data": comm
            }
            await asyncio.sleep(1)

async def run_streaming_demo():
    """运行流式Demo"""
    
    console.print(Panel(
        "🌊 A2A资源处理系统流式Demo\n"
        "展示如何使用 yield 实现实时进度反馈和状态更新",
        title="流式处理演示",
        style="blue"
    ))
    
    processor = StreamingWorkflowProcessor()
    
    # Demo 1: 流式资源处理
    console.print("\n📋 Demo 1: 流式资源处理工作流")
    
    # 创建进度表格
    progress_table = Table(title="工作流进度")
    progress_table.add_column("步骤", style="cyan")
    progress_table.add_column("状态", style="magenta")
    progress_table.add_column("进度", style="green")
    progress_table.add_column("消息", style="yellow")
    
    async for update in processor.process_resources_stream("./test_images"):
        # 实时更新进度表格
        progress_table.add_row(
            update["step"],
            update["status"],
            f"{update['progress']}%",
            update["message"]
        )
        
        console.clear()
        console.print(progress_table)
        
        # 显示详细数据（如果有）
        if "data" in update and update["status"] in ["analysis_complete", "images_complete", "completed"]:
            console.print(f"\n📊 详细数据:")
            console.print(json.dumps(update["data"], indent=2, ensure_ascii=False))
        
        await asyncio.sleep(0.1)  # 短暂延迟以便观察
    
    console.print("\n" + "="*60)
    
    # Demo 2: Agent通信流
    console.print("\n📋 Demo 2: Agent间通信流")
    
    agent_status_table = Table(title="Agent通信状态")
    agent_status_table.add_column("时间", style="dim")
    agent_status_table.add_column("类型", style="cyan") 
    agent_status_table.add_column("发送方", style="green")
    agent_status_table.add_column("接收方", style="blue")
    agent_status_table.add_column("动作", style="magenta")
    
    async for comm_update in processor.simulate_agent_communication_stream():
        timestamp = time.strftime("%H:%M:%S")
        
        if comm_update["type"] == "agent_status":
            agent_status_table.add_row(
                timestamp,
                "状态",
                comm_update["agent"],
                "-",
                comm_update["status"]
            )
        else:
            agent_status_table.add_row(
                timestamp,
                "通信",
                comm_update["from_agent"],
                comm_update["to_agent"],
                comm_update["action"]
            )
        
        console.clear()
        console.print(agent_status_table)
        console.print(f"\n💬 {comm_update['message']}")
        
        await asyncio.sleep(0.1)

    console.print(Panel(
        "✨ 流式Demo完成！\n\n"
        "🎯 yield 的主要用途:\n"
        "• 实时进度反馈 - 让用户看到处理过程\n"
        "• 流式响应 - 避免长时间等待\n"
        "• 状态管理 - 精确控制每个处理步骤\n"
        "• 内存效率 - 避免一次性加载大量数据\n"
        "• 用户体验 - 提供即时反馈和状态更新",
        title="Demo总结",
        style="green"
    ))

if __name__ == "__main__":
    asyncio.run(run_streaming_demo()) 