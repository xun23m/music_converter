#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
音乐格式转换器 - 主程序入口
支持批量文件夹转换和单个文件转换
"""

import sys
import os

# 设置ffmpeg路径（在导入pydub之前）
from ffmpeg_config import setup_ffmpeg
setup_ffmpeg()

# 应用pydub黑窗口补丁
from ffmpeg_patch import patch_pydub_for_no_window
patch_pydub_for_no_window()

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
