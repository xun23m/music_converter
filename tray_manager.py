#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
系统托盘管理器
提供托盘图标功能，支持最小化到托盘
"""

from PyQt6.QtWidgets import QSystemTrayIcon, QMenu, QMessageBox
from PyQt6.QtGui import QIcon, QAction
from PyQt6.QtCore import QTimer

class TrayManager:
    """系统托盘管理器"""
    
    def __init__(self, main_window, language_manager):
        """初始化托盘管理器"""
        self.main_window = main_window
        self.lang = language_manager
        self.tray_icon = None
        self.tray_menu = None
        self.is_minimized_to_tray = False
        
        # 检查系统是否支持托盘图标
        if not QSystemTrayIcon.isSystemTrayAvailable():
            print("系统不支持托盘图标")
            return
        
        self.init_tray()
    
    def init_tray(self):
        """初始化托盘图标"""
        # 创建托盘图标
        self.tray_icon = QSystemTrayIcon()
        
        # 创建图标
        from PyQt6.QtGui import QPixmap, QPainter, QColor, QFont, QIcon
        from PyQt6.QtCore import Qt
        
        # 创建一个带emoji的图标
        pixmap = QPixmap(32, 32)
        pixmap.fill(Qt.GlobalColor.transparent)
        
        painter = QPainter(pixmap)
        painter.setPen(QColor("#4a9eff"))
        painter.setFont(QFont("Arial", 16, QFont.Weight.Bold))
        painter.drawText(pixmap.rect(), Qt.AlignmentFlag.AlignCenter, "🎵")
        painter.end()
        
        # 设置图标
        icon = QIcon(pixmap)
        self.tray_icon.setIcon(icon)
        
        # 设置窗口图标（确保窗口也有图标）
        if not self.main_window.windowIcon():
            self.main_window.setWindowIcon(icon)
        
        # 创建托盘菜单
        self.tray_menu = QMenu()
        
        # 添加菜单项
        self.show_action = QAction(self.lang.get_text("tray_show"), self.main_window)
        self.show_action.triggered.connect(self.show_main_window)
        self.tray_menu.addAction(self.show_action)
        
        self.tray_menu.addSeparator()
        
        # 状态显示（不可点击）
        status_action = QAction(self.lang.get_text("tray_status"), self.main_window)
        status_action.setEnabled(False)
        self.tray_menu.addAction(status_action)
        
        self.tray_menu.addSeparator()
        
        # 退出动作
        self.quit_action = QAction(self.lang.get_text("tray_exit"), self.main_window)
        self.quit_action.triggered.connect(self.quit_application)
        self.tray_menu.addAction(self.quit_action)
        
        # 设置托盘菜单
        self.tray_icon.setContextMenu(self.tray_menu)
        
        # 连接点击事件
        self.tray_icon.activated.connect(self.on_tray_activated)
        
        # 显示托盘图标
        self.tray_icon.show()
        
        # 设置提示文本
        self.tray_icon.setToolTip(self.lang.get_text("window_title"))
    
    def on_tray_activated(self, reason):
        """托盘图标点击事件"""
        if reason == QSystemTrayIcon.ActivationReason.DoubleClick:
            # 双击显示窗口
            self.show_main_window()
        elif reason == QSystemTrayIcon.ActivationReason.MiddleClick:
            # 中键点击也可以显示窗口
            self.show_main_window()
    
    def show_main_window(self):
        """显示主窗口"""
        if self.main_window.isMinimized():
            self.main_window.showNormal()
        elif self.main_window.isHidden():
            self.main_window.show()
        elif not self.main_window.isVisible():
            self.main_window.show()
        
        self.main_window.activateWindow()
        self.main_window.raise_()
        self.is_minimized_to_tray = False
    
    def hide_main_window(self):
        """隐藏主窗口到托盘"""
        if self.tray_icon and QSystemTrayIcon.isSystemTrayAvailable():
            self.main_window.hide()
            self.is_minimized_to_tray = True
            
            # 显示通知
            self.show_notification(
                self.lang.get_text("window_title"),
                self.lang.get_text("tray_minimized")
            )
    
    def quit_application(self):
        """退出应用程序"""
        if self.main_window.converter.is_converting:
            # 如果正在转换，询问用户
            reply = QMessageBox.question(
                self.main_window,
                self.lang.get_text("confirm_exit_title"),
                self.lang.get_text("confirm_exit_message"),
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
                QMessageBox.StandardButton.No
            )
            
            if reply == QMessageBox.StandardButton.Yes:
                self.main_window.converter.stop_conversion()
                self.cleanup()
                self.main_window.close()
            else:
                return
        else:
            self.cleanup()
            self.main_window.close()
    
    def cleanup(self):
        """清理资源"""
        if self.tray_icon:
            self.tray_icon.hide()
            self.tray_icon = None
    
    def show_notification(self, title, message, timeout=3000):
        """显示系统通知"""
        if self.tray_icon and QSystemTrayIcon.supportsMessages():
            self.tray_icon.showMessage(
                title,
                message,
                QSystemTrayIcon.MessageIcon.Information,
                timeout
            )
    
    def update_language(self):
        """更新托盘菜单语言"""
        if self.tray_menu and self.show_action and self.quit_action:
            self.show_action.setText(self.lang.get_text("tray_show"))
            self.quit_action.setText(self.lang.get_text("tray_exit"))
            self.tray_icon.setToolTip(self.lang.get_text("window_title"))
    
    def is_visible(self):
        """检查是否最小化到托盘"""
        return self.is_minimized_to_tray
    
    def has_tray(self):
        """检查是否有托盘图标"""
        return self.tray_icon is not None
