#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
音乐格式转换器 - 现代化界面
使用PyQt6创建现代化的GUI界面
"""

import os
from pathlib import Path
from PyQt6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
                             QPushButton, QLabel, QLineEdit, QComboBox, 
                             QProgressBar, QTextEdit, QFileDialog, QGroupBox,
                             QFormLayout, QMessageBox)
from PyQt6.QtCore import Qt, QTimer, pyqtSignal, QObject, QMimeData
from PyQt6.QtGui import QFont, QPalette, QColor, QIcon, QDragEnterEvent, QDropEvent

from language_manager import LanguageManager

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
        
        # 创建语言管理器
        self.lang = LanguageManager()
        
        # 创建信号对象
        self.ui_signals = UISignals()
        
        # 托盘管理器（已删除）
        
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
        
        # 启用拖拽功能
        self.setAcceptDrops(True)
        
        # 创建中央窗口
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # 主布局
        main_layout = QVBoxLayout(central_widget)
        main_layout.setSpacing(15)
        main_layout.setContentsMargins(20, 20, 20, 20)
        
        # 标题和控制按钮
        title_layout = QHBoxLayout()
        
        title_label = QLabel("🎵 音乐格式转换器")
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title_font = QFont("Arial", 24, QFont.Weight.Bold)
        title_label.setFont(title_font)
        title_label.setStyleSheet("color: #4a9eff; margin-bottom: 10px;")
        title_layout.addWidget(title_label)
        
        # 语言切换按钮
        self.lang_btn = QPushButton("EN")
        self.lang_btn.setStyleSheet("""
            QPushButton {
                background-color: #2d3748;
                color: #e2e8f0;
                border: 1px solid #4a5568;
                border-radius: 4px;
                padding: 6px 12px;
                font-size: 12px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #4a5568;
            }
        """)
        self.lang_btn.clicked.connect(self.toggle_language)
        self.lang_btn.setFixedWidth(60)
        title_layout.addWidget(self.lang_btn)
        
        # 主题切换按钮
        self.theme_btn = QPushButton("🌙 切换主题")
        self.theme_btn.setStyleSheet("""
            QPushButton {
                background-color: #2d3748;
                color: #e2e8f0;
                border: 1px solid #4a5568;
                border-radius: 4px;
                padding: 6px 12px;
                font-size: 12px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #4a5568;
            }
        """)
        self.theme_btn.clicked.connect(self.toggle_theme)
        self.theme_btn.setFixedWidth(120)
        title_layout.addWidget(self.theme_btn)
        
        main_layout.addLayout(title_layout)
        
        # 当前主题状态
        self.is_dark_theme = True
        
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
        
        # 添加拖拽提示标签
        self.drag_hint = QLabel("💡 提示：也可以直接拖拽文件或文件夹到此窗口")
        self.drag_hint.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.drag_hint.setStyleSheet("""
            QLabel {
                color: #718096;
                font-size: 12px;
                padding: 8px;
                background-color: #1a202c;
                border-radius: 4px;
                border: 1px dashed #4a5568;
            }
        """)
        main_layout.addWidget(self.drag_hint)
        
        # 托盘功能已删除
        
        # 菜单栏已删除（因为包含托盘相关功能）
        
        # 更新UI语言
        self.update_ui_language()
        
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
    
    # 资源监控和进度预测功能已删除
    
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
    
    def apply_light_theme(self):
        """应用浅色主题"""
        palette = QPalette()
        
        # 基础颜色 - 浅色主题
        palette.setColor(QPalette.ColorRole.Window, QColor("#ffffff"))
        palette.setColor(QPalette.ColorRole.WindowText, QColor("#1a202c"))
        palette.setColor(QPalette.ColorRole.Base, QColor("#f7fafc"))
        palette.setColor(QPalette.ColorRole.AlternateBase, QColor("#edf2f7"))
        palette.setColor(QPalette.ColorRole.ToolTipBase, QColor("#ffffff"))
        palette.setColor(QPalette.ColorRole.ToolTipText, QColor("#1a202c"))
        palette.setColor(QPalette.ColorRole.Text, QColor("#1a202c"))
        palette.setColor(QPalette.ColorRole.Button, QColor("#e2e8f0"))
        palette.setColor(QPalette.ColorRole.ButtonText, QColor("#1a202c"))
        palette.setColor(QPalette.ColorRole.BrightText, QColor("#e53e3e"))
        palette.setColor(QPalette.ColorRole.Highlight, QColor("#3182ce"))
        palette.setColor(QPalette.ColorRole.HighlightedText, QColor("#ffffff"))
        
        self.setPalette(palette)
    
    def toggle_theme(self):
        """切换主题"""
        self.is_dark_theme = not self.is_dark_theme
        
        if self.is_dark_theme:
            self.apply_dark_theme()
            self.theme_btn.setText("🌙 切换主题")
            self.theme_btn.setStyleSheet("""
                QPushButton {
                    background-color: #2d3748;
                    color: #e2e8f0;
                    border: 1px solid #4a5568;
                    border-radius: 4px;
                    padding: 6px 12px;
                    font-size: 12px;
                    font-weight: bold;
                }
                QPushButton:hover {
                    background-color: #4a5568;
                }
            """)
            
            # 更新组件样式为深色
            self.update_component_styles(dark=True)
            self.add_log("切换到深色主题")
        else:
            self.apply_light_theme()
            self.theme_btn.setText("☀️ 切换主题")
            self.theme_btn.setStyleSheet("""
                QPushButton {
                    background-color: #e2e8f0;
                    color: #1a202c;
                    border: 1px solid #cbd5e0;
                    border-radius: 4px;
                    padding: 6px 12px;
                    font-size: 12px;
                    font-weight: bold;
                }
                QPushButton:hover {
                    background-color: #cbd5e0;
                }
            """)
            
            # 更新组件样式为浅色
            self.update_component_styles(dark=False)
            self.add_log("切换到浅色主题")
    
    def update_component_styles(self, dark=True):
        """更新组件样式"""
        if dark:
            # 深色主题样式
            bg_color = "#1a202c"
            border_color = "#4a5568"
            text_color = "#e2e8f0"
            log_bg = "#0d1117"
            log_border = "#30363d"
            log_text = "#c9d1d9"
            hint_color = "#718096"
            hint_border = "#4a5568"
        else:
            # 浅色主题样式
            bg_color = "#ffffff"
            border_color = "#cbd5e0"
            text_color = "#1a202c"
            log_bg = "#f7fafc"
            log_border = "#e2e8f0"
            log_text = "#2d3748"
            hint_color = "#4a5568"
            hint_border = "#cbd5e0"
        
        # 更新路径显示
        self.path_display.setStyleSheet(f"""
            QTextEdit {{
                background-color: {bg_color};
                border: 1px solid {border_color};
                border-radius: 4px;
                color: {text_color};
                padding: 8px;
                font-family: Consolas, monospace;
                font-size: 12px;
            }}
        """)
        
        # 更新格式选择框
        self.format_combo.setStyleSheet(f"""
            QComboBox {{
                background-color: {bg_color};
                border: 1px solid {border_color};
                border-radius: 4px;
                color: {text_color};
                padding: 6px;
                min-width: 150px;
            }}
            QComboBox::drop-down {{
                border: none;
            }}
        """)
        
        # 更新输出目录输入框
        self.output_dir_input.setStyleSheet(f"""
            QLineEdit {{
                background-color: {bg_color};
                border: 1px solid {border_color};
                border-radius: 4px;
                color: {text_color};
                padding: 6px;
            }}
        """)
        
        # 更新进度条
        progress_bg = "#1a202c" if dark else "#e2e8f0"
        progress_chunk = "#4a9eff" if dark else "#3182ce"
        self.progress_bar.setStyleSheet(f"""
            QProgressBar {{
                background-color: {progress_bg};
                border: 2px solid {border_color};
                border-radius: 6px;
                text-align: center;
                color: {text_color};
                font-weight: bold;
                height: 25px;
            }}
            QProgressBar::chunk {{
                background-color: {progress_chunk};
                border-radius: 4px;
            }}
        """)
        
        # 更新状态标签
        status_bg = "#1a202c" if dark else "#edf2f7"
        status_color = "#a0aec0" if dark else "#4a5568"
        self.status_label.setStyleSheet(f"""
            QLabel {{
                color: {status_color};
                font-size: 14px;
                padding: 5px;
                background-color: {status_bg};
                border-radius: 4px;
            }}
        """)
        
        # 更新日志框
        self.log_text.setStyleSheet(f"""
            QTextEdit {{
                background-color: {log_bg};
                border: 1px solid {log_border};
                border-radius: 4px;
                color: {log_text};
                padding: 8px;
                font-family: Consolas, monospace;
                font-size: 11px;
            }}
        """)
        
        # 更新拖拽提示
        self.drag_hint.setStyleSheet(f"""
            QLabel {{
                color: {hint_color};
                font-size: 12px;
                padding: 8px;
                background-color: {bg_color};
                border-radius: 4px;
                border: 1px dashed {hint_border};
            }}
        """)
        
        # 更新组标题样式
        for group in self.findChildren(QGroupBox):
            title = group.title()
            if title:
                group.setStyleSheet(f"""
                    QGroupBox {{
                        border: 2px solid {border_color};
                        border-radius: 8px;
                        margin-top: 1ex;
                        padding-top: 15px;
                        font-weight: bold;
                        color: {text_color};
                    }}
                    QGroupBox::title {{
                        subcontrol-origin: margin;
                        left: 10px;
                        padding: 0 5px;
                    }}
                """)
        
        # 更新按钮样式（保持原有颜色，只调整边框）
        for btn in self.findChildren(QPushButton):
            if btn.text() in ["开始转换", "停止", "清空选择", "选择音乐文件", 
                            "选择音乐文件夹", "选择目录", "选择音乐文件", "选择音乐文件夹"]:
                # 保持原有按钮颜色，只更新边框
                pass
    
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
        """开始转换（异步优化版）"""
        if not self.selected_paths:
            self.show_error("请先选择要转换的文件或文件夹！")
            return
        
        output_format = self.format_combo.currentText()
        output_dir = self.output_dir_input.text().strip() or None
        
        # 检查是否为批量模式
        is_batch = len(self.selected_paths) > 1 or (
            len(self.selected_paths) == 1 and os.path.isdir(self.selected_paths[0])
        )
        
        # 显示转换信息
        self.add_log("=" * 50)
        self.add_log(f"开始转换 -> 格式: {output_format}")
        if output_dir:
            self.add_log(f"输出目录: {output_dir}")
        if is_batch:
            self.add_log("模式: 批量转换")
            # 显示预估文件数量
            total_files = self._count_files(self.selected_paths)
            self.add_log(f"预估文件数: {total_files} 个")
        else:
            self.add_log("模式: 单文件转换")
        
        # 更新UI状态
        self.start_btn.setEnabled(False)
        self.stop_btn.setEnabled(True)
        self.format_combo.setEnabled(False)
        self.progress_bar.setValue(0)
        
        # 禁用文件选择按钮，防止在转换过程中修改选择
        for btn in self.findChildren(QPushButton):
            if btn.text() in ["选择音乐文件", "选择音乐文件夹", "选择目录", "清空选择"]:
                btn.setEnabled(False)
        
        # 启动转换
        self.converter.start_conversion(
            self.selected_paths,
            output_format,
            output_dir,
            is_batch
        )
    
    def _count_files(self, paths):
        """计算预估文件数量"""
        count = 0
        for path in paths:
            if os.path.isdir(path):
                for ext in self.converter.SUPPORTED_INPUT_FORMATS:
                    count += len(list(Path(path).glob(f"*.{ext}")))
                    count += len(list(Path(path).glob(f"*.{ext.upper()}")))
            else:
                count += 1
        return count
    
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
        """转换完成回调（优化版）"""
        if success:
            self.add_log("✅ 转换完成！")
            QMessageBox.information(self, "完成", "所有转换任务已完成！")
        else:
            self.add_log("⚠️ 转换完成，但可能存在错误")
        
        self.update_button_states()
        
        # 强制清理内存
        import gc
        gc.collect()
    
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
    
    # 资源监控和进度预测功能已删除
    
    def update_button_states(self):
        """更新按钮状态（优化版）"""
        is_converting = self.converter.is_converting
        has_selection = len(self.selected_paths) > 0
        
        self.start_btn.setEnabled(has_selection and not is_converting)
        self.stop_btn.setEnabled(is_converting)
        self.format_combo.setEnabled(not is_converting)
        
        # 恢复所有按钮状态
        for btn in self.findChildren(QPushButton):
            if btn.text() in ["选择音乐文件", "选择音乐文件夹", "选择目录", "清空选择"]:
                btn.setEnabled(not is_converting)
        
        # 转换完成后清理内存
        if not is_converting:
            import gc
            gc.collect()
    
    def dragEnterEvent(self, event: QDragEnterEvent):
        """拖拽进入事件"""
        # 接受拖拽的文件和文件夹
        if event.mimeData().hasUrls():
            event.acceptProposedAction()
            self.drag_hint.setText("🎯 释放以添加文件/文件夹")
            self.drag_hint.setStyleSheet("""
                QLabel {
                    color: #4a9eff;
                    font-size: 12px;
                    padding: 8px;
                    background-color: #1a202c;
                    border-radius: 4px;
                    border: 1px dashed #4a9eff;
                    font-weight: bold;
                }
            """)
    
    def dragLeaveEvent(self, event):
        """拖拽离开事件"""
        # 恢复提示样式
        self.drag_hint.setText("💡 提示：也可以直接拖拽文件或文件夹到此窗口")
        self.drag_hint.setStyleSheet("""
            QLabel {
                color: #718096;
                font-size: 12px;
                padding: 8px;
                background-color: #1a202c;
                border-radius: 4px;
                border: 1px dashed #4a5568;
            }
        """)
    
    def dropEvent(self, event: QDropEvent):
        """拖拽释放事件"""
        # 恢复提示样式
        self.drag_hint.setText("💡 提示：也可以直接拖拽文件或文件夹到此窗口")
        self.drag_hint.setStyleSheet("""
            QLabel {
                color: #718096;
                font-size: 12px;
                padding: 8px;
                background-color: #1a202c;
                border-radius: 4px;
                border: 1px dashed #4a5568;
            }
        """)
        
        # 获取拖拽的文件路径
        mime_data = event.mimeData()
        if mime_data.hasUrls():
            dropped_paths = [url.toLocalFile() for url in mime_data.urls()]
            
            # 过滤出支持的音频文件
            audio_files = []
            folders = []
            
            for path in dropped_paths:
                if os.path.isdir(path):
                    folders.append(path)
                elif os.path.isfile(path):
                    # 检查文件扩展名
                    ext = os.path.splitext(path)[1][1:].lower()
                    if ext in self.converter.SUPPORTED_INPUT_FORMATS:
                        audio_files.append(path)
            
            # 组合结果
            if folders:
                self.selected_paths = folders
                self.add_log(f"拖拽选择了 {len(folders)} 个文件夹")
            elif audio_files:
                self.selected_paths = audio_files
                self.add_log(f"拖拽选择了 {len(audio_files)} 个音频文件")
            else:
                self.show_error("拖拽的文件格式不支持！")
                return
            
            self.update_path_display()
            self.update_button_states()
            event.acceptProposedAction()
    
    def toggle_language(self):
        """切换语言"""
        current_lang = self.lang.toggle_language()
        
        # 更新语言按钮文本
        if current_lang == "zh":
            self.lang_btn.setText("EN")
        else:
            self.lang_btn.setText("中文")
        
        # 更新所有UI文本
        self.update_ui_language()
        
        # 添加日志
        lang_name = self.lang.get_language_name(current_lang)
        self.add_log(f"Language switched to {lang_name}")
    
    def update_ui_language(self):
        """更新UI语言文本"""
        # 更新窗口标题
        self.setWindowTitle(self.lang.get_text("window_title"))
        
        # 更新标题标签
        title_label = self.findChild(QLabel, "")
        if title_label and title_label.text().startswith("🎵"):
            title_label.setText(self.lang.get_text("title"))
        
        # 更新主题按钮文本
        if self.is_dark_theme:
            self.theme_btn.setText(self.lang.get_text("theme_dark"))
        else:
            self.theme_btn.setText(self.lang.get_text("theme_light"))
        
        # 更新组标题
        for group in self.findChildren(QGroupBox):
            title = group.title()
            if title:
                if "输入" in title or "Input" in title:
                    group.setTitle(self.lang.get_text("group_input"))
                elif "输出" in title or "Output" in title:
                    group.setTitle(self.lang.get_text("group_output"))
                elif "转换" in title or "Conversion" in title:
                    group.setTitle(self.lang.get_text("group_control"))
                elif "进度" in title or "Progress" in title:
                    group.setTitle(self.lang.get_text("group_progress"))
                elif "日志" in title or "Log" in title:
                    group.setTitle(self.lang.get_text("group_log"))
        
        # 更新按钮文本
        for btn in self.findChildren(QPushButton):
            text = btn.text()
            if text in ["选择音乐文件", "Select Music Files"]:
                btn.setText(self.lang.get_text("btn_select_files"))
            elif text in ["选择音乐文件夹", "Select Music Folder"]:
                btn.setText(self.lang.get_text("btn_select_folder"))
            elif text in ["选择目录", "Select Directory"]:
                btn.setText(self.lang.get_text("btn_select_dir"))
            elif text in ["开始转换", "Start Conversion"]:
                btn.setText(self.lang.get_text("btn_start"))
            elif text in ["停止", "Stop"]:
                btn.setText(self.lang.get_text("btn_stop"))
            elif text in ["清空选择", "Clear Selection"]:
                btn.setText(self.lang.get_text("btn_clear"))
        
        # 更新标签文本
        for label in self.findChildren(QLabel):
            text = label.text()
            if text in ["输出格式:", "Output Format:"]:
                label.setText(self.lang.get_text("label_format"))
            elif text in ["输出目录:", "Output Directory:"]:
                label.setText(self.lang.get_text("label_output_dir"))
            elif text.startswith("💡") or text.startswith("Tip:"):
                label.setText(self.lang.get_text("label_drag_hint"))
            elif text in ["准备就绪", "Ready"]:
                label.setText(self.lang.get_text("label_status_ready"))
        
        # 更新占位符文本
        if self.output_dir_input.placeholderText() in ["留空则使用默认输出目录", "Leave empty for default output directory"]:
            self.output_dir_input.setPlaceholderText(self.lang.get_text("placeholder_output_dir"))
        
        # 更新拖拽提示
        if hasattr(self, 'drag_hint'):
            self.drag_hint.setText(self.lang.get_text("drag_drop_text"))
    
    def closeEvent(self, event):
        """关闭窗口事件"""
        if self.converter.is_converting:
            reply = QMessageBox.question(
                self, 
                self.lang.get_text("confirm_exit_title"),
                self.lang.get_text("confirm_exit_message"),
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
