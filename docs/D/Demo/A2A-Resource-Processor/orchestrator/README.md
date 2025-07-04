# Orchestrator Agent

A2A资源处理编排器，负责协调整个资源处理工作流。

## 功能

- 🎯 工作流编排和任务分发
- 🤝 Agent间通信协调
- 📊 处理进度监控
- 🔄 任务状态管理

## 运行

```bash
uv run app --port 8000
```

## Agent信息

- **端口**: 8000
- **AgentCard**: http://localhost:8000/.well-known/agent.json
- **任务端点**: http://localhost:8000/tasks/send

## 技能

- 资源处理工作流编排
- 多Agent协调管理
- 任务进度追踪 