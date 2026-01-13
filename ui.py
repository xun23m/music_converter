#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
音乐格式转换器 - 现代化界面
使用PyQt6创建现代化的GUI界面
"""

import os
from PyQt6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
                             QPushButton, QLabel, QLineEdit, QComboBox, 
                             QProgressBar, QTextEdit, QFileDialog, QGroupBox,
                             QFormLayout, QMessageBox, QScrollArea, QFrame)
from PyQt6.QtCore import Qt, QTimer, pyqtSignal, QObject
from PyQt6.QtGui import QFont, QPalette, QColor, QIcon

class UISignals(QObject):
    """用于线程安全的UI信号"""
    progress_signal = pyqtSignal(int)
    status_signal = pyqtSignal(str)
    error_signal = pyqtSignal(str)
    complete_signal = pyqtSignal(bool)

class MusicConverterUI(QMainWindow):
    """主界面类"""
    
    def __init__(self, converter):
        """初始化界面"""
        super().__init__()
        self.converter = converter
        self.selected_paths = []
        self.output_dir = ""
        
        # 创建信号对象
        self.ui_signals = UISignals()
        
        # 连接信号到槽函数
        self.ui_signals.progress_signal.connect(self.update_progress)
        self.ui_signals.status_signal.connect(self.update_status)
        self.ui_signals.error_signal.connect(self.show_error)
        self.ui_signals.complete_signal.connect(self.on_conversion_complete)
        
        # 设置回调（使用信号发射）
        self.converter.set_callbacks(
            lambda v: self.ui_signals.progress_signal.emit(v),
            lambda m: self.ui_signals.status_signal.emit(m),
            lambda e: self.ui_signals.error_signal.emit(e),
            lambda s: self.ui_signals.complete_signal.emit(s)
        )
        
        self.init_ui()
        self.apply_dark_theme()
        
    def init_ui(self):
        """初始化UI组件"""
        self.setWindowTitle("音乐格式转换器")
        self.setGeometry(100, 100, 800, 650)
        
        # 创建中央窗口
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # 主布局
        main_layout = QVBoxLayout(central_widget)
        main_layout.setSpacing(15)
        main_layout.setContentsMargins(20, 20, 20, 20)
        
        # 标题
        title_label = QLabel("🎵 音乐格式转换器")
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title_font = QFont("Arial", 24, QFont.Weight.Bold)
        title_label.setFont(title_font)
        title_label.setStyleSheet("color: #4a9eff; margin-bottom: 10px;")
        main_layout.addWidget(title_label)
        
        # 输入选择区域
        input_group = self.create_input_group()
        main_layout.addWidget(input_group)
        
        # 输出设置区域
        output_group = self.create_output_group()
        main_layout.addWidget(output_group)
        
        # 转换控制区域
        control_group = self.create_control_group()
        main_layout.addWidget(control_group)
        
        # 进度显示区域
        progress_group = self.create_progress_group()
        main_layout.addWidget(progress_group)
        
        # 日志区域
        log_group = self.create_log_group()
        main_layout.addWidget(log_group)
        
        # 按钮状态更新
        self.update_button_states()
        
    def create_input_group(self):
        """创建输入选择区域"""
        group = QGroupBox("📁 输入选择")
        group.setStyleSheet("""
            QGroupBox {
                border: 2px solid #2d3748;
                border-radius: 8px;
                margin-top: 1ex;
                padding-top: 15px;
                font-weight: bold;
                color: #e2e8f0;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 5px;
            }
        """)
        
        layout = QVBoxLayout(group)
        
        # 文件选择按钮
        file_btn = QPushButton("选择音乐文件")
        file_btn.setStyleSheet(self.get_button_style())
        file_btn.clicked.connect(self.select_files)
        layout.addWidget(file_btn)
        
        # 文件夹选择按钮
        folder_btn = QPushButton("选择音乐文件夹")
        folder_btn.setStyleSheet(self.get_button_style())
        folder_btn.clicked.connect(self.select_folder)
        layout.addWidget(folder_btn)
        
        # 显示选择的路径
        self.path_display = QTextEdit()
        self.path_display.setReadOnly(True)
        self.path_display.setMaximumHeight(80)
        self.path_display.setStyleSheet("""
            QTextEdit {
                background-color: #1a202c;
                border: 1px solid #4a5568;
                border-radius: 4px;
                color: #e2e8f0;
                padding: 8px;
                font-family: Consolas, monospace;
                font-size: 12px;
            }
        """)
        layout.addWidget(self.path_display)
        
        return group
    
    def create_output_group(self):
        """创建输出设置区域"""
        group = QGroupBox("⚙️ 输出设置")
        group.setStyleSheet("""
            QGroupBox {
                border: 2px solid #2d3748;
                border-radius: 8px;
                margin-top: 1ex;
                padding-top: 15px;
                font-weight: bold;
                color: #e2e8f0;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 5px;
            }
        """)
        
        layout = QFormLayout(group)
        layout.setSpacing(10)
        
        # 格式选择
        self.format_combo = QComboBox()
        self.format_combo.addItems(self.converter.get_supported_formats())
        self.format_combo.setStyleSheet("""
            QComboBox {
                background-color: #1a202c;
                border: 1px solid #4a5568;
                border-radius: 4px;
                color: #e2e8f0;
                padding: 6px;
                min-width: 150px;
            }
            QComboBox::drop-down {
                border: none;
            }
        """)
        layout.addRow("输出格式:", self.format_combo)
        
        # 输出目录选择
        output_dir_layout = QHBoxLayout()
        self.output_dir_input = QLineEdit()
        self.output_dir_input.setPlaceholderText("留空则使用默认输出目录")
        self.output_dir_input.setStyleSheet("""
            QLineEdit {
                background-color: #1a202c;
                border: 1px solid #4a5568;
                border-radius: 4px;
                color: #e2e8f0;
                padding: 6px;
            }
        """)
        output_dir_layout.addWidget(self.output_dir_input)
        
        output_dir_btn = QPushButton("选择目录")
        output_dir_btn.setStyleSheet(self.get_button_style("small"))
        output_dir_btn.clicked.connect(self.select_output_dir)
        output_dir_layout.addWidget(output_dir_btn)
        
        layout.addRow("输出目录:", output_dir_layout)
        
        return group
    
    def create_control_group(self):
        """创建控制按钮区域"""
        group = QGroupBox("🎮 转换控制")
        group.setStyleSheet("""
            QGroupBox {
                border: 2px solid #2d3748;
                border-radius: 8px;
                margin-top: 1ex;
                padding-top: 15px;
                font-weight: bold;
                color: #e2e8f0;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 5px;
            }
        """)
        
        layout = QHBoxLayout(group)
        
        # 开始转换按钮
        self.start_btn = QPushButton("开始转换")
        self.start_btn.setStyleSheet(self.get_button_style("primary"))
        self.start_btn.clicked.connect(self.start_conversion)
        layout.addWidget(self.start_btn)
        
        # 停止转换按钮
        self.stop_btn = QPushButton("停止")
        self.stop_btn.setStyleSheet(self.get_button_style("danger"))
        self.stop_btn.clicked.connect(self.stop_conversion)
        self.stop_btn.setEnabled(False)
        layout.addWidget(self.stop_btn)
        
        # 清空按钮
        clear_btn = QPushButton("清空选择")
        clear_btn.setStyleSheet(self.get_button_style())
        clear_btn.clicked.connect(self.clear_selection)
        layout.addWidget(clear_btn)
        
        return group
    
    def create_progress_group(self):
        """创建进度显示区域"""
        group = QGroupBox("📊 进度显示")
        group.setStyleSheet("""
            QGroupBox {
                border: 2px solid #2d3748;
                border-radius: 8px;
                margin-top: 1ex;
                padding-top: 15px;
                font-weight: bold;
                color: #e2e8f0;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 5px;
            }
        """)
        
        layout = QVBoxLayout(group)
        
        # 进度条
        self.progress_bar = QProgressBar()
        self.progress_bar.setRange(0, 100)
        self.progress_bar.setValue(0)
        self.progress_bar.setStyleSheet("""
            QProgressBar {
                background-color: #1a202c;
                border: 2px solid #4a5568;
                border-radius: 6px;
                text-align: center;
                color: #e2e8f0;
                font-weight: bold;
                height: 25px;
            }
            QProgressBar::chunk {
                background-color: #4a9eff;
                border-radius: 4px;
            }
        """)
        layout.addWidget(self.progress_bar)
        
        # 状态标签
        self.status_label = QLabel("准备就绪")
        self.status_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.status_label.setStyleSheet("""
            QLabel {
                color: #a0aec0;
                font-size: 14px;
                padding: 5px;
                background-color: #1a202c;
                border-radius: 4px;
            }
        """)
        layout.addWidget(self.status_label)
        
        return group
    
    def create_log_group(self):
        """创建日志区域"""
        group = QGroupBox("📝 操作日志")
        group.setStyleSheet("""
            QGroupBox {
                border: 2px solid #2d3748;
                border-radius: 8px;
                margin-top: 1ex;
                padding-top: 15px;
                font-weight: bold;
                color: #e2e8f0;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 5px;
            }
        """)
        
        layout = QVBoxLayout(group)
        
        self.log_text = QTextEdit()
        self.log_text.setReadOnly(True)
        self.log_text.setMaximumHeight(120)
        self.log_text.setStyleSheet("""
            QTextEdit {
                background-color: #0d1117;
                border: 1px solid #30363d;
                border-radius: 4px;
                color: #c9d1d9;
                padding: 8px;
                font-family: Consolas, monospace;
                font-size: 11px;
            }
        """)
        layout.addWidget(self.log_text)
        
        return group
    
    def apply_dark_theme(self):
        """应用深色主题"""
        palette = QPalette()
        
        # 基础颜色
        palette.setColor(QPalette.ColorRole.Window, QColor("#1a202c"))
        palette.setColor(QPalette.ColorRole.WindowText, QColor("#e2e8f0"))
        palette.setColor(QPalette.ColorRole.Base, QColor("#0d1117"))
        palette.setColor(QPalette.ColorRole.AlternateBase, QColor("#1a202c"))
        palette.setColor(QPalette.ColorRole.ToolTipBase, QColor("#2d3748"))
        palette.setColor(QPalette.ColorRole.ToolTipText, QColor("#e2e8f0"))
        palette.setColor(QPalette.ColorRole.Text, QColor("#e2e8f0"))
        palette.setColor(QPalette.ColorRole.Button, QColor("#2d3748"))
        palette.setColor(QPalette.ColorRole.ButtonText, QColor("#e2e8f0"))
        palette.setColor(QPalette.ColorRole.BrightText, QColor("#fc8181"))
        palette.setColor(QPalette.ColorRole.Highlight, QColor("#4a9eff"))
        palette.setColor(QPalette.ColorRole.HighlightedText, QColor("#ffffff"))
        
        self.setPalette(palette)
    
    def get_button_style(self, style_type="normal"):
        """获取按钮样式"""
        base_style = """
            QPushButton {
                padding: 10px 20px;
                border-radius: 6px;
                font-weight: bold;
                font-size: 14px;
                border: none;
            }
            QPushButton:disabled {
                opacity: 0.5;
            }
        """
        
        if style_type == "primary":
            return base_style + """
                QPushButton {
                    background-color: #4a9eff;
                    color: white;
                }
                QPushButton:hover {
                    background-color: #3a8eef;
                    font-weight: bold;
                }
            """
        elif style_type == "danger":
            return base_style + """
                QPushButton {
                    background-color: #f56565;
                    color: white;
                }
                QPushButton:hover {
                    background-color: #e53e3e;
                    font-weight: bold;
                }
            """
        elif style_type == "small":
            return base_style + """
                QPushButton {
                    padding: 6px 12px;
                    font-size: 12px;
                    background-color: #4a5568;
                    color: white;
                }
                QPushButton:hover {
                    background-color: #5a6578;
                    font-weight: bold;
                }
            """
        else:
            return base_style + """
                QPushButton {
                    background-color: #4a5568;
                    color: white;
                }
                QPushButton:hover {
                    background-color: #5a6578;
                    font-weight: bold;
                }
            """
    
    def select_files(self):
        """选择音乐文件"""
        files, _ = QFileDialog.getOpenFileNames(
            self,
            "选择音乐文件",
            "",
            f"音频文件 ({' '.join(['*.' + ext for ext in self.converter.SUPPORTED_INPUT_FORMATS])})"
        )
        
        if files:
            self.selected_paths = files
            self.update_path_display()
            self.add_log(f"选择了 {len(files)} 个文件")
            self.update_button_states()
    
    def select_folder(self):
        """选择文件夹"""
        folder = QFileDialog.getExistingDirectory(
            self,
            "选择音乐文件夹"
        )
        
        if folder:
            self.selected_paths = [folder]
            self.update_path_display()
            self.add_log(f"选择了文件夹: {folder}")
            self.update_button_states()
    
    def select_output_dir(self):
        """选择输出目录"""
        folder = QFileDialog.getExistingDirectory(
            self,
            "选择输出目录"
        )
        
        if folder:
            self.output_dir = folder
            self.output_dir_input.setText(folder)
            self.add_log(f"输出目录设置为: {folder}")
    
    def update_path_display(self):
        """更新路径显示"""
        if not self.selected_paths:
            self.path_display.clear()
            return
        
        text = "\n".join(self.selected_paths)
        self.path_display.setText(text)
    
    def start_conversion(self):
        """开始转换"""
        if not self.selected_paths:
            self.show_error("请先选择要转换的文件或文件夹！")
            return
        
        output_format = self.format_combo.currentText()
        output_dir = self.output_dir_input.text().strip() or None
        
        # 检查是否为批量模式
        is_batch = len(self.selected_paths) > 1 or (
            len(self.selected_paths) == 1 and os.path.isdir(self.selected_paths[0])
        )
        
        self.add_log("=" * 50)
        self.add_log(f"开始转换 -> 格式: {output_format}")
        if output_dir:
            self.add_log(f"输出目录: {output_dir}")
        if is_batch:
            self.add_log("模式: 批量转换")
        else:
            self.add_log("模式: 单文件转换")
        
        # 更新UI状态
        self.start_btn.setEnabled(False)
        self.stop_btn.setEnabled(True)
        self.format_combo.setEnabled(False)
        self.progress_bar.setValue(0)
        
        # 启动转换
        self.converter.start_conversion(
            self.selected_paths,
            output_format,
            output_dir,
            is_batch
        )
    
    def stop_conversion(self):
        """停止转换"""
        self.converter.stop_conversion()
        self.add_log("用户停止转换")
        self.update_button_states()
    
    def clear_selection(self):
        """清空选择"""
        self.selected_paths = []
        self.output_dir = ""
        self.output_dir_input.clear()
        self.path_display.clear()
        self.progress_bar.setValue(0)
        self.status_label.setText("准备就绪")
        self.add_log("已清空选择")
        self.update_button_states()
    
    def update_progress(self, value):
        """更新进度条"""
        self.progress_bar.setValue(value)
    
    def update_status(self, message):
        """更新状态"""
        self.status_label.setText(message)
        self.add_log(f"状态: {message}")
    
    def show_error(self, message):
        """显示错误"""
        self.add_log(f"❌ 错误: {message}")
        QMessageBox.critical(self, "错误", message)
    
    def on_conversion_complete(self, success):
        """转换完成回调"""
        if success:
            self.add_log("✅ 转换完成！")
            QMessageBox.information(self, "完成", "所有转换任务已完成！")
        else:
            self.add_log("⚠️ 转换完成，但可能存在错误")
        
        self.update_button_states()
    
    def add_log(self, message):
        """添加日志"""
        from datetime import datetime
        timestamp = datetime.now().strftime("%H:%M:%S")
        log_line = f"[{timestamp}] {message}"
        self.log_text.append(log_line)
        # 滚动到底部
        self.log_text.verticalScrollBar().setValue(
            self.log_text.verticalScrollBar().maximum()
        )
    
    def update_button_states(self):
        """更新按钮状态"""
        is_converting = self.converter.is_converting
        has_selection = len(self.selected_paths) > 0
        
        self.start_btn.setEnabled(has_selection and not is_converting)
        self.stop_btn.setEnabled(is_converting)
        self.format_combo.setEnabled(not is_converting)
        
        # 如果正在转换，禁用文件选择按钮
        for btn in self.findChildren(QPushButton):
            if btn.text() in ["选择音乐文件", "选择音乐文件夹", "选择目录", "清空选择"]:
                btn.setEnabled(not is_converting)
    
    def closeEvent(self, event):
        """关闭窗口事件"""
        if self.converter.is_converting:
            reply = QMessageBox.question(
                self, "确认退出",
                "转换正在进行中，确定要退出吗？",
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
                QMessageBox.StandardButton.No
            )
            
            if reply == QMessageBox.StandardButton.Yes:
                self.converter.stop_conversion()
                event.accept()
            else:
                event.ignore()
        else:
            event.accept()
