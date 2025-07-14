"""
MonitoringDataAgent - 监控数据获取核心逻辑
"""

import logging
from collections.abc import AsyncIterable
from typing import Any, Dict
import asyncio

logger = logging.getLogger(__name__)


class MonitoringDataAgent:
    """监控数据获取Agent核心逻辑"""

    def __init__(self):
        logger.info("📊 MonitoringDataAgent 初始化完成")

    async def stream(self, start_time: str, end_time: str, task_id: str) -> AsyncIterable[Dict[str, Any]]:
        """获取监控数据的具体实现：返回异步生成器"""
        logger.info(f"🔧 任务ID: {task_id}")
        logger.info(f"🔧 获取监控数据: {start_time} 至 {end_time}")

        # 假装每秒推送一条监控信息
        await asyncio.sleep(0.2)
        yield self.get_agent_response(start_time, end_time)

    def get_agent_response(self, start_time, end_time):
        return {
            "status": "success",
            "content": {
                "start_time": start_time,
                "end_time": end_time,
                "metrics": {
                    "cpu_peak": 80,
                    "memory_usage": 90,
                    "network_traffic": "突增",
                    "disk_io": "正常"
                },
                "alerts": [
                    {"time": f"{start_time.split(' ')[0]} 12:30", "type": "CPU", "value": "85%"},
                    {"time": f"{start_time.split(' ')[0]} 12:45", "type": "Memory", "value": "92%"}
                ]
            }
        }

    SUPPORTED_CONTENT_TYPES = ['text', 'text/plain']