# Resource Analyzer Agent

A2A资源分析器，负责目录扫描、文件分析和图像颜色分析。

## 功能

- 📁 目录结构分析
- 🖼️ 图像文件识别
- 🎨 图像颜色分析
- 📊 文件信息统计

## 运行

```bash
uv run app --port 8001
```

## Agent信息

- **端口**: 8001
- **AgentCard**: http://localhost:8001/.well-known/agent.json
- **任务端点**: http://localhost:8001/tasks/send

## 技能

- 目录和文件分析
- 图像颜色分析
- 文件信息提取 