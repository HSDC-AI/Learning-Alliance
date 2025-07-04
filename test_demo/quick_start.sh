#!/bin/bash

# A2A资源处理系统 - 快速启动脚本
# 使用方法: ./quick_start.sh

echo "🎭 A2A资源处理系统快速启动"
echo "================================"

# 检查Python是否可用
if ! command -v python3 &> /dev/null; then
    echo "❌ Python3 未找到，请先安装Python 3.10+"
    exit 1
fi

# 检查UV是否可用
if ! command -v uv &> /dev/null; then
    echo "❌ UV 未找到，请先安装UV包管理器"
    echo "   安装命令: curl -LsSf https://astral.sh/uv/install.sh | sh"
    exit 1
fi

# 检查Pillow依赖
echo "🔍 检查依赖..."
python3 -c "import PIL" 2>/dev/null
if [ $? -ne 0 ]; then
    echo "📦 安装Pillow..."
    pip install Pillow
fi

python3 -c "import httpx" 2>/dev/null  
if [ $? -ne 0 ]; then
    echo "📦 安装httpx..."
    pip install httpx
fi

python3 -c "import rich" 2>/dev/null
if [ $? -ne 0 ]; then
    echo "📦 安装rich..."
    pip install rich
fi

echo "✅ 依赖检查完成"

# 运行Demo
echo "🚀 启动A2A资源处理系统Demo..."
echo ""

python3 run_demo.py

echo ""
echo "🎯 Demo完成！"
echo "💡 查看 test_images 目录了解处理结果"
echo "�� 详细说明请参阅 README.md" 