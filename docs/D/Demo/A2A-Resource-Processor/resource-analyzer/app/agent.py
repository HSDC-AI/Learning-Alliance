"""
Resource Analyzer Core - 资源分析器核心逻辑
"""

import asyncio
import logging
import uuid
import os
import json
from typing import Dict, Any, List, Optional, Tuple
from datetime import datetime
from pathlib import Path
import mimetypes
import hashlib

import numpy as np
from PIL import Image, ImageStat
import cv2

logger = logging.getLogger(__name__)


class ResourceAnalyzer:
    """资源分析器核心逻辑"""
    
    def __init__(self):
        # 支持的图片格式
        self.supported_image_formats = {
            '.jpg', '.jpeg', '.png', '.bmp', '.tiff', '.tif', 
            '.webp', '.gif', '.ico', '.svg'
        }
        
        # 支持的图片MIME类型
        self.supported_image_mimes = {
            'image/jpeg', 'image/png', 'image/bmp', 'image/tiff',
            'image/webp', 'image/gif', 'image/x-icon', 'image/svg+xml'
        }
        
        logger.info("🔍 ResourceAnalyzer 初始化完成")
    
    async def analyze_directory(self, directory_path: str, user_message: str) -> Dict[str, Any]:
        """分析目录资源"""
        logger.info(f"📂 开始分析目录: {directory_path}")
        
        analysis_result = {
            "analysis_id": str(uuid.uuid4()),
            "timestamp": datetime.now().isoformat(),
            "directory_path": directory_path,
            "user_message": user_message,
            "summary": {
                "total_files": 0,
                "total_directories": 0,
                "image_files": 0,
                "non_image_files": 0,
                "total_size": 0,
                "errors": []
            },
            "directory_structure": {},
            "image_analysis": [],
            "file_list": []
        }
        
        try:
            # 解析目录路径
            parsed_path = self._parse_directory_path(directory_path)
            if not parsed_path:
                raise ValueError(f"无效的目录路径: {directory_path}")
            
            # 检查目录是否存在
            if not os.path.exists(parsed_path):
                raise FileNotFoundError(f"目录不存在: {parsed_path}")
            
            if not os.path.isdir(parsed_path):
                raise ValueError(f"路径不是目录: {parsed_path}")
            
            # 扫描目录结构
            logger.info("🔍 扫描目录结构...")
            analysis_result["directory_structure"] = await self._scan_directory_structure(parsed_path)
            
            # 统计文件信息
            logger.info("📊 分析文件信息...")
            file_info = await self._analyze_files(parsed_path)
            analysis_result["file_list"] = file_info["files"]
            analysis_result["summary"].update(file_info["summary"])
            
            # 分析图片文件
            logger.info("🎨 分析图片文件...")
            image_files = [f for f in file_info["files"] if f.get("is_image")]
            analysis_result["image_analysis"] = await self._analyze_images(image_files)
            
            logger.info(f"✅ 目录分析完成: {len(analysis_result['file_list'])} 个文件")
            
            return analysis_result
            
        except Exception as e:
            logger.error(f"❌ 目录分析失败: {e}")
            analysis_result["summary"]["errors"].append(str(e))
            return analysis_result
    
    def _parse_directory_path(self, path: str) -> Optional[str]:
        """解析目录路径"""
        try:
            # 处理相对路径
            if path.startswith('./'):
                path = path[2:]
            elif path.startswith('~/'):
                path = os.path.expanduser(path)
            
            # 转换为绝对路径
            return os.path.abspath(path)
            
        except Exception as e:
            logger.error(f"❌ 解析目录路径失败: {e}")
            return None
    
    async def _scan_directory_structure(self, root_path: str) -> Dict[str, Any]:
        """扫描目录结构"""
        structure = {
            "name": os.path.basename(root_path),
            "path": root_path,
            "type": "directory",
            "children": []
        }
        
        try:
            items = os.listdir(root_path)
            for item in sorted(items):
                item_path = os.path.join(root_path, item)
                
                if os.path.isdir(item_path):
                    # 递归扫描子目录
                    child_structure = await self._scan_directory_structure(item_path)
                    structure["children"].append(child_structure)
                else:
                    # 文件信息
                    structure["children"].append({
                        "name": item,
                        "path": item_path,
                        "type": "file"
                    })
                    
        except PermissionError:
            logger.warning(f"⚠️ 访问权限不足: {root_path}")
            structure["error"] = "访问权限不足"
        except Exception as e:
            logger.error(f"❌ 扫描目录失败 {root_path}: {e}")
            structure["error"] = str(e)
        
        return structure
    
    async def _analyze_files(self, root_path: str) -> Dict[str, Any]:
        """分析文件信息"""
        files = []
        summary = {
            "total_files": 0,
            "total_directories": 0,
            "image_files": 0,
            "non_image_files": 0,
            "total_size": 0,
            "errors": []
        }
        
        try:
            for root, dirs, filenames in os.walk(root_path):
                # 统计目录数量
                summary["total_directories"] += len(dirs)
                
                for filename in filenames:
                    file_path = os.path.join(root, filename)
                    
                    try:
                        # 获取文件信息
                        file_info = await self._get_file_info(file_path)
                        files.append(file_info)
                        
                        # 更新统计
                        summary["total_files"] += 1
                        summary["total_size"] += file_info.get("size", 0)
                        
                        if file_info.get("is_image"):
                            summary["image_files"] += 1
                        else:
                            summary["non_image_files"] += 1
                            
                    except Exception as e:
                        error_msg = f"分析文件失败 {file_path}: {str(e)}"
                        logger.warning(f"⚠️ {error_msg}")
                        summary["errors"].append(error_msg)
                        
        except Exception as e:
            error_msg = f"扫描目录失败: {str(e)}"
            logger.error(f"❌ {error_msg}")
            summary["errors"].append(error_msg)
        
        return {
            "files": files,
            "summary": summary
        }
    
    async def _get_file_info(self, file_path: str) -> Dict[str, Any]:
        """获取文件信息"""
        try:
            stat = os.stat(file_path)
            file_ext = os.path.splitext(file_path)[1].lower()
            
            file_info = {
                "name": os.path.basename(file_path),
                "path": file_path,
                "size": stat.st_size,
                "modified_time": datetime.fromtimestamp(stat.st_mtime).isoformat(),
                "created_time": datetime.fromtimestamp(stat.st_ctime).isoformat(),
                "extension": file_ext,
                "is_image": self._is_image_file(file_path, file_ext),
                "mime_type": mimetypes.guess_type(file_path)[0],
                "hash": self._calculate_file_hash(file_path)
            }
            
            # 获取图片特定信息
            if file_info["is_image"]:
                try:
                    image_info = await self._get_image_info(file_path)
                    file_info.update(image_info)
                except Exception as e:
                    logger.warning(f"⚠️ 获取图片信息失败 {file_path}: {e}")
            
            return file_info
            
        except Exception as e:
            logger.error(f"❌ 获取文件信息失败 {file_path}: {e}")
            return {
                "name": os.path.basename(file_path),
                "path": file_path,
                "error": str(e)
            }
    
    def _is_image_file(self, file_path: str, file_ext: str) -> bool:
        """判断是否为图片文件"""
        # 根据扩展名判断
        if file_ext in self.supported_image_formats:
            return True
        
        # 根据MIME类型判断
        mime_type = mimetypes.guess_type(file_path)[0]
        if mime_type and mime_type in self.supported_image_mimes:
            return True
        
        return False
    
    def _calculate_file_hash(self, file_path: str) -> str:
        """计算文件哈希值"""
        try:
            hash_md5 = hashlib.md5()
            with open(file_path, "rb") as f:
                for chunk in iter(lambda: f.read(4096), b""):
                    hash_md5.update(chunk)
            return hash_md5.hexdigest()
        except Exception as e:
            logger.warning(f"⚠️ 计算文件哈希失败 {file_path}: {e}")
            return ""
    
    async def _get_image_info(self, image_path: str) -> Dict[str, Any]:
        """获取图片详细信息"""
        try:
            with Image.open(image_path) as img:
                # 基本信息
                image_info = {
                    "width": img.width,
                    "height": img.height,
                    "mode": img.mode,
                    "format": img.format,
                    "has_transparency": img.mode in ('RGBA', 'LA') or 'transparency' in img.info
                }
                
                # 颜色分析
                if img.mode in ('RGB', 'RGBA'):
                    color_analysis = self._analyze_image_colors(img)
                    image_info.update(color_analysis)
                
                return image_info
                
        except Exception as e:
            logger.warning(f"⚠️ 分析图片失败 {image_path}: {e}")
            return {"error": f"图片分析失败: {str(e)}"}
    
    def _analyze_image_colors(self, img: Image.Image) -> Dict[str, Any]:
        """分析图片颜色信息"""
        try:
            # 转换为RGB
            rgb_img = img.convert('RGB')
            
            # 计算平均颜色
            stat = ImageStat.Stat(rgb_img)
            avg_color = [int(c) for c in stat.mean]
            
            # 获取主要颜色
            dominant_colors = self._get_dominant_colors(rgb_img)
            
            return {
                "average_color": {
                    "rgb": avg_color,
                    "hex": "#{:02x}{:02x}{:02x}".format(*avg_color)
                },
                "dominant_colors": dominant_colors,
                "color_count": len(set(rgb_img.getdata()))
            }
            
        except Exception as e:
            logger.warning(f"⚠️ 颜色分析失败: {e}")
            return {"color_analysis_error": str(e)}
    
    def _get_dominant_colors(self, img: Image.Image, num_colors: int = 5) -> List[Dict[str, Any]]:
        """获取主要颜色"""
        try:
            # 缩放图片以提高性能
            img_small = img.resize((150, 150))
            
            # 转换为numpy数组
            data = np.array(img_small)
            data = data.reshape((-1, 3))
            
            # 使用OpenCV的K-means聚类
            criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 100, 0.2)
            _, labels, centers = cv2.kmeans(
                data.astype(np.float32), 
                num_colors, 
                None, 
                criteria, 
                10, 
                cv2.KMEANS_RANDOM_CENTERS
            )
            
            # 计算每个颜色的百分比
            unique, counts = np.unique(labels, return_counts=True)
            
            dominant_colors = []
            for i, (color, count) in enumerate(zip(centers, counts)):
                rgb = [int(c) for c in color]
                percentage = (count / len(labels)) * 100
                
                dominant_colors.append({
                    "rank": i + 1,
                    "rgb": rgb,
                    "hex": "#{:02x}{:02x}{:02x}".format(*rgb),
                    "percentage": round(percentage, 2)
                })
            
            # 按百分比排序
            dominant_colors.sort(key=lambda x: x["percentage"], reverse=True)
            
            return dominant_colors
            
        except Exception as e:
            logger.warning(f"⚠️ 获取主要颜色失败: {e}")
            return []
    
    async def _analyze_images(self, image_files: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """分析图片文件列表"""
        image_analysis = []
        
        for image_file in image_files:
            try:
                analysis = {
                    "file_path": image_file.get("path"),
                    "file_name": image_file.get("name"),
                    "file_size": image_file.get("size"),
                    "image_info": image_file,
                    "needs_processing": self._needs_color_processing(image_file),
                    "recommended_actions": self._get_recommended_actions(image_file)
                }
                
                image_analysis.append(analysis)
                
            except Exception as e:
                logger.warning(f"⚠️ 分析图片失败 {image_file.get('path', 'unknown')}: {e}")
                image_analysis.append({
                    "file_path": image_file.get("path"),
                    "error": str(e)
                })
        
        return image_analysis
    
    def _needs_color_processing(self, image_file: Dict[str, Any]) -> bool:
        """判断图片是否需要颜色处理"""
        # 检查是否有颜色信息
        if "average_color" not in image_file:
            return True
        
        # 检查是否已经是红色主题
        avg_color = image_file.get("average_color", {}).get("rgb", [0, 0, 0])
        
        # 简单的红色检测：红色分量明显大于绿色和蓝色
        if len(avg_color) >= 3:
            r, g, b = avg_color[:3]
            if r > g + 50 and r > b + 50:
                return False  # 已经是红色主题
        
        return True
    
    def _get_recommended_actions(self, image_file: Dict[str, Any]) -> List[str]:
        """获取推荐的处理动作"""
        actions = []
        
        # 基本动作
        actions.append("颜色主题替换为红色")
        
        # 根据图片特征添加特定动作
        if image_file.get("has_transparency"):
            actions.append("保持透明度信息")
        
        if image_file.get("format") == "JPEG":
            actions.append("保持JPEG质量")
        elif image_file.get("format") == "PNG":
            actions.append("优化PNG压缩")
        
        # 根据尺寸添加建议
        width = image_file.get("width", 0)
        height = image_file.get("height", 0)
        
        if width > 2000 or height > 2000:
            actions.append("考虑压缩大尺寸图片")
        
        return actions 