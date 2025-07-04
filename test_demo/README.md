# A2A资源处理系统测试Demo

这是一个完整的A2A (Agent-to-Agent) 资源处理系统测试Demo，展示了多Agent协作完成复杂工作流的过程。

## 🎯 Demo功能

这个Demo将演示：

1. **资源分析** - 扫描目录，识别图片文件和其他资源
2. **图像处理** - 将图片的主题色替换为指定颜色（红色）
3. **资源替换** - 安全地替换原始文件，包括备份机制
4. **工作流编排** - 协调多个Agent按顺序完成任务

## 🏗️ 系统架构

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Orchestrator  │───▶│Resource Analyzer│───▶│ Image Processor │───▶│Resource Replacer│
│   (端口 8000)   │    │   (端口 8001)   │    │   (端口 8002)   │    │   (端口 8003)   │
│                 │    │                 │    │                 │    │                 │
│ 工作流编排      │    │ 目录扫描        │    │ 图像主题色替换  │    │ 文件替换备份    │
│ Agent协调       │    │ 文件分析        │    │ 颜色空间转换    │    │ 版本控制        │
└─────────────────┘    └─────────────────┘    └─────────────────┘    └─────────────────┘
```

## 📋 系统要求

- Python 3.10+
- UV 包管理器
- 所需Python包：
  - `a2a-sdk>=0.2.6` (Google A2A SDK)
  - `httpx`, `rich`, `click`, `pillow`
  - `uvicorn`, `pydantic`

## 🚀 快速开始

### 方法1: 运行完整Demo (推荐)

```bash
# 进入Demo目录
cd test_demo

# 运行完整Demo（自动创建测试图片、启动所有Agent、执行工作流）
python run_demo.py
```

### 方法2: 手动步骤

```bash
# 1. 创建测试图片
cd test_demo
python create_test_images.py

# 2. 启动所有Agent (需要4个终端窗口)
# 终端1 - Orchestrator
cd ../orchestrator && uv run app --port 8000

# 终端2 - Resource Analyzer  
cd ../resource-analyzer && uv run app --port 8001

# 终端3 - Image Processor
cd ../image-processor && uv run app --port 8002

# 终端4 - Resource Replacer
cd ../resource-replacer && uv run app --port 8003

# 3. 运行测试客户端
cd ../orchestrator
uv run python test_client.py --message "帮我分析一下 ../test_demo/test_images 目录中的所有资源，并替换所有资源图片的主题色为红色"
```

## 📁 Demo目录结构

```
test_demo/
├── README.md                 # 本说明文件
├── run_demo.py              # 完整Demo运行脚本
├── create_test_images.py    # 测试图片生成脚本
└── test_images/            # 测试图片目录（运行后生成）
    ├── blue_sample.png
    ├── green_sample.png
    ├── yellow_sample.png
    ├── purple_sample.png
    ├── orange_sample.png
    ├── readme.txt
    └── subfolder/
        ├── cyan_image.png
        └── magenta_image.png
```

## 🔍 运行结果

Demo成功运行后，你将看到：

1. **测试图片创建** - 7张不同颜色的测试图片
2. **Agent启动** - 4个Agent服务启动并报告健康状态
3. **工作流执行** - 完整的资源处理流程
4. **结果显示** - 处理统计和详细日志

### 预期输出示例

```
🎭 A2A资源处理系统完整测试Demo
本Demo将展示多Agent协作完成资源处理工作流
包括：资源分析 → 图像处理 → 资源替换

📝 步骤1: 创建测试数据
🎨 创建测试图片...
✅ 创建测试图片: test_images/blue_sample.png (blue)
✅ 创建测试图片: test_images/green_sample.png (green)
...

🚀 步骤2: 启动所有Agent服务
🚀 启动 orchestrator Agent (端口 8000)
🚀 启动 resource-analyzer Agent (端口 8001)
🚀 启动 image-processor Agent (端口 8002)
🚀 启动 resource-replacer Agent (端口 8003)

⏳ 步骤3: 等待Agent准备就绪
✅ 所有Agent已准备就绪!

🧪 步骤4: 运行资源处理工作流
✅ 工作流执行成功!

📊 步骤5: Demo总结
┏━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━┳━━━━━━━┳━━━━━━━━━━━━━━┓
┃ 组件              ┃ 状态      ┃ 端口  ┃ 功能         ┃
┡━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━╇━━━━━━━╇━━━━━━━━━━━━━━┩
│ orchestrator      │ ✅ 运行中 │ 8000  │ 工作流编排   │
│ resource-analyzer │ ✅ 运行中 │ 8001  │ 资源分析     │
│ image-processor   │ ✅ 运行中 │ 8002  │ 图像处理     │
│ resource-replacer │ ✅ 运行中 │ 8003  │ 资源替换     │
└───────────────────┴───────────┴───────┴──────────────┘

🎉 Demo执行成功!
A2A资源处理系统已完成完整的工作流演示。
你可以检查test_images目录查看处理结果。
```

## 🛠️ 故障排除

### 常见问题

1. **端口被占用**
   ```bash
   # 检查端口占用
   lsof -i :8000
   lsof -i :8001
   lsof -i :8002
   lsof -i :8003
   
   # 杀死占用进程
   kill -9 <PID>
   ```

2. **依赖缺失**
   ```bash
   # 安装依赖
   cd orchestrator && uv sync
   cd ../resource-analyzer && uv sync
   cd ../image-processor && uv sync  
   cd ../resource-replacer && uv sync
   ```

3. **权限问题**
   ```bash
   # 确保脚本可执行
   chmod +x run_demo.py
   chmod +x create_test_images.py
   ```

### 调试模式

如果需要调试，可以单独启动Agent并查看日志：

```bash
# 以调试模式启动Orchestrator
cd orchestrator
uv run app --port 8000 --debug
```

## 🔗 相关文档

- [A2A SDK文档](https://github.com/google-a2a/A2A)
- [项目README](../README.md)
- [Agent架构设计](../README.md#architecture)

## 📝 注意事项

1. **测试环境** - 这个Demo仅用于演示和测试，不适用于生产环境
2. **数据安全** - Demo会修改测试图片，请确保使用专门的测试目录
3. **资源清理** - Demo会自动清理启动的Agent进程
4. **网络要求** - 需要本地端口8000-8003可用

## 💡 扩展建议

你可以基于这个Demo进行扩展：

1. **添加更多Agent** - 实现更复杂的处理流程
2. **支持更多格式** - 处理视频、音频等其他媒体文件
3. **云端部署** - 将Agent部署到不同的服务器
4. **监控面板** - 添加实时监控和日志查看界面
5. **配置管理** - 支持动态配置Agent参数

---

如有问题，请检查各Agent的日志文件或查看项目文档。 