#!/bin/bash

# A2A Resource Processor - 停止所有Agent脚本
# 使用方法: ./stop-all.sh

echo "⏹️ 停止A2A资源处理系统 - 4个Agent"
echo "============================================"

# 定义颜色
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[0;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# 停止单个Agent
stop_agent() {
    local name=$1
    local color=$2
    local pid_file="pids/${name}.pid"
    
    echo -e "${color}⏹️ 停止 $name${NC}"
    
    if [ -f "$pid_file" ]; then
        local pid=$(cat "$pid_file")
        
        if ps -p $pid > /dev/null 2>&1; then
            echo "   🔍 找到进程 PID: $pid"
            kill $pid
            
            # 等待进程停止
            local count=0
            while ps -p $pid > /dev/null 2>&1 && [ $count -lt 10 ]; do
                sleep 1
                count=$((count + 1))
                echo "   ⏳ 等待进程停止... ($count/10)"
            done
            
            if ps -p $pid > /dev/null 2>&1; then
                echo -e "${RED}   ⚠️ 进程未正常停止，强制终止${NC}"
                kill -9 $pid
            fi
            
            echo -e "${GREEN}   ✅ $name 已停止${NC}"
        else
            echo -e "${YELLOW}   ⚠️ 进程 $pid 不存在（可能已停止）${NC}"
        fi
        
        # 删除PID文件
        rm -f "$pid_file"
    else
        echo -e "${YELLOW}   ⚠️ 未找到PID文件，尝试按端口查找进程${NC}"
        
        # 根据Agent名称确定端口
        case "$name" in
            "Orchestrator")
                port=8000
                ;;
            "ResourceAnalyzer")
                port=8001
                ;;
            "ImageProcessor")
                port=8002
                ;;
            "ResourceReplacer")
                port=8003
                ;;
            *)
                echo -e "${RED}   ❌ 未知的Agent名称: $name${NC}"
                return
                ;;
        esac
        
        # 查找并终止占用端口的进程
        local pid=$(lsof -ti:$port)
        if [ -n "$pid" ]; then
            echo "   🔍 找到占用端口 $port 的进程 PID: $pid"
            kill $pid
            echo -e "${GREEN}   ✅ 已终止进程 $pid${NC}"
        else
            echo -e "${YELLOW}   ℹ️ 端口 $port 未被占用${NC}"
        fi
    fi
    
    echo ""
}

# 检查pids目录是否存在
if [ ! -d "pids" ]; then
    echo -e "${YELLOW}⚠️ pids目录不存在，可能没有运行的Agent${NC}"
    echo ""
fi

# 停止所有Agent
stop_agent "Orchestrator" "$PURPLE"
stop_agent "ResourceAnalyzer" "$BLUE"
stop_agent "ImageProcessor" "$CYAN"
stop_agent "ResourceReplacer" "$YELLOW"

# 清理
echo "🧹 清理..."

# 删除PID目录（如果为空）
if [ -d "pids" ] && [ -z "$(ls -A pids)" ]; then
    rmdir pids
    echo "   📁 已删除空的pids目录"
fi

# 检查是否还有相关进程
echo ""
echo "🔍 检查剩余进程..."

remaining_processes=$(ps aux | grep -E "(orchestrator|resource-analyzer|image-processor|resource-replacer)" | grep -v grep | grep -v stop-all.sh)

if [ -n "$remaining_processes" ]; then
    echo -e "${YELLOW}⚠️ 发现可能相关的剩余进程:${NC}"
    echo "$remaining_processes"
    echo ""
    echo -e "${YELLOW}如需手动清理，请使用: kill <PID>${NC}"
else
    echo -e "${GREEN}✅ 没有发现相关的剩余进程${NC}"
fi

# 检查端口占用情况
echo ""
echo "🔍 检查端口占用情况..."

ports=(8000 8001 8002 8003)
port_names=("Orchestrator" "ResourceAnalyzer" "ImageProcessor" "ResourceReplacer")

for i in "${!ports[@]}"; do
    port=${ports[$i]}
    name=${port_names[$i]}
    
    if lsof -Pi :$port -sTCP:LISTEN -t >/dev/null 2>&1; then
        echo -e "${RED}   ❌ 端口 $port ($name) 仍被占用${NC}"
    else
        echo -e "${GREEN}   ✅ 端口 $port ($name) 已释放${NC}"
    fi
done

echo ""
echo -e "${GREEN}🎉 停止操作完成！${NC}"

# 显示日志文件位置
if [ -d "logs" ] && [ "$(ls -A logs)" ]; then
    echo ""
    echo "📋 日志文件仍保留在 logs/ 目录中:"
    ls -la logs/
    echo ""
    echo "💡 如需清理日志文件: rm -rf logs/"
fi 