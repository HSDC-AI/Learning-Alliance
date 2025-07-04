#!/usr/bin/env python3
"""
A2A资源处理系统完整测试Demo
这个脚本会：
1. 启动所有必要的Agent服务
2. 创建测试图片
3. 运行完整的资源处理工作流
4. 显示结果

使用方法:
python run_demo.py
"""

import asyncio
import subprocess
import time
import signal
import sys
import os
from pathlib import Path
import httpx
from rich.console import Console
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.table import Table

console = Console()

class A2AResourceProcessorDemo:
    """A2A资源处理系统Demo"""
    
    def __init__(self):
        self.base_dir = Path(__file__).parent.parent
        self.test_dir = Path(__file__).parent
        self.agents = {
            "orchestrator": {"port": 8000, "path": "orchestrator", "process": None},
            "resource-analyzer": {"port": 8001, "path": "resource-analyzer", "process": None},
            "image-processor": {"port": 8002, "path": "image-processor", "process": None},
            "resource-replacer": {"port": 8003, "path": "resource-replacer", "process": None},
        }
        self.running_agents = []
        
        # 注册信号处理器，确保优雅关闭
        signal.signal(signal.SIGINT, self.signal_handler)
        signal.signal(signal.SIGTERM, self.signal_handler)
    
    def signal_handler(self, signum, frame):
        """处理中断信号"""
        console.print("\n⏹️ 收到中断信号，正在关闭所有Agent...")
        self.stop_all_agents()
        sys.exit(0)
    
    async def check_agent_health(self, name: str, port: int, timeout: int = 5) -> bool:
        """检查Agent健康状态"""
        try:
            async with httpx.AsyncClient(timeout=timeout) as client:
                response = await client.get(f"http://localhost:{port}/.well-known/agent.json")
                return response.status_code == 200
        except:
            return False
    
    def start_agent(self, name: str, agent_info: dict) -> bool:
        """启动单个Agent"""
        try:
            agent_path = self.base_dir / agent_info["path"]
            cmd = ["uv", "run", "app", "--port", str(agent_info["port"])]
            
            console.print(f"🚀 启动 {name} Agent (端口 {agent_info['port']})")
            
            # 启动进程
            process = subprocess.Popen(
                cmd,
                cwd=agent_path,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            
            agent_info["process"] = process
            self.running_agents.append(name)
            
            return True
            
        except Exception as e:
            console.print(f"❌ 启动 {name} 失败: {e}", style="red")
            return False
    
    def stop_all_agents(self):
        """停止所有Agent"""
        console.print("\n🛑 正在停止所有Agent...")
        
        for name, agent_info in self.agents.items():
            if agent_info["process"]:
                try:
                    agent_info["process"].terminate()
                    agent_info["process"].wait(timeout=5)
                    console.print(f"✅ {name} 已停止")
                except subprocess.TimeoutExpired:
                    agent_info["process"].kill()
                    console.print(f"🔫 强制停止 {name}")
                except Exception as e:
                    console.print(f"⚠️ 停止 {name} 时出错: {e}")
        
        self.running_agents.clear()
    
    async def wait_for_agents_ready(self, timeout: int = 60) -> bool:
        """等待所有Agent启动完成"""
        console.print("⏳ 等待所有Agent启动完成...")
        
        start_time = time.time()
        
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=console,
            transient=True
        ) as progress:
            
            while time.time() - start_time < timeout:
                all_ready = True
                status_text = "检查Agent状态: "
                
                for name, agent_info in self.agents.items():
                    if name in self.running_agents:
                        if await self.check_agent_health(name, agent_info["port"]):
                            status_text += f"✅{name} "
                        else:
                            status_text += f"⏳{name} "
                            all_ready = False
                    else:
                        status_text += f"❌{name} "
                        all_ready = False
                
                task = progress.add_task(status_text, total=None)
                
                if all_ready:
                    console.print("✅ 所有Agent已准备就绪!")
                    return True
                
                await asyncio.sleep(2)
                progress.remove_task(task)
        
        console.print("❌ 等待Agent启动超时", style="red")
        return False
    
    def create_test_images(self) -> bool:
        """创建测试图片"""
        try:
            console.print("🎨 创建测试图片...")
            
            # 运行创建测试图片脚本
            cmd = ["python", "create_test_images.py"]
            result = subprocess.run(
                cmd,
                cwd=self.test_dir,
                capture_output=True,
                text=True
            )
            
            if result.returncode == 0:
                console.print("✅ 测试图片创建成功")
                console.print(result.stdout)
                return True
            else:
                console.print(f"❌ 创建测试图片失败: {result.stderr}", style="red")
                return False
                
        except Exception as e:
            console.print(f"❌ 创建测试图片异常: {e}", style="red")
            return False
    
    async def run_test_workflow(self) -> bool:
        """运行测试工作流"""
        try:
            console.print("🧪 运行A2A资源处理工作流...")
            
            # 构造测试消息
            test_images_path = self.test_dir / "test_images"
            message = f"帮我分析一下 {test_images_path.absolute()} 目录中的所有资源，并替换所有资源图片的主题色为红色"
            
            console.print(f"📝 测试消息: {message}")
            
            # 运行测试客户端
            cmd = ["uv", "run", "python", "test_client.py", "--message", message]
            
            with Progress(
                SpinnerColumn(),
                TextColumn("[progress.description]{task.description}"),
                console=console,
                transient=True
            ) as progress:
                task = progress.add_task("🚀 执行资源处理工作流...", total=None)
                
                result = subprocess.run(
                    cmd,
                    cwd=self.base_dir / "orchestrator",
                    capture_output=True,
                    text=True,
                    timeout=180  # 3分钟超时
                )
                
                progress.update(task, description="✅ 工作流执行完成")
            
            if result.returncode == 0:
                console.print("✅ 工作流执行成功!")
                console.print("\n📋 执行结果:")
                console.print(result.stdout)
                return True
            else:
                console.print(f"❌ 工作流执行失败: {result.stderr}", style="red")
                console.print("标准输出:", result.stdout)
                return False
                
        except subprocess.TimeoutExpired:
            console.print("⏱️ 工作流执行超时", style="yellow")
            return False
        except Exception as e:
            console.print(f"❌ 工作流执行异常: {e}", style="red")
            return False
    
    def show_summary(self):
        """显示Demo总结"""
        table = Table(title="🎯 A2A资源处理系统Demo总结")
        
        table.add_column("组件", style="cyan", no_wrap=True)
        table.add_column("状态", style="magenta")
        table.add_column("端口", style="green")
        table.add_column("功能", style="yellow")
        
        for name, agent_info in self.agents.items():
            status = "✅ 运行中" if name in self.running_agents else "❌ 未运行"
            
            functions = {
                "orchestrator": "工作流编排",
                "resource-analyzer": "资源分析",
                "image-processor": "图像处理", 
                "resource-replacer": "资源替换"
            }
            
            table.add_row(
                name,
                status,
                str(agent_info["port"]),
                functions.get(name, "未知")
            )
        
        console.print(table)
        
        # 显示测试文件信息
        test_images_path = self.test_dir / "test_images"
        if test_images_path.exists():
            console.print(f"\n📁 测试图片目录: {test_images_path.absolute()}")
            
            # 列出图片文件
            image_files = list(test_images_path.rglob("*.png")) + list(test_images_path.rglob("*.jpg"))
            if image_files:
                console.print("🖼️ 测试图片:")
                for img_file in image_files:
                    rel_path = img_file.relative_to(test_images_path)
                    console.print(f"  • {rel_path}")
    
    async def run_demo(self):
        """运行完整Demo"""
        try:
            # 显示欢迎信息
            console.print(Panel(
                "🎭 A2A资源处理系统完整测试Demo\n"
                "本Demo将展示多Agent协作完成资源处理工作流\n"
                "包括：资源分析 → 图像处理 → 资源替换",
                title="欢迎使用",
                style="blue"
            ))
            
            # 步骤1: 创建测试图片
            console.print("\n📝 步骤1: 创建测试数据")
            if not self.create_test_images():
                console.print("❌ 测试数据创建失败，退出Demo", style="red")
                return False
            
            # 步骤2: 启动所有Agent
            console.print("\n🚀 步骤2: 启动所有Agent服务")
            for name, agent_info in self.agents.items():
                if not self.start_agent(name, agent_info):
                    console.print(f"❌ 启动Agent失败，退出Demo", style="red")
                    return False
            
            # 步骤3: 等待Agent准备就绪
            console.print("\n⏳ 步骤3: 等待Agent准备就绪")
            if not await self.wait_for_agents_ready():
                console.print("❌ Agent启动失败，退出Demo", style="red")
                return False
            
            # 步骤4: 运行测试工作流
            console.print("\n🧪 步骤4: 运行资源处理工作流")
            success = await self.run_test_workflow()
            
            # 步骤5: 显示总结
            console.print("\n📊 步骤5: Demo总结")
            self.show_summary()
            
            if success:
                console.print(Panel(
                    "🎉 Demo执行成功!\n"
                    "A2A资源处理系统已完成完整的工作流演示。\n"
                    "你可以检查test_images目录查看处理结果。",
                    title="Demo完成",
                    style="green"
                ))
            else:
                console.print(Panel(
                    "⚠️ Demo部分完成\n"
                    "虽然Agent启动成功，但工作流执行可能遇到问题。\n"
                    "请检查各Agent的日志以排查问题。",
                    title="Demo结果",
                    style="yellow"
                ))
            
            return success
            
        except Exception as e:
            console.print(f"❌ Demo执行异常: {e}", style="red")
            return False
        
        finally:
            # 清理：停止所有Agent
            console.print("\n🧹 清理资源...")
            self.stop_all_agents()
            console.print("✅ Demo清理完成")

def main():
    """主函数"""
    demo = A2AResourceProcessorDemo()
    
    try:
        # 运行Demo
        success = asyncio.run(demo.run_demo())
        
        # 根据结果设置退出码
        exit_code = 0 if success else 1
        sys.exit(exit_code)
        
    except KeyboardInterrupt:
        console.print("\n⏹️ Demo被用户中断")
        demo.stop_all_agents()
        sys.exit(1)
    except Exception as e:
        console.print(f"\n❌ Demo运行失败: {e}", style="red")
        demo.stop_all_agents()
        sys.exit(1)

if __name__ == "__main__":
    main() 