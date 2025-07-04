# Resource Replacer Agent

A2A资源替换器，负责安全的文件替换、备份和版本控制。

## 功能

- 🔄 安全文件替换
- 💾 自动文件备份
- 📋 操作日志记录
- ↩️ 完整回滚支持

## 运行

```bash
uv run app --port 8003
```

## Agent信息

- **端口**: 8003
- **AgentCard**: http://localhost:8003/.well-known/agent.json
- **任务端点**: http://localhost:8003/tasks/send

## 技能

- 资源文件替换
- 备份管理
- 版本控制 