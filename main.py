#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
音乐格式转换器 - 主程序入口
支持批量文件夹转换和单个文件转换
"""

import sys
import os
from PyQt6.QtWidgets import QApplication
from ui import MusicConverterUI
from converter import MusicConverter

def main():
    """主函数"""
    # 创建应用程序
    app = QApplication(sys.argv)
    
    # 设置应用程序样式（现代化深色主题）
    app.setStyle('Fusion')
    
    # 创建转换器核心逻辑
    converter = MusicConverter()
    
    # 创建主界面
    ui = MusicConverterUI(converter)
    ui.show()
    
    # 运行应用程序
    sys.exit(app.exec())

if __name__ == '__main__':
    main()
