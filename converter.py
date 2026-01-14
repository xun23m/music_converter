#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
音乐格式转换核心逻辑
使用pydub和ffmpeg进行音频处理
"""

import os
import threading
import gc
import asyncio
import time
from concurrent.futures import ThreadPoolExecutor
from typing import List, Optional, Callable
from pathlib import Path
from pydub import AudioSegment
from pydub.exceptions import CouldntDecodeError

from resource_monitor import ResourceMonitor

class MusicConverter:
    """音乐格式转换器核心类"""
    
    # 支持的输入格式
    SUPPORTED_INPUT_FORMATS = ['mp3', 'wav', 'flac', 'aac', 'm4a', 'ogg', 'wma', 'ape', 'tta']
    
    # 支持的输出格式
    SUPPORTED_OUTPUT_FORMATS = ['mp3', 'wav', 'flac', 'aac', 'ogg', 'm4a']
    
    def __init__(self):
        """初始化转换器"""
        self.is_converting = False
        self.current_file = ""
        self.progress_callback = None
        self.status_callback = None
        self.error_callback = None
        self.complete_callback = None
        
        # 资源监控器
        self.resource_monitor = ResourceMonitor()
        self.use_resource_monitor = True  # 是否启用资源监控
        
        # 转换统计
        self.conversion_stats = {
            'start_time': None,
            'processed_files': 0,
            'total_files': 0,
            'current_file_index': 0,
        }
    
    def set_callbacks(self, progress_cb: Callable, status_cb: Callable, 
                     error_cb: Callable, complete_cb: Callable, 
                     resource_cb: Optional[Callable] = None, 
                     prediction_cb: Optional[Callable] = None):
        """设置回调函数"""
        self.progress_callback = progress_cb
        self.status_callback = status_cb
        self.error_callback = error_cb
        self.complete_callback = complete_cb
        
        # 设置资源监控回调
        if resource_cb:
            self.resource_monitor.set_callback('resource_status', resource_cb)
        if prediction_cb:
            self.resource_monitor.set_callback('progress_prediction', prediction_cb)
        
        # 设置并发调整回调
        if resource_cb:
            self.resource_monitor.set_callback('worker_adjustment', self._on_worker_adjustment)
    
    def _on_worker_adjustment(self, status: dict):
        """并发数调整回调"""
        if status['status'] == 'critical':
            self._status(f"⚠️ 资源紧张，建议减少并发数至 {status['available_workers']}")
        elif status['status'] == 'warning':
            self._status(f"⚡ 资源警告，当前推荐并发数: {status['available_workers']}")
    
    def convert_single_file(self, input_path: str, output_format: str, 
                           output_dir: str = None, file_index: int = 0) -> bool:
        """
        转换单个音乐文件（优化版 + 进度预测）
        
        Args:
            input_path: 输入文件路径
            output_format: 输出格式（如 'mp3', 'wav'）
            output_dir: 输出目录，如果为None则使用输入文件所在目录
            file_index: 文件索引（用于进度预测）
            
        Returns:
            bool: 转换是否成功
        """
        audio = None  # 确保在finally中可以清理
        file_size_mb = 0
        start_time = time.time()
        
        try:
            if not os.path.exists(input_path):
                self._error(f"文件不存在: {input_path}")
                return False
            
            # 获取文件信息
            input_path = Path(input_path)
            input_stem = input_path.stem
            input_suffix = input_path.suffix.lower()[1:]  # 去掉点
            
            # 检查输入格式支持
            if input_suffix not in self.SUPPORTED_INPUT_FORMATS:
                self._error(f"不支持的输入格式: {input_suffix}")
                return False
            
            # 检查输出格式支持
            if output_format not in self.SUPPORTED_OUTPUT_FORMATS:
                self._error(f"不支持的输出格式: {output_format}")
                return False
            
            # 设置输出路径
            if output_dir:
                output_path = Path(output_dir) / f"{input_stem}.{output_format}"
            else:
                output_path = input_path.parent / f"{input_stem}.{output_format}"
            
            # 避免覆盖原文件
            if output_path.exists() and output_path == input_path:
                output_path = input_path.parent / f"{input_stem}_converted.{output_format}"
            
            # 获取文件大小（用于进度预测）
            file_size = input_path.stat().st_size
            file_size_mb = file_size / (1024 * 1024)
            
            self._status(f"正在转换 ({file_index}/{self.conversion_stats['total_files']}): {input_path.name} ({file_size_mb:.1f}MB)")
            self._progress(0)
            
            # 加载音频文件（使用内存优化）
            try:
                # 使用临时文件减少内存占用（对于大文件）
                if file_size > 100 * 1024 * 1024:  # 大于100MB
                    self._status(f"正在加载大文件: {input_path.name} ({file_size_mb:.1f}MB)")
                
                audio = AudioSegment.from_file(str(input_path), format=input_suffix)
                
                # 及时清理原始数据
                import gc
                gc.collect()
                
            except CouldntDecodeError:
                self._error(f"无法解码文件: {input_path.name}")
                return False
            except Exception as e:
                self._error(f"加载文件失败: {str(e)}")
                return False
            
            self._progress(50)
            
            # 导出音频文件
            try:
                # MP3需要指定编码器参数
                if output_format == 'mp3':
                    audio.export(str(output_path), format=output_format, 
                               bitrate='192k', parameters=['-q:a', '2'])
                else:
                    audio.export(str(output_path), format=output_format)
                
                # 导出后清理内存
                del audio
                gc.collect()
                
            except Exception as e:
                self._error(f"导出文件失败: {str(e)}")
                return False
            
            self._progress(100)
            
            # 更新统计和进度预测
            self.conversion_stats['processed_files'] += 1
            if self.use_resource_monitor:
                self.resource_monitor.update_progress(
                    self.conversion_stats['processed_files'], 
                    file_size_mb
                )
            
            # 计算处理时间
            elapsed = time.time() - start_time
            self._status(f"转换完成: {output_path.name} (耗时: {elapsed:.1f}秒)")
            
            return True
            
        except Exception as e:
            self._error(f"转换过程中发生错误: {str(e)}")
            return False
        finally:
            # 确保内存清理
            if 'audio' in locals() and audio is not None:
                del audio
            gc.collect()
    
    def convert_folder(self, folder_path: str, output_format: str, 
                      output_dir: str = None) -> bool:
        """
        转换整个文件夹的音乐文件（优化版 + 资源监控）
        
        Args:
            folder_path: 输入文件夹路径
            output_format: 输出格式
            output_dir: 输出目录，如果为None则在原目录创建converted子文件夹
            
        Returns:
            bool: 转换是否成功
        """
        try:
            if not os.path.isdir(folder_path):
                self._error(f"文件夹不存在: {folder_path}")
                return False
            
            # 查找所有支持的音频文件（优化搜索）
            audio_files = []
            for ext in self.SUPPORTED_INPUT_FORMATS:
                # 使用大小写不敏感的搜索
                audio_files.extend(Path(folder_path).glob(f"*.{ext}"))
                audio_files.extend(Path(folder_path).glob(f"*.{ext.upper()}"))
            
            if not audio_files:
                self._error(f"文件夹中没有找到支持的音频文件")
                return False
            
            # 设置输出目录
            if output_dir:
                output_path = Path(output_dir)
            else:
                output_path = Path(folder_path) / "converted"
            
            output_path.mkdir(exist_ok=True)
            
            total_files = len(audio_files)
            success_count = 0
            
            # 更新转换统计
            self.conversion_stats['total_files'] = total_files
            self.conversion_stats['processed_files'] = 0
            
            # 开始资源监控和进度预测
            if self.use_resource_monitor:
                self.resource_monitor.start_monitoring()
                self.resource_monitor.start_progress_prediction(total_files)
            
            self._status(f"准备转换 {total_files} 个文件...")
            
            # 使用线程池进行并行处理（动态调整并发数）
            base_workers = min(4, os.cpu_count() or 1)
            max_workers = base_workers
            
            with ThreadPoolExecutor(max_workers=max_workers) as executor:
                # 提交所有任务
                futures = []
                for i, file_path in enumerate(audio_files, 1):
                    self._status(f"准备任务 ({i}/{total_files}): {file_path.name}")
                    future = executor.submit(
                        self.convert_single_file, 
                        str(file_path), 
                        output_format, 
                        str(output_path),
                        i
                    )
                    futures.append((i, future, file_path.name))
                
                # 等待完成并收集结果
                for i, future, filename in futures:
                    # 检查资源状态并显示警告
                    if self.use_resource_monitor:
                        warning = self.resource_monitor.get_resource_warning()
                        if warning:
                            self._status(warning)
                    
                    self._status(f"正在处理: {filename}")
                    self._progress(int((i - 1) / total_files * 100))
                    
                    try:
                        if future.result(timeout=300):  # 5分钟超时
                            success_count += 1
                    except Exception as e:
                        self._error(f"转换 {filename} 失败: {str(e)}")
                    
                    # 定期强制垃圾回收
                    if i % 5 == 0:
                        gc.collect()
            
            # 停止资源监控
            if self.use_resource_monitor:
                self.resource_monitor.stop_monitoring()
            
            self._progress(100)
            self._status(f"批量转换完成: {success_count}/{total_files} 个文件成功")
            
            # 最终清理
            gc.collect()
            
            return success_count > 0
            
        except Exception as e:
            self._error(f"批量转换过程中发生错误: {str(e)}")
            return False
        finally:
            # 确保停止监控
            if self.use_resource_monitor:
                self.resource_monitor.stop_monitoring()
    
    def start_conversion(self, input_paths: List[str], output_format: str, 
                        output_dir: str = None, is_batch: bool = False):
        """
        开始转换（异步优化版 + 资源监控）
        
        Args:
            input_paths: 输入路径列表
            output_format: 输出格式
            output_dir: 输出目录
            is_batch: 是否为批量转换模式
        """
        if self.is_converting:
            self._error("已有转换任务正在进行")
            return
        
        def conversion_thread():
            self.is_converting = True
            success = False
            
            # 重置统计
            self.conversion_stats = {
                'start_time': time.time(),
                'processed_files': 0,
                'total_files': 0,
                'current_file_index': 0,
            }
            
            try:
                if is_batch or len(input_paths) > 1:
                    # 批量转换
                    if len(input_paths) == 1 and os.path.isdir(input_paths[0]):
                        success = self.convert_folder(input_paths[0], output_format, output_dir)
                    else:
                        # 多个文件转换 - 使用优化的批量处理
                        total = len(input_paths)
                        success_count = 0
                        
                        # 更新统计
                        self.conversion_stats['total_files'] = total
                        
                        # 开始资源监控和进度预测
                        if self.use_resource_monitor:
                            self.resource_monitor.start_monitoring()
                            self.resource_monitor.start_progress_prediction(total)
                        
                        # 使用线程池处理多个文件
                        base_workers = min(4, os.cpu_count() or 1)
                        max_workers = base_workers
                        
                        with ThreadPoolExecutor(max_workers=max_workers) as executor:
                            futures = []
                            for i, path in enumerate(input_paths, 1):
                                self._status(f"提交任务 ({i}/{total}): {Path(path).name}")
                                self._progress(int((i - 1) / total * 100))
                                future = executor.submit(
                                    self.convert_single_file, 
                                    path, 
                                    output_format, 
                                    output_dir,
                                    i
                                )
                                futures.append((i, future, Path(path).name))
                            
                            # 等待结果
                            for i, future, filename in futures:
                                # 检查资源状态
                                if self.use_resource_monitor:
                                    warning = self.resource_monitor.get_resource_warning()
                                    if warning:
                                        self._status(warning)
                                
                                self._status(f"正在处理: {filename}")
                                try:
                                    if future.result(timeout=300):
                                        success_count += 1
                                        # 更新进度预测
                                        if self.use_resource_monitor:
                                            self.resource_monitor.update_progress(
                                                self.conversion_stats['processed_files']
                                            )
                                except Exception as e:
                                    self._error(f"转换 {filename} 失败: {str(e)}")
                                
                                # 定期清理内存
                                if i % 5 == 0:
                                    gc.collect()
                        
                        # 停止资源监控
                        if self.use_resource_monitor:
                            self.resource_monitor.stop_monitoring()
                        
                        success = success_count > 0
                else:
                    # 单个文件转换
                    success = self.convert_single_file(input_paths[0], output_format, output_dir, 1)
                
                if self.complete_callback:
                    self.complete_callback(success)
                    
            finally:
                self.is_converting = False
                # 停止资源监控
                if self.use_resource_monitor:
                    self.resource_monitor.stop_monitoring()
                # 最终内存清理
                gc.collect()
        
        # 启动转换线程
        thread = threading.Thread(target=conversion_thread, daemon=True)
        thread.start()
    
    def stop_conversion(self):
        """停止转换"""
        self.is_converting = False
        self._status("转换已停止")
    
    def _progress(self, value: int):
        """进度回调"""
        if self.progress_callback:
            self.progress_callback(value)
    
    def _status(self, message: str):
        """状态回调"""
        if self.status_callback:
            self.status_callback(message)
    
    def _error(self, message: str):
        """错误回调"""
        if self.error_callback:
            self.error_callback(message)
    
    @staticmethod
    def get_supported_formats():
        """获取支持的格式列表"""
        return MusicConverter.SUPPORTED_OUTPUT_FORMATS
    
    @staticmethod
    def is_audio_file(file_path: str) -> bool:
        """检查是否为支持的音频文件"""
        ext = Path(file_path).suffix.lower()[1:]
        return ext in MusicConverter.SUPPORTED_INPUT_FORMATS
