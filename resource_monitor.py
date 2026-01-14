#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
资源监控器
实时监控系统资源，自动调整并发数
"""

import psutil
import threading
import time
from typing import Callable, Optional

class ResourceMonitor:
    """资源监控器"""
    
    def __init__(self):
        """初始化资源监控器"""
        self.monitoring = False
        self.monitor_thread = None
        self.callbacks = {}
        
        # 资源阈值配置
        self.thresholds = {
            'cpu_percent': 85,      # CPU使用率阈值
            'memory_percent': 80,   # 内存使用率阈值
            'disk_percent': 90,     # 磁盘使用率阈值
        }
        
        # 当前资源状态
        self.current_status = {
            'cpu_percent': 0,
            'memory_percent': 0,
            'disk_percent': 0,
            'available_workers': 4,  # 推荐并发数
            'status': 'normal',      # normal, warning, critical
        }
        
        # 历史数据（用于进度预测）
        self.history = {
            'processing_times': [],  # 处理时间历史
            'file_sizes': [],        # 文件大小历史
            'memory_usage': [],      # 内存使用历史
        }
        
        # 进度预测数据
        self.prediction_data = {
            'start_time': None,
            'processed_files': 0,
            'total_files': 0,
            'avg_time_per_file': 0,
            'estimated_remaining': 0,
        }
    
    def set_callback(self, event_type: str, callback: Callable):
        """设置回调函数
        
        Args:
            event_type: 事件类型 ('resource_status', 'progress_prediction', 'worker_adjustment')
            callback: 回调函数
        """
        self.callbacks[event_type] = callback
    
    def start_monitoring(self):
        """开始监控"""
        if self.monitoring:
            return
        
        self.monitoring = True
        self.monitor_thread = threading.Thread(target=self._monitor_loop, daemon=True)
        self.monitor_thread.start()
    
    def stop_monitoring(self):
        """停止监控"""
        self.monitoring = False
        if self.monitor_thread:
            self.monitor_thread.join(timeout=2)
    
    def _monitor_loop(self):
        """监控循环"""
        while self.monitoring:
            try:
                # 获取系统资源
                cpu_percent = psutil.cpu_percent(interval=1)
                memory = psutil.virtual_memory()
                disk = psutil.disk_usage('/')
                
                # 更新状态
                self.current_status.update({
                    'cpu_percent': cpu_percent,
                    'memory_percent': memory.percent,
                    'disk_percent': disk.percent,
                })
                
                # 计算推荐并发数
                self._calculate_optimal_workers()
                
                # 检查资源状态
                self._check_resource_status()
                
                # 触发资源状态回调
                if 'resource_status' in self.callbacks:
                    self.callbacks['resource_status'](self.current_status.copy())
                
                # 更新进度预测
                self._update_progress_prediction()
                
                # 检查是否需要调整并发数
                self._check_worker_adjustment()
                
            except Exception as e:
                print(f"资源监控错误: {e}")
            
            time.sleep(2)  # 每2秒检查一次
    
    def _calculate_optimal_workers(self):
        """计算最优并发数"""
        cpu = self.current_status['cpu_percent']
        memory = self.current_status['memory_percent']
        
        # 基础并发数
        base_workers = min(4, psutil.cpu_count() or 1)
        
        # 根据CPU使用率调整
        if cpu > 90:
            cpu_workers = 1
        elif cpu > 75:
            cpu_workers = 2
        elif cpu > 60:
            cpu_workers = 3
        else:
            cpu_workers = base_workers
        
        # 根据内存使用率调整
        if memory > 90:
            memory_workers = 1
        elif memory > 80:
            memory_workers = 2
        elif memory > 70:
            memory_workers = 3
        else:
            memory_workers = base_workers
        
        # 取最小值作为安全策略
        optimal_workers = min(cpu_workers, memory_workers, base_workers)
        
        self.current_status['available_workers'] = optimal_workers
    
    def _check_resource_status(self):
        """检查资源状态"""
        cpu = self.current_status['cpu_percent']
        memory = self.current_status['memory_percent']
        disk = self.current_status['disk_percent']
        
        # 检查是否达到临界值
        if cpu > self.thresholds['cpu_percent'] or \
           memory > self.thresholds['memory_percent'] or \
           disk > self.thresholds['disk_percent']:
            self.current_status['status'] = 'critical'
        # 检查是否达到警告值
        elif cpu > self.thresholds['cpu_percent'] - 10 or \
             memory > self.thresholds['memory_percent'] - 10 or \
             disk > self.thresholds['disk_percent'] - 10:
            self.current_status['status'] = 'warning'
        else:
            self.current_status['status'] = 'normal'
    
    def _check_worker_adjustment(self):
        """检查是否需要调整并发数"""
        if 'worker_adjustment' in self.callbacks:
            # 如果状态为critical，立即通知调整
            if self.current_status['status'] == 'critical':
                self.callbacks['worker_adjustment'](self.current_status.copy())
    
    def start_progress_prediction(self, total_files: int):
        """开始进度预测
        
        Args:
            total_files: 总文件数
        """
        self.prediction_data.update({
            'start_time': time.time(),
            'processed_files': 0,
            'total_files': total_files,
            'avg_time_per_file': 0,
            'estimated_remaining': 0,
        })
    
    def update_progress(self, processed_files: int, file_size: float = 0):
        """更新进度
        
        Args:
            processed_files: 已处理文件数
            file_size: 当前文件大小（MB）
        """
        if self.prediction_data['start_time'] is None:
            return
        
        self.prediction_data['processed_files'] = processed_files
        
        # 记录历史数据
        if file_size > 0:
            self.history['file_sizes'].append(file_size)
        
        # 计算平均处理时间
        elapsed_time = time.time() - self.prediction_data['start_time']
        if processed_files > 0:
            avg_time = elapsed_time / processed_files
            self.prediction_data['avg_time_per_file'] = avg_time
            
            # 预测剩余时间
            remaining_files = self.prediction_data['total_files'] - processed_files
            estimated_remaining = avg_time * remaining_files
            self.prediction_data['estimated_remaining'] = estimated_remaining
            
            # 记录处理时间历史
            self.history['processing_times'].append(avg_time)
    
    def _update_progress_prediction(self):
        """更新进度预测"""
        if self.prediction_data['start_time'] is None:
            return
        
        if 'progress_prediction' in self.callbacks:
            prediction = {
                'processed': self.prediction_data['processed_files'],
                'total': self.prediction_data['total_files'],
                'avg_time': self.prediction_data['avg_time_per_file'],
                'remaining_time': self.prediction_data['estimated_remaining'],
                'progress_percent': 0,
            }
            
            if self.prediction_data['total_files'] > 0:
                prediction['progress_percent'] = (
                    self.prediction_data['processed_files'] / 
                    self.prediction_data['total_files'] * 100
                )
            
            self.callbacks['progress_prediction'](prediction)
    
    def get_prediction_text(self) -> str:
        """获取预测文本"""
        if self.prediction_data['start_time'] is None:
            return ""
        
        remaining = self.prediction_data['estimated_remaining']
        if remaining <= 0:
            return ""
        
        # 格式化时间
        if remaining < 60:
            return f"预计剩余时间: {remaining:.0f}秒"
        elif remaining < 3600:
            minutes = int(remaining // 60)
            seconds = int(remaining % 60)
            return f"预计剩余时间: {minutes}分{seconds}秒"
        else:
            hours = int(remaining // 3600)
            minutes = int((remaining % 3600) // 60)
            return f"预计剩余时间: {hours}小时{minutes}分"
    
    def get_resource_warning(self) -> Optional[str]:
        """获取资源警告"""
        status = self.current_status['status']
        
        if status == 'critical':
            cpu = self.current_status['cpu_percent']
            memory = self.current_status['memory_percent']
            return f"⚠️ 资源紧张! CPU: {cpu:.1f}%, 内存: {memory:.1f}%"
        elif status == 'warning':
            cpu = self.current_status['cpu_percent']
            memory = self.current_status['memory_percent']
            return f"⚡ 资源警告: CPU: {cpu:.1f}%, 内存: {memory:.1f}%"
        
        return None
    
    def get_optimal_workers_text(self) -> str:
        """获取最优并发数文本"""
        workers = self.current_status['available_workers']
        return f"当前推荐并发数: {workers}"
