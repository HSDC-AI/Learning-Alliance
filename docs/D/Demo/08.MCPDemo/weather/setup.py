from setuptools import setup, find_packages

setup(
    name="weather-service",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "httpx",
        "mcp",  # 你的依赖
    ],
    entry_points={
        "console_scripts": [
            "weather-service = weather.weather:main"
        ]
    },
)