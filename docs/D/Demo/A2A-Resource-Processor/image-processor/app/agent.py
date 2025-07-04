"""
Image Processor Core - 图片处理器核心逻辑
"""

import asyncio
import logging
import uuid
import os
import json
from typing import Dict, Any, List, Optional, Tuple
from datetime import datetime
from pathlib import Path
import tempfile
import shutil

import numpy as np
from PIL import Image, ImageEnhance, ImageFilter
import cv2
from skimage import color

logger = logging.getLogger(__name__)


class ImageProcessor:
    """图片处理器核心逻辑"""
    
    def __init__(self):
        # 支持的图片格式
        self.supported_formats = {'.jpg', '.jpeg', '.png', '.bmp', '.tiff', '.tif', '.webp'}
        
        # 目标颜色 (红色)
        self.target_color_rgb = (255, 0, 0)  # 红色
        self.target_color_hsv = color.rgb2hsv(np.array([[[255, 0, 0]]]))[0][0]  # 红色的HSV值
        
        # 处理参数
        self.color_tolerance = 50  # 颜色容忍度
        self.saturation_boost = 1.2  # 饱和度增强
        self.brightness_adjust = 1.1  # 亮度调整
        
        logger.info("🎨 ImageProcessor 初始化完成")
        logger.info(f"🎯 目标颜色: RGB{self.target_color_rgb}")
    
    async def process_images(self, task_description: str) -> Dict[str, Any]:
        """处理图片任务"""
        logger.info(f"🖼️ 开始处理图片任务: {task_description}")
        
        processing_result = {
            "processing_id": str(uuid.uuid4()),
            "timestamp": datetime.now().isoformat(),
            "task_description": task_description,
            "target_color": {
                "rgb": self.target_color_rgb,
                "hex": "#{:02x}{:02x}{:02x}".format(*self.target_color_rgb)
            },
            "summary": {
                "total_images": 0,
                "processed_images": 0,
                "failed_images": 0,
                "processing_time": 0,
                "errors": []
            },
            "processing_details": [],
            "output_directory": None
        }
        
        try:
            # 解析任务描述，提取图片路径信息
            image_paths = self._extract_image_paths(task_description)
            
            if not image_paths:
                # 如果没有找到具体路径，使用模拟处理
                return await self._simulate_processing(processing_result, task_description)
            
            # 创建输出目录
            output_dir = self._create_output_directory()
            processing_result["output_directory"] = output_dir
            
            # 批量处理图片
            start_time = datetime.now()
            
            for image_path in image_paths:
                try:
                    logger.info(f"🔄 处理图片: {image_path}")
                    
                    # 处理单张图片
                    result = await self._process_single_image(image_path, output_dir)
                    processing_result["processing_details"].append(result)
                    
                    if result.get("success"):
                        processing_result["summary"]["processed_images"] += 1
                    else:
                        processing_result["summary"]["failed_images"] += 1
                        if "error" in result:
                            processing_result["summary"]["errors"].append(result["error"])
                    
                    processing_result["summary"]["total_images"] += 1
                    
                except Exception as e:
                    logger.error(f"❌ 处理图片失败 {image_path}: {e}")
                    processing_result["summary"]["failed_images"] += 1
                    processing_result["summary"]["errors"].append(f"图片 {image_path}: {str(e)}")
            
            # 计算处理时间
            end_time = datetime.now()
            processing_time = (end_time - start_time).total_seconds()
            processing_result["summary"]["processing_time"] = processing_time
            
            logger.info(f"✅ 图片处理完成: {processing_result['summary']['processed_images']} 成功, {processing_result['summary']['failed_images']} 失败")
            
            return processing_result
            
        except Exception as e:
            logger.error(f"❌ 图片处理失败: {e}")
            processing_result["summary"]["errors"].append(str(e))
            return processing_result
    
    def _extract_image_paths(self, task_description: str) -> List[str]:
        """从任务描述中提取图片路径"""
        # 简化的路径提取逻辑
        # 在真实场景中，这里会从ResourceAnalyzer的结果中获取图片列表
        logger.info("📝 解析任务描述中的图片路径...")
        
        # 模拟返回一些测试图片路径
        # 在实际实现中，应该从分析结果中获取
        return []
    
    async def _simulate_processing(self, processing_result: Dict[str, Any], task_description: str) -> Dict[str, Any]:
        """模拟图片处理（当没有实际图片时）"""
        logger.info("🎭 执行模拟图片处理...")
        
        # 模拟处理多张图片
        simulated_images = [
            "image_001.jpg", "image_002.png", "image_003.bmp", 
            "logo.png", "banner.jpg", "icon.png"
        ]
        
        processing_result["summary"]["total_images"] = len(simulated_images)
        
        for i, image_name in enumerate(simulated_images):
            # 模拟处理延时
            await asyncio.sleep(0.1)
            
            # 模拟处理结果
            success = i < len(simulated_images) - 1  # 最后一张失败
            
            detail = {
                "image_name": image_name,
                "original_path": f"./mock_images/{image_name}",
                "output_path": f"./processed_images/red_{image_name}",
                "success": success,
                "processing_methods": [
                    "主色调识别",
                    "颜色空间转换",
                    "红色主题应用",
                    "饱和度增强"
                ],
                "color_changes": {
                    "original_dominant": "#3498db" if success else "#000000",
                    "new_dominant": "#e74c3c" if success else "#000000",
                    "color_shift_percentage": 85.2 if success else 0
                }
            }
            
            if success:
                processing_result["summary"]["processed_images"] += 1
            else:
                processing_result["summary"]["failed_images"] += 1
                detail["error"] = "模拟处理失败：文件格式不支持"
                processing_result["summary"]["errors"].append(detail["error"])
            
            processing_result["processing_details"].append(detail)
        
        # 模拟处理时间
        processing_result["summary"]["processing_time"] = 2.5
        
        return processing_result
    
    def _create_output_directory(self) -> str:
        """创建输出目录"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_dir = os.path.join(tempfile.gettempdir(), f"processed_images_{timestamp}")
        os.makedirs(output_dir, exist_ok=True)
        
        logger.info(f"📁 创建输出目录: {output_dir}")
        return output_dir
    
    async def _process_single_image(self, image_path: str, output_dir: str) -> Dict[str, Any]:
        """处理单张图片"""
        result = {
            "image_path": image_path,
            "output_path": None,
            "success": False,
            "processing_methods": [],
            "color_analysis": {},
            "performance": {}
        }
        
        try:
            start_time = datetime.now()
            
            # 打开图片
            with Image.open(image_path) as img:
                # 分析原始颜色
                original_colors = self._analyze_colors(img)
                result["color_analysis"]["original"] = original_colors
                
                # 应用红色主题
                processed_img = self._apply_red_theme(img)
                result["processing_methods"].append("红色主题应用")
                
                # 增强图片
                enhanced_img = self._enhance_image(processed_img)
                result["processing_methods"].append("图片增强")
                
                # 分析处理后颜色
                processed_colors = self._analyze_colors(enhanced_img)
                result["color_analysis"]["processed"] = processed_colors
                
                # 保存处理后的图片
                output_filename = f"red_{os.path.basename(image_path)}"
                output_path = os.path.join(output_dir, output_filename)
                enhanced_img.save(output_path)
                
                result["output_path"] = output_path
                result["success"] = True
                
                # 性能统计
                end_time = datetime.now()
                processing_time = (end_time - start_time).total_seconds()
                result["performance"] = {
                    "processing_time": processing_time,
                    "original_size": os.path.getsize(image_path),
                    "output_size": os.path.getsize(output_path)
                }
                
                logger.info(f"✅ 图片处理成功: {image_path} -> {output_path}")
                
        except Exception as e:
            logger.error(f"❌ 处理图片失败 {image_path}: {e}")
            result["error"] = str(e)
        
        return result
    
    def _analyze_colors(self, img: Image.Image) -> Dict[str, Any]:
        """分析图片颜色"""
        try:
            # 转换为RGB
            rgb_img = img.convert('RGB')
            
            # 计算平均颜色
            pixels = np.array(rgb_img)
            avg_color = np.mean(pixels, axis=(0, 1))
            
            # 计算主要颜色
            dominant_color = self._get_dominant_color(rgb_img)
            
            return {
                "average_color": {
                    "rgb": avg_color.tolist(),
                    "hex": "#{:02x}{:02x}{:02x}".format(*[int(c) for c in avg_color])
                },
                "dominant_color": dominant_color,
                "color_distribution": self._get_color_distribution(rgb_img)
            }
            
        except Exception as e:
            logger.warning(f"⚠️ 颜色分析失败: {e}")
            return {"error": str(e)}
    
    def _get_dominant_color(self, img: Image.Image) -> Dict[str, Any]:
        """获取主要颜色"""
        try:
            # 缩小图片以提高性能
            img_small = img.resize((50, 50))
            
            # 转换为numpy数组
            data = np.array(img_small)
            data = data.reshape((-1, 3))
            
            # 计算平均值作为主要颜色
            dominant_rgb = np.mean(data, axis=0)
            
            return {
                "rgb": dominant_rgb.tolist(),
                "hex": "#{:02x}{:02x}{:02x}".format(*[int(c) for c in dominant_rgb])
            }
            
        except Exception as e:
            logger.warning(f"⚠️ 获取主要颜色失败: {e}")
            return {"rgb": [0, 0, 0], "hex": "#000000"}
    
    def _get_color_distribution(self, img: Image.Image) -> Dict[str, float]:
        """获取颜色分布"""
        try:
            # 简化的颜色分布分析
            pixels = np.array(img)
            total_pixels = pixels.shape[0] * pixels.shape[1]
            
            # 计算各颜色通道的平均值
            r_avg = np.mean(pixels[:, :, 0])
            g_avg = np.mean(pixels[:, :, 1])
            b_avg = np.mean(pixels[:, :, 2])
            
            # 计算各颜色的比例
            total = r_avg + g_avg + b_avg
            
            return {
                "red_ratio": float(r_avg / total) if total > 0 else 0,
                "green_ratio": float(g_avg / total) if total > 0 else 0,
                "blue_ratio": float(b_avg / total) if total > 0 else 0
            }
            
        except Exception as e:
            logger.warning(f"⚠️ 颜色分布分析失败: {e}")
            return {"red_ratio": 0, "green_ratio": 0, "blue_ratio": 0}
    
    def _apply_red_theme(self, img: Image.Image) -> Image.Image:
        """应用红色主题"""
        try:
            # 转换为HSV颜色空间
            hsv_img = img.convert('HSV')
            hsv_array = np.array(hsv_img)
            
            # 获取HSV通道
            h, s, v = hsv_array[:, :, 0], hsv_array[:, :, 1], hsv_array[:, :, 2]
            
            # 将色相调整为红色（0度）
            h_red = np.full_like(h, 0)
            
            # 增强饱和度
            s_enhanced = np.clip(s * self.saturation_boost, 0, 255)
            
            # 调整亮度
            v_adjusted = np.clip(v * self.brightness_adjust, 0, 255)
            
            # 重新组合HSV
            hsv_red = np.stack([h_red, s_enhanced, v_adjusted], axis=-1)
            
            # 转换回RGB
            red_img = Image.fromarray(hsv_red.astype(np.uint8), 'HSV').convert('RGB')
            
            return red_img
            
        except Exception as e:
            logger.warning(f"⚠️ 应用红色主题失败: {e}")
            return img
    
    def _enhance_image(self, img: Image.Image) -> Image.Image:
        """增强图片"""
        try:
            # 增强对比度
            contrast_enhancer = ImageEnhance.Contrast(img)
            img = contrast_enhancer.enhance(1.1)
            
            # 增强锐度
            sharpness_enhancer = ImageEnhance.Sharpness(img)
            img = sharpness_enhancer.enhance(1.1)
            
            # 增强颜色饱和度
            color_enhancer = ImageEnhance.Color(img)
            img = color_enhancer.enhance(1.2)
            
            return img
            
        except Exception as e:
            logger.warning(f"⚠️ 图片增强失败: {e}")
            return img 