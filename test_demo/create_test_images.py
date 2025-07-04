#!/usr/bin/env python3
"""
创建测试图片脚本
生成一些简单的彩色测试图片用于演示A2A资源处理工作流
"""

import os
from PIL import Image, ImageDraw, ImageFont
import random

def create_test_image(filename, color, size=(300, 200), text=None):
    """创建一个彩色测试图片"""
    # 创建图片
    image = Image.new('RGB', size, color=color)
    draw = ImageDraw.Draw(image)
    
    # 添加文字
    if text:
        # 尝试使用系统字体，如果找不到就使用默认字体
        try:
            font = ImageFont.truetype("/System/Library/Fonts/Arial.ttf", 24)
        except:
            font = ImageFont.load_default()
        
        # 计算文字位置（居中）
        bbox = draw.textbbox((0, 0), text, font=font)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]
        x = (size[0] - text_width) // 2
        y = (size[1] - text_height) // 2
        
        # 绘制文字（白色）
        draw.text((x, y), text, fill='white', font=font)
    
    # 添加一些装饰图形
    # 绘制圆形
    draw.ellipse([20, 20, 80, 80], fill='white', outline='black', width=2)
    
    # 绘制矩形
    draw.rectangle([size[0]-100, 20, size[0]-20, 80], fill='white', outline='black', width=2)
    
    # 绘制线条
    draw.line([20, size[1]-40, size[0]-20, size[1]-40], fill='white', width=3)
    
    # 保存图片
    image.save(filename)
    print(f"✅ 创建测试图片: {filename} ({color})")

def main():
    """主函数"""
    print("🎨 开始创建测试图片...")
    
    # 确保目录存在
    os.makedirs("test_images", exist_ok=True)
    
    # 创建不同颜色的测试图片
    test_images = [
        ("test_images/blue_sample.png", "blue", "Blue Sample"),
        ("test_images/green_sample.png", "green", "Green Sample"), 
        ("test_images/yellow_sample.png", "yellow", "Yellow Sample"),
        ("test_images/purple_sample.png", "purple", "Purple Sample"),
        ("test_images/orange_sample.png", "orange", "Orange Sample"),
    ]
    
    for filename, color, text in test_images:
        create_test_image(filename, color, text=text)
    
    # 创建一个子目录，包含更多图片
    os.makedirs("test_images/subfolder", exist_ok=True)
    
    sub_images = [
        ("test_images/subfolder/cyan_image.png", "cyan", "Cyan"),
        ("test_images/subfolder/magenta_image.png", "magenta", "Magenta"),
    ]
    
    for filename, color, text in sub_images:
        create_test_image(filename, color, size=(250, 150), text=text)
    
    # 创建一个文本文件
    with open("test_images/readme.txt", "w", encoding="utf-8") as f:
        f.write("""# 测试图片说明
        
这些是用于测试A2A资源处理系统的示例图片：

- blue_sample.png - 蓝色主题图片
- green_sample.png - 绿色主题图片  
- yellow_sample.png - 黄色主题图片
- purple_sample.png - 紫色主题图片
- orange_sample.png - 橙色主题图片

subfolder/ 目录包含：
- cyan_image.png - 青色图片
- magenta_image.png - 品红色图片

这些图片将被A2A工作流处理，主题色将被替换为红色。
""")
    
    print("\n📁 测试目录结构:")
    for root, dirs, files in os.walk("test_images"):
        level = root.replace("test_images", "").count(os.sep)
        indent = " " * 2 * level
        print(f"{indent}📂 {os.path.basename(root)}/")
        subindent = " " * 2 * (level + 1)
        for file in files:
            if file.endswith(('.png', '.jpg', '.jpeg')):
                print(f"{subindent}🖼️ {file}")
            else:
                print(f"{subindent}📄 {file}")
    
    print(f"\n✅ 创建完成！总共生成了 {len(test_images) + len(sub_images)} 张测试图片")
    print("💡 现在可以运行 A2A 资源处理工作流来测试图片主题色替换功能")

if __name__ == "__main__":
    main() 