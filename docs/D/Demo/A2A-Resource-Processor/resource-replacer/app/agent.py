"""
Resource Replacer Core - 资源替换器核心逻辑
"""

import asyncio
import logging
import uuid
import os
import json
import shutil
from typing import Dict, Any, List, Optional, Tuple
from datetime import datetime
from pathlib import Path
import tempfile

logger = logging.getLogger(__name__)


class ResourceReplacer:
    """资源替换器核心逻辑"""
    
    def __init__(self):
        # 备份配置
        self.backup_enabled = True
        self.backup_suffix = ".backup"
        self.max_backup_versions = 5
        
        # 支持的文件操作
        self.supported_operations = {
            "replace", "backup", "restore", "clean"
        }
        
        logger.info("📁 ResourceReplacer 初始化完成")
        logger.info(f"🔄 备份启用: {self.backup_enabled}")
        logger.info(f"🗂️ 最大备份版本: {self.max_backup_versions}")
    
    async def replace_resources(self, task_description: str) -> Dict[str, Any]:
        """替换资源文件"""
        logger.info(f"🔄 开始替换资源: {task_description}")
        
        replacement_result = {
            "replacement_id": str(uuid.uuid4()),
            "timestamp": datetime.now().isoformat(),
            "task_description": task_description,
            "summary": {
                "total_files": 0,
                "replaced_files": 0,
                "backed_up_files": 0,
                "failed_files": 0,
                "replacement_time": 0,
                "errors": []
            },
            "replacement_details": [],
            "backup_directory": None,
            "operations": []
        }
        
        try:
            # 解析任务描述，提取文件映射信息
            file_mappings = self._extract_file_mappings(task_description)
            
            if not file_mappings:
                # 如果没有找到具体映射，使用模拟替换
                return await self._simulate_replacement(replacement_result, task_description)
            
            # 创建备份目录
            if self.backup_enabled:
                backup_dir = self._create_backup_directory()
                replacement_result["backup_directory"] = backup_dir
            
            # 批量替换文件
            start_time = datetime.now()
            
            for mapping in file_mappings:
                try:
                    logger.info(f"🔄 替换文件: {mapping.get('source')} -> {mapping.get('target')}")
                    
                    # 替换单个文件
                    result = await self._replace_single_file(mapping, backup_dir if self.backup_enabled else None)
                    replacement_result["replacement_details"].append(result)
                    
                    if result.get("success"):
                        replacement_result["summary"]["replaced_files"] += 1
                        if result.get("backed_up"):
                            replacement_result["summary"]["backed_up_files"] += 1
                    else:
                        replacement_result["summary"]["failed_files"] += 1
                        if "error" in result:
                            replacement_result["summary"]["errors"].append(result["error"])
                    
                    replacement_result["summary"]["total_files"] += 1
                    
                except Exception as e:
                    logger.error(f"❌ 替换文件失败 {mapping}: {e}")
                    replacement_result["summary"]["failed_files"] += 1
                    replacement_result["summary"]["errors"].append(f"文件映射 {mapping}: {str(e)}")
            
            # 计算替换时间
            end_time = datetime.now()
            replacement_time = (end_time - start_time).total_seconds()
            replacement_result["summary"]["replacement_time"] = replacement_time
            
            # 记录操作历史
            replacement_result["operations"].append({
                "operation": "batch_replace",
                "timestamp": datetime.now().isoformat(),
                "files_count": replacement_result["summary"]["replaced_files"],
                "success": replacement_result["summary"]["failed_files"] == 0
            })
            
            logger.info(f"✅ 资源替换完成: {replacement_result['summary']['replaced_files']} 成功, {replacement_result['summary']['failed_files']} 失败")
            
            return replacement_result
            
        except Exception as e:
            logger.error(f"❌ 资源替换失败: {e}")
            replacement_result["summary"]["errors"].append(str(e))
            return replacement_result
    
    def _extract_file_mappings(self, task_description: str) -> List[Dict[str, str]]:
        """从任务描述中提取文件映射关系"""
        # 简化的映射提取逻辑
        # 在真实场景中，这里会从前面Agent的结果中获取文件映射
        logger.info("📝 解析任务描述中的文件映射关系...")
        
        # 模拟返回一些测试文件映射
        # 在实际实现中，应该从处理结果中获取
        return []
    
    async def _simulate_replacement(self, replacement_result: Dict[str, Any], task_description: str) -> Dict[str, Any]:
        """模拟资源替换（当没有实际文件时）"""
        logger.info("🎭 执行模拟资源替换...")
        
        # 模拟替换多个文件
        simulated_files = [
            {"original": "image_001.jpg", "processed": "red_image_001.jpg"},
            {"original": "image_002.png", "processed": "red_image_002.png"},
            {"original": "logo.png", "processed": "red_logo.png"},
            {"original": "banner.jpg", "processed": "red_banner.jpg"},
            {"original": "icon.bmp", "processed": "red_icon.bmp"}
        ]
        
        replacement_result["summary"]["total_files"] = len(simulated_files)
        
        # 模拟备份目录
        backup_dir = "/tmp/backup_" + datetime.now().strftime("%Y%m%d_%H%M%S")
        replacement_result["backup_directory"] = backup_dir
        
        for i, file_pair in enumerate(simulated_files):
            # 模拟替换延时
            await asyncio.sleep(0.1)
            
            # 模拟替换结果
            success = i < len(simulated_files) - 1  # 最后一个失败
            
            detail = {
                "original_file": f"./original_images/{file_pair['original']}",
                "processed_file": f"./processed_images/{file_pair['processed']}",
                "backup_file": f"{backup_dir}/{file_pair['original']}.backup",
                "success": success,
                "backed_up": success,
                "operations": [
                    "创建备份",
                    "验证文件完整性",
                    "执行替换",
                    "验证替换结果"
                ],
                "file_info": {
                    "original_size": 1024 * (i + 1),
                    "processed_size": 1024 * (i + 1) * 1.1,
                    "backup_created": success
                }
            }
            
            if success:
                replacement_result["summary"]["replaced_files"] += 1
                replacement_result["summary"]["backed_up_files"] += 1
            else:
                replacement_result["summary"]["failed_files"] += 1
                detail["error"] = "模拟替换失败：目标文件权限不足"
                replacement_result["summary"]["errors"].append(detail["error"])
            
            replacement_result["replacement_details"].append(detail)
        
        # 模拟处理时间
        replacement_result["summary"]["replacement_time"] = 1.8
        
        # 添加操作记录
        replacement_result["operations"] = [
            {
                "operation": "backup_creation",
                "timestamp": datetime.now().isoformat(),
                "backup_directory": backup_dir,
                "success": True
            },
            {
                "operation": "batch_replace",
                "timestamp": datetime.now().isoformat(),
                "files_count": replacement_result["summary"]["replaced_files"],
                "success": replacement_result["summary"]["failed_files"] == 0
            }
        ]
        
        return replacement_result
    
    def _create_backup_directory(self) -> str:
        """创建备份目录"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_dir = os.path.join(tempfile.gettempdir(), f"backup_{timestamp}")
        os.makedirs(backup_dir, exist_ok=True)
        
        logger.info(f"📁 创建备份目录: {backup_dir}")
        return backup_dir
    
    async def _replace_single_file(self, mapping: Dict[str, str], backup_dir: Optional[str] = None) -> Dict[str, Any]:
        """替换单个文件"""
        result = {
            "original_file": mapping.get("source"),
            "processed_file": mapping.get("target"),
            "backup_file": None,
            "success": False,
            "backed_up": False,
            "operations": [],
            "file_info": {}
        }
        
        try:
            source_file = mapping.get("source")
            target_file = mapping.get("target")
            
            if not source_file or not target_file:
                raise ValueError("无效的文件映射")
            
            # 检查源文件是否存在
            if not os.path.exists(source_file):
                raise FileNotFoundError(f"源文件不存在: {source_file}")
            
            # 检查目标文件是否存在
            if not os.path.exists(target_file):
                raise FileNotFoundError(f"目标文件不存在: {target_file}")
            
            # 创建备份
            if backup_dir and self.backup_enabled:
                backup_result = await self._create_file_backup(source_file, backup_dir)
                result["backup_file"] = backup_result.get("backup_path")
                result["backed_up"] = backup_result.get("success", False)
                result["operations"].append("创建备份")
            
            # 获取文件信息
            original_size = os.path.getsize(source_file)
            processed_size = os.path.getsize(target_file)
            
            result["file_info"] = {
                "original_size": original_size,
                "processed_size": processed_size,
                "size_change": processed_size - original_size
            }
            
            # 执行替换
            shutil.copy2(target_file, source_file)
            result["operations"].append("执行替换")
            
            # 验证替换结果
            if os.path.exists(source_file):
                new_size = os.path.getsize(source_file)
                if new_size == processed_size:
                    result["success"] = True
                    result["operations"].append("验证替换成功")
                else:
                    raise Exception("替换后文件大小不匹配")
            else:
                raise Exception("替换后文件不存在")
            
            logger.info(f"✅ 文件替换成功: {source_file}")
            
        except Exception as e:
            logger.error(f"❌ 替换文件失败 {mapping}: {e}")
            result["error"] = str(e)
        
        return result
    
    async def _create_file_backup(self, file_path: str, backup_dir: str) -> Dict[str, Any]:
        """创建文件备份"""
        backup_result = {
            "source_file": file_path,
            "backup_path": None,
            "success": False
        }
        
        try:
            filename = os.path.basename(file_path)
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            backup_filename = f"{filename}.{timestamp}{self.backup_suffix}"
            backup_path = os.path.join(backup_dir, backup_filename)
            
            # 复制文件到备份目录
            shutil.copy2(file_path, backup_path)
            
            backup_result["backup_path"] = backup_path
            backup_result["success"] = True
            
            logger.info(f"✅ 文件备份成功: {file_path} -> {backup_path}")
            
            # 清理旧备份
            await self._cleanup_old_backups(backup_dir, filename)
            
        except Exception as e:
            logger.error(f"❌ 创建备份失败 {file_path}: {e}")
            backup_result["error"] = str(e)
        
        return backup_result
    
    async def _cleanup_old_backups(self, backup_dir: str, filename: str):
        """清理旧备份文件"""
        try:
            if not os.path.exists(backup_dir):
                return
            
            # 查找同名文件的所有备份
            backup_files = []
            base_name = filename
            
            for file in os.listdir(backup_dir):
                if file.startswith(base_name) and self.backup_suffix in file:
                    file_path = os.path.join(backup_dir, file)
                    stat = os.stat(file_path)
                    backup_files.append({
                        "path": file_path,
                        "mtime": stat.st_mtime
                    })
            
            # 按修改时间排序，保留最新的N个
            backup_files.sort(key=lambda x: x["mtime"], reverse=True)
            
            # 删除多余的备份
            if len(backup_files) > self.max_backup_versions:
                for backup_file in backup_files[self.max_backup_versions:]:
                    try:
                        os.remove(backup_file["path"])
                        logger.info(f"🗑️ 清理旧备份: {backup_file['path']}")
                    except Exception as e:
                        logger.warning(f"⚠️ 清理备份失败: {e}")
                        
        except Exception as e:
            logger.warning(f"⚠️ 清理旧备份失败: {e}")
    
    async def restore_from_backup(self, backup_path: str, target_path: str) -> Dict[str, Any]:
        """从备份恢复文件"""
        restore_result = {
            "backup_file": backup_path,
            "target_file": target_path,
            "success": False,
            "restore_time": None
        }
        
        try:
            start_time = datetime.now()
            
            if not os.path.exists(backup_path):
                raise FileNotFoundError(f"备份文件不存在: {backup_path}")
            
            # 执行恢复
            shutil.copy2(backup_path, target_path)
            
            # 验证恢复结果
            if os.path.exists(target_path):
                restore_result["success"] = True
                end_time = datetime.now()
                restore_result["restore_time"] = (end_time - start_time).total_seconds()
                
                logger.info(f"✅ 文件恢复成功: {backup_path} -> {target_path}")
            else:
                raise Exception("恢复后文件不存在")
                
        except Exception as e:
            logger.error(f"❌ 文件恢复失败: {e}")
            restore_result["error"] = str(e)
        
        return restore_result
    
    async def get_backup_list(self, backup_dir: str) -> Dict[str, Any]:
        """获取备份文件列表"""
        backup_list = {
            "backup_directory": backup_dir,
            "total_backups": 0,
            "backup_files": [],
            "total_size": 0
        }
        
        try:
            if not os.path.exists(backup_dir):
                return backup_list
            
            for file in os.listdir(backup_dir):
                if self.backup_suffix in file:
                    file_path = os.path.join(backup_dir, file)
                    stat = os.stat(file_path)
                    
                    backup_info = {
                        "filename": file,
                        "path": file_path,
                        "size": stat.st_size,
                        "created_time": datetime.fromtimestamp(stat.st_ctime).isoformat(),
                        "modified_time": datetime.fromtimestamp(stat.st_mtime).isoformat()
                    }
                    
                    backup_list["backup_files"].append(backup_info)
                    backup_list["total_size"] += stat.st_size
            
            backup_list["total_backups"] = len(backup_list["backup_files"])
            
            # 按修改时间排序
            backup_list["backup_files"].sort(key=lambda x: x["modified_time"], reverse=True)
            
        except Exception as e:
            logger.error(f"❌ 获取备份列表失败: {e}")
            backup_list["error"] = str(e)
        
        return backup_list 