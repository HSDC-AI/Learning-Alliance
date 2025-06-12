from typing import Any
import httpx
from mcp.server.fastmcp import FastMCP

# 初始化 FastMCP server
mcp = FastMCP("weather")

# Constants
NWS_API_BASE = "https://api.weather.gov"
USER_AGENT = "weather-app/1.0"

# 异步返回接口请求
async def make_nws_request(url: str) -> dict[str, Any] | None: 
    """向 NWS API 发送请求，并进行适当的错误处理。"""
    headers = {
        "User-Agent": USER_AGENT,
        "Accept": "application/geo+json"
    }
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(url, headers=headers, timeout=30.0)
            response.raise_for_status()
            return response.json()
        except Exception:
            return None
        


def format_alert(feature: dict) -> str:
    """将警报 feature 格式化为可读的字符串。"""
    props = feature["properties"]
    return f"""
     事件: {props.get('event', 'Unknown')}
     区域: {props.get('areaDesc', 'Unknown')}
     严重性: {props.get('severity', 'Unknown')}
     描述: {props.get('description', 'No description available')}
     指示: {props.get('instruction', 'No specific instructions provided')}
     """
     
@mcp.tool()
async def get_alerts(state: str) -> str:
    """获取美国州的天气预报
    
    Args:
        state: 两个字母的美国州代码（例如 CA、NY）
    """
    url = f"{NWS_API_BASE}/alerts/active/area/{state}"
    data = await make_nws_request(url)
    if not data or "features" not in data:
        return "无法获取天气预报或未找到天气预报"
      
    if not data["features"]:
        return "没有找到天气预报"
    
    alerts = [format_alert(feature) for feature in data["features"]] 
    return "\n---\n".join(alerts)
   

@mcp.tool()
async def get_forecast(latitude: float, longitude: float) -> str:
    """获取某个位置的天气预报。
    
    Args:
        latitude： 位置的维度
        longitude 位置的经度
    """
    # 首先获取天气预报的网络 endpoint
    points_url = f"{NWS_API_BASE}/points/{latitude},{longitude}"
    points_data = await make_nws_request(points_url)
    if not points_data:
        return "无法获取天气预报或未找到天气预报"
    
    # 从 points response 中提取URL
    forecast_url = points_data["properties"]["forecast"]
    forecast_data = await make_nws_request(forecast_url)
    
    if not forecast_data:
        return "无法获取天气预报或未找到天气预报"
    
    # 将 periods 格式化为可读的字符串
    periods = forecast_data["properties"]["periods"]
    forecasts = []
    for period in periods:
        forecast = f"""
        {period['name']}:
        温度：{period['temperature']}°{period['temperatureUnit']}
        风：{period['windSpeed']} {period['windDirection']}
        预报：{period['detailedForecast']}
        """
        forecasts.append(forecast)
    return "\n---\n".join(forecasts)


if __name__ == "__main__":
    mcp.run(transport='stdio')
