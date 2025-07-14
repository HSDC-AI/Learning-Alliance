"""
监控突刺分析系统主程序
"""

import asyncio
from coordinator.agent import CoordinatorAgent


async def main():
    # 设置分析时间范围
    start_time = "2025-06-30 12:00"
    end_time = "2025-06-30 13:00"

    # 创建协调Agent
    coordinator = CoordinatorAgent()

    # 运行分析
    print("🚀 开始监控突刺分析流程")
    report_path = await coordinator.run_analysis(start_time, end_time)

    # 处理结果
    if report_path:
        print(f"\n✅ 分析完成！报告已生成: {report_path}")
        try:
            print("\n📄 报告内容预览:")
            with open(report_path, 'r', encoding='utf-8') as f:
                print(f.read()[:500] + "...")  # 只打印前500个字符
        except Exception as e:
            print(f"\n⚠️ 无法读取报告文件: {str(e)}")
    else:
        print("\n❌ 报告生成失败")


if __name__ == "__main__":
    asyncio.run(main())