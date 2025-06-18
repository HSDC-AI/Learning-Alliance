# MCP Demo - 天气播报员

这是一个MCP (Model Context Protocol) 服务示例，实现了一个天气播报员功能。

## 功能说明

- **Prompt**: `demo` - 定义天气播报员的角色和播报格式
- **Tool**: `get_weather` - 获取指定城市的天气信息

## 配置步骤

### 1. 安装依赖
```bash
pip install mcp[cli]
```

### 2. 配置Claude桌面应用

将以下配置添加到Claude桌面应用的配置文件中：

**macOS**: `~/Library/Application Support/Claude/claude_desktop_config.json`
**Windows**: `%APPDATA%\Claude\claude_desktop_config.json`

```json
{
  "mcpServers": {
    "mcpdemo": {
      "command": "python",
      "args": ["/path/to/your/demo.py"],
      "env": {}
    }
  }
}
```

### 3. 重启Claude桌面应用

配置完成后，重启Claude桌面应用以加载新的MCP服务。

## 使用方法

### 方法1: 直接使用工具
```
北京的天气如何？
```

### 方法2: 明确使用prompt
在对话中提及要使用"demo"这个prompt，或者说"按照天气播报员的方式"。

## 预期输出格式

使用prompt后，输出应该是：
```
我是小李播报员，下面是今天的天气预报：
当前北京的天气是晴天
```

## 测试MCP服务

可以使用以下命令测试服务是否正常：
```bash
python demo.py
```

## 故障排查

1. **Prompt没有生效**：
   - 确保Claude桌面应用已重启
   - 检查配置文件路径是否正确
   - 尝试明确提及要使用"demo" prompt

2. **工具无法调用**：
   - 检查Python环境和依赖
   - 确认MCP服务正常启动
   - 查看Claude桌面应用的日志
