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
    
    def set_callbacks(self, progress_cb: Callable, status_cb: Callable, 
                     error_cb: Callable, complete_cb: Callable):
        """设置回调函数"""
        self.progress_callback = progress_cb
        self.status_callback = status_cb
        self.error_callback = error_cb
        self.complete_callback = complete_cb
    
    def convert_single_file(self, input_path: str, output_format: str, 
                           output_dir: str = None) -> bool:
        """
        转换单个音乐文件（优化版）
        
        Args:
            input_path: 输入文件路径
            output_format: 输出格式（如 'mp3', 'wav'）
            output_dir: 输出目录，如果为None则使用输入文件所在目录
            
        Returns:
            bool: 转换是否成功
        """
        audio = None  # 确保在finally中可以清理
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
            
            self._status(f"正在转换: {input_path.name} -> {output_format}")
            self._progress(0)
            
            # 加载音频文件（使用内存优化）
            try:
                # 使用临时文件减少内存占用（对于大文件）
                file_size = input_path.stat().st_size
                if file_size > 100 * 1024 * 1024:  # 大于100MB
                    self._status(f"正在加载大文件: {input_path.name} ({file_size/(1024*1024):.1f}MB)")
                
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
            self._status(f"转换完成: {output_path.name}")
            
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
                      output_dir: str = None, source_formats: List[str] = None) -> bool:
        """
        转换整个文件夹的音乐文件（优化版）
        
        Args:
            folder_path: 输入文件夹路径
            output_format: 输出格式
            output_dir: 输出目录，如果为None则在原目录创建converted子文件夹
            source_formats: 源文件格式列表，如果为None则处理所有支持的格式
            
        Returns:
            bool: 转换是否成功
        """
        try:
            if not os.path.isdir(folder_path):
                self._error(f"文件夹不存在: {folder_path}")
                return False
            
            # 确定要处理的格式
            target_formats = source_formats if source_formats else self.SUPPORTED_INPUT_FORMATS
            
            # 查找所有支持的音频文件（优化搜索）
            audio_files = []
            for ext in target_formats:
                # 使用大小写不敏感的搜索
                audio_files.extend(Path(folder_path).glob(f"*.{ext}"))
                audio_files.extend(Path(folder_path).glob(f"*.{ext.upper()}"))
            
            if not audio_files:
                self._error(f"文件夹中没有找到匹配的音频文件")
                return False
            
            # 设置输出目录
            if output_dir:
                output_path = Path(output_dir)
            else:
                output_path = Path(folder_path) / "converted"
            
            output_path.mkdir(exist_ok=True)
            
            total_files = len(audio_files)
            success_count = 0
            
            self._status(f"准备转换 {total_files} 个文件...")
            
            # 使用线程池进行并行处理（限制并发数）
            max_workers = min(4, os.cpu_count() or 1)
            with ThreadPoolExecutor(max_workers=max_workers) as executor:
                # 提交所有任务
                futures = []
                for i, file_path in enumerate(audio_files, 1):
                    self._status(f"准备任务 ({i}/{total_files}): {file_path.name}")
                    future = executor.submit(
                        self.convert_single_file, 
                        str(file_path), 
                        output_format, 
                        str(output_path)
                    )
                    futures.append((i, future, file_path.name))
                
                # 等待完成并收集结果
                processed_count = 0
                for i, future, filename in futures:
                    self._status(f"正在处理: {filename}")
                    
                    try:
                        if future.result(timeout=300):  # 5分钟超时
                            success_count += 1
                    except Exception as e:
                        self._error(f"转换 {filename} 失败: {str(e)}")
                    
                    processed_count += 1
                    # 更新进度条：显示已处理文件的进度
                    self._progress(int(processed_count / total_files * 100))
                    
                    # 定期强制垃圾回收
                    if i % 5 == 0:
                        gc.collect()
            
            self._progress(100)
            self._status(f"批量转换完成: {success_count}/{total_files} 个文件成功")
            
            # 最终清理
            gc.collect()
            
            return success_count > 0
            
        except Exception as e:
            self._error(f"批量转换过程中发生错误: {str(e)}")
            return False
    
    def start_conversion(self, input_paths: List[str], output_format: str, 
                        output_dir: str = None, is_batch: bool = False,
                        source_formats: List[str] = None):
        """
        开始转换（异步优化版）
        
        Args:
            input_paths: 输入路径列表
            output_format: 输出格式
            output_dir: 输出目录
            is_batch: 是否为批量转换模式
            source_formats: 源文件格式筛选列表
        """
        if self.is_converting:
            self._error("已有转换任务正在进行")
            return
        
        def conversion_thread():
            self.is_converting = True
            success = False
            
            try:
                if is_batch or len(input_paths) > 1:
                    # 批量转换
                    if len(input_paths) == 1 and os.path.isdir(input_paths[0]):
                        success = self.convert_folder(input_paths[0], output_format, output_dir, source_formats)
                    else:
                        # 多个文件转换 - 使用优化的批量处理
                        # 如果指定了源格式，先进行过滤
                        if source_formats:
                            filtered_paths = []
                            for path in input_paths:
                                ext = Path(path).suffix.lower()[1:]
                                if ext in source_formats:
                                    filtered_paths.append(path)
                            current_paths = filtered_paths
                        else:
                            current_paths = input_paths
                            
                        if not current_paths:
                            self._error("没有找到符合条件的源文件")
                            self.is_converting = False
                            if self.complete_callback:
                                self.complete_callback(False)
                            return

                        total = len(current_paths)
                        success_count = 0
                        
                        # 使用线程池处理多个文件
                        base_workers = min(4, os.cpu_count() or 1)
                        max_workers = base_workers
                        
                        with ThreadPoolExecutor(max_workers=max_workers) as executor:
                            futures = []
                            for i, path in enumerate(current_paths, 1):
                                self._status(f"提交任务 ({i}/{total}): {Path(path).name}")
                                # 这里的进度条不更新，等待任务完成时更新
                                future = executor.submit(
                                    self.convert_single_file, 
                                    path, 
                                    output_format, 
                                    output_dir
                                )
                                futures.append((i, future, Path(path).name))
                            
                            # 等待结果
                            processed_count = 0
                            for i, future, filename in futures:
                                self._status(f"正在处理: {filename}")
                                try:
                                    if future.result(timeout=300):
                                        success_count += 1
                                except Exception as e:
                                    self._error(f"转换 {filename} 失败: {str(e)}")
                                
                                processed_count += 1
                                # 更新进度条：显示已处理文件的进度
                                self._progress(int(processed_count / total * 100))
                                
                                # 定期清理内存
                                if i % 5 == 0:
                                    gc.collect()
                        
                        success = success_count > 0
                else:
                    # 单个文件转换
                    success = self.convert_single_file(input_paths[0], output_format, output_dir)
                
                if self.complete_callback:
                    self.complete_callback(success)
                    
            finally:
                self.is_converting = False
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
