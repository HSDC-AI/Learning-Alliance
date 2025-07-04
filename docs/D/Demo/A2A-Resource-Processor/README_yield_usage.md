# Agent 中 yield 的正确用法

## 概述

你说得对！`yield` **应该在 Agent 内部使用**，而不是在客户端。这是实现 Agent 流式响应的核心机制。

## 🎯 正确的架构

```
客户端 ← [HTTP/WebSocket] ← AgentExecutor ← yield ← Agent核心逻辑
```

## 🌟 三层结构

### 1. Agent 核心逻辑层 (使用 yield)
```python
# streaming_agent.py
async def process_resources_stream(self, message: str) -> AsyncGenerator[Dict, None]:
    """Agent的核心处理逻辑 - 这里使用yield"""
    
    # 步骤1: 初始化
    yield {
        "type": "workflow_start",
        "message": "🎭 开始处理...",
        "progress": 0
    }
    
    # 步骤2: 处理过程
    for i in range(10):
        await asyncio.sleep(0.5)  # 模拟处理时间
        
        yield {
            "type": "progress",
            "message": f"处理步骤 {i+1}/10",
            "progress": (i+1) * 10
        }
    
    # 步骤3: 完成
    yield {
        "type": "completion", 
        "message": "✅ 处理完成",
        "progress": 100,
        "result": {"status": "success"}
    }
```

### 2. AgentExecutor 层 (接收 yield)
```python
# streaming_agent_executor.py
class StreamingAgentExecutor(AgentExecutor):
    async def execute(self, context, event_queue):
        """AgentExecutor接收yield并转发给客户端"""
        
        # 🌟 关键：使用Agent的yield方法
        async for update in self.agent.process_resources_stream(message):
            
            # 将yield的结果转换为客户端消息
            await event_queue.enqueue_event(
                new_agent_text_message(f"[{update['progress']}%] {update['message']}")
            )
            
            # 发送结构化数据
            if update["type"] == "completion":
                await event_queue.enqueue_event(
                    new_data_artifact(
                        data=update["result"],
                        artifact_type="application/json"
                    )
                )
```

### 3. 客户端层 (接收响应)
```python
# test_client.py
async def test_send_message(self, message: str):
    """客户端发送消息并接收流式响应"""
    
    response = await a2a_client.send_message(request)
    # 客户端接收最终结果，不直接使用yield
```

## 🔑 关键原则

### ✅ 正确用法
1. **Agent内部使用yield**: 在Agent的处理方法中使用 `async def` + `yield`
2. **AgentExecutor接收**: 用 `async for` 接收Agent的yield结果
3. **转换为消息**: 将yield结果转换为 `new_agent_text_message()` 发送给客户端

### ❌ 错误用法
1. ~~在客户端使用yield~~ - 客户端只负责发送请求和接收响应
2. ~~直接在HTTP接口使用yield~~ - 应该通过A2A的event_queue机制
3. ~~在数据库操作中使用yield~~ - yield用于向客户端报告进度，不是数据处理

## 🚀 实际用例

### 场景1: 批量文件处理
```python
async def process_files_stream(self, files: List[str]):
    for i, file in enumerate(files):
        # 处理文件
        result = await self.process_single_file(file)
        
        # 🌟 yield 进度
        yield {
            "type": "file_progress",
            "file": file,
            "progress": int((i+1) / len(files) * 100),
            "result": result
        }
```

### 场景2: 多Agent协作
```python
async def orchestrate_agents_stream(self, task: str):
    agents = ["analyzer", "processor", "replacer"]
    
    for i, agent in enumerate(agents):
        # 🌟 yield 当前Agent状态
        yield {
            "type": "agent_start",
            "agent": agent,
            "progress": int(i / len(agents) * 100)
        }
        
        # 调用子Agent (也可以有自己的yield)
        async for sub_update in self.call_agent(agent, task):
            yield {
                "type": "sub_progress",
                "agent": agent,
                "sub_update": sub_update
            }
```

### 场景3: 长时间运算
```python
async def complex_calculation_stream(self, data):
    steps = ["预处理", "计算", "后处理"]
    
    for i, step in enumerate(steps):
        # 🌟 yield 计算步骤
        yield {
            "type": "calculation_step",
            "step": step,
            "progress": int(i / len(steps) * 100)
        }
        
        await self.execute_step(step, data)
```

## 💡 最佳实践

### 1. 进度粒度控制
```python
# ✅ 好的做法：合理的进度粒度
if progress % 10 == 0:  # 每10%更新一次
    yield progress_update

# ❌ 不好的做法：过于频繁
for i in range(1000):
    yield {"progress": i}  # 太频繁，影响性能
```

### 2. 错误处理
```python
async def robust_stream_processing(self):
    try:
        yield {"type": "start", "message": "开始处理"}
        
        # 处理逻辑
        result = await self.do_work()
        
        yield {"type": "success", "result": result}
        
    except Exception as e:
        # 🌟 yield 错误信息
        yield {
            "type": "error",
            "message": f"处理失败: {str(e)}",
            "error_type": type(e).__name__
        }
```

### 3. 数据结构标准化
```python
# 建议的yield数据格式
{
    "type": "progress|start|complete|error",
    "message": "人类可读的消息",
    "progress": 0-100,  # 进度百分比
    "timestamp": "ISO格式时间戳",
    "data": {
        # 具体的业务数据
    }
}
```

## 🎯 总结

**正确的理解**:
- `yield` 是 Agent **内部**的流式处理机制
- 用于向 AgentExecutor 报告实时进度
- AgentExecutor 负责转换并发送给客户端
- 客户端只需要接收最终的 A2A 响应

这样的架构让 Agent 可以提供实时反馈，同时保持了清晰的职责分离。 