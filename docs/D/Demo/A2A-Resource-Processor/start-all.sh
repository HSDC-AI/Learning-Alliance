#!/bin/bash

# A2A Resource Processor - 启动所有Agent脚本
# 使用方法: ./start-all.sh

echo "🚀 启动A2A资源处理系统 - 4个独立Agent"
echo "================================================"

# 检查uv是否安装
if ! command -v uv &> /dev/null; then
    echo "❌ 错误: uv未安装。请先安装uv: curl -LsSf https://astral.sh/uv/install.sh | sh"
    exit 1
fi

# 定义颜色
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[0;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# 检查端口是否被占用
check_port() {
    local port=$1
    local name=$2
    if lsof -Pi :$port -sTCP:LISTEN -t >/dev/null ; then
        echo -e "${RED}❌ 端口 $port 已被占用，无法启动 $name${NC}"
        return 1
    fi
    return 0
}

# 启动单个Agent
start_agent() {
    local dir=$1
    local port=$2
    local name=$3
    local color=$4
    
    echo -e "${color}📍 启动 $name (端口:$port)${NC}"
    
    # 检查端口
    if ! check_port $port "$name"; then
        return 1
    fi
    
    # 检查目录是否存在
    if [ ! -d "$dir" ]; then
        echo -e "${RED}❌ 目录不存在: $dir${NC}"
        return 1
    fi
    
    # 启动Agent
    cd "$dir"
    echo "   💻 在目录: $(pwd)"
    echo "   🔧 执行: uv run app --port $port"
    
    # 在后台启动Agent
    uv run app --port $port > "../logs/${name}.log" 2>&1 &
    local pid=$!
    
    # 保存PID
    echo $pid > "../pids/${name}.pid"
    
    echo -e "${GREEN}   ✅ $name 已启动 (PID: $pid)${NC}"
    echo -e "   📋 日志文件: logs/${name}.log"
    echo -e "   🔍 AgentCard: http://localhost:$port/.well-known/agent.json"
    echo ""
    
    cd ..
    return 0
}

# 创建必要的目录
mkdir -p logs pids

echo "🔍 检查端口可用性..."
ports_ok=true
check_port 8000 "Orchestrator" || ports_ok=false
check_port 8001 "ResourceAnalyzer" || ports_ok=false
check_port 8002 "ImageProcessor" || ports_ok=false
check_port 8003 "ResourceReplacer" || ports_ok=false

if [ "$ports_ok" = false ]; then
    echo -e "${RED}❌ 部分端口被占用，请停止相关服务或更改端口配置${NC}"
    exit 1
fi

echo -e "${GREEN}✅ 所有端口可用${NC}"
echo ""

# 启动所有Agent
echo "🚀 启动所有Agent..."
echo ""

start_agent "orchestrator" 8000 "Orchestrator" "$PURPLE"
start_agent "resource-analyzer" 8001 "ResourceAnalyzer" "$BLUE"
start_agent "image-processor" 8002 "ImageProcessor" "$CYAN"
start_agent "resource-replacer" 8003 "ResourceReplacer" "$YELLOW"

# 等待Agent启动
echo "⏳ 等待Agent启动完成..."
sleep 3

# 检查Agent状态
echo "🏥 检查Agent健康状态..."
echo ""

check_agent_health() {
    local port=$1
    local name=$2
    local color=$3
    
    echo -e "${color}🔍 检查 $name (端口:$port)${NC}"
    
    if curl -s --max-time 5 "http://localhost:$port/.well-known/agent.json" > /dev/null; then
        echo -e "${GREEN}   ✅ $name 运行正常${NC}"
        return 0
    else
        echo -e "${RED}   ❌ $name 启动失败或未就绪${NC}"
        return 1
    fi
}

health_ok=true
check_agent_health 8000 "Orchestrator" "$PURPLE" || health_ok=false
check_agent_health 8001 "ResourceAnalyzer" "$BLUE" || health_ok=false
check_agent_health 8002 "ImageProcessor" "$CYAN" || health_ok=false
check_agent_health 8003 "ResourceReplacer" "$YELLOW" || health_ok=false

echo ""

if [ "$health_ok" = true ]; then
    echo -e "${GREEN}🎉 所有Agent启动成功！${NC}"
    echo ""
    echo "📋 系统信息:"
    echo "🎭 Orchestrator:     http://localhost:8000"
    echo "🔍 ResourceAnalyzer: http://localhost:8001"
    echo "🎨 ImageProcessor:   http://localhost:8002"
    echo "📁 ResourceReplacer: http://localhost:8003"
    echo ""
    echo "🧪 测试系统:"
    echo "   cd orchestrator && python test_client.py"
    echo ""
    echo "📖 查看日志:"
    echo "   tail -f logs/Orchestrator.log"
    echo ""
    echo "⏹️ 停止所有Agent:"
    echo "   ./stop-all.sh"
else
    echo -e "${RED}❌ 部分Agent启动失败，请检查日志文件${NC}"
    echo ""
    echo "📋 日志文件:"
    echo "   logs/Orchestrator.log"
    echo "   logs/ResourceAnalyzer.log"
    echo "   logs/ImageProcessor.log"
    echo "   logs/ResourceReplacer.log"
    exit 1
fi 