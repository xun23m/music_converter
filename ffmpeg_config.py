#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
FFmpeg配置模块
用于在打包后指定ffmpeg路径
"""

import os
import sys
import tempfile

def get_ffmpeg_path():
    """
    获取ffmpeg可执行文件路径
    在打包后从临时目录或内置路径获取
    """
    if getattr(sys, 'frozen', False):
        # 如果是打包后的exe
        bundle_dir = sys._MEIPASS
        ffmpeg_path = os.path.join(bundle_dir, 'ffmpeg', 'bin', 'ffmpeg.exe')
        
        # 如果内置ffmpeg不存在，尝试其他方式
        if not os.path.exists(ffmpeg_path):
            # 尝试直接从临时目录查找
            temp_dir = tempfile.gettempdir()
            temp_ffmpeg = os.path.join(temp_dir, 'music_converter_ffmpeg.exe')
            
            # 如果已经复制过，直接使用
            if os.path.exists(temp_ffmpeg):
                return temp_ffmpeg
            
            # 尝试从系统PATH查找
            import shutil
            which_ffmpeg = shutil.which('ffmpeg.exe')
            if which_ffmpeg:
                return which_ffmpeg
            
            # 尝试从D:\systemenv\ffmpeg复制
            system_ffmpeg = r"D:\systemenv\ffmpeg\bin\ffmpeg.exe"
            if os.path.exists(system_ffmpeg):
                try:
                    shutil.copy2(system_ffmpeg, temp_ffmpeg)
                    return temp_ffmpeg
                except:
                    pass
            
            # 最后尝试相对路径
            relative_ffmpeg = os.path.join(bundle_dir, 'ffmpeg.exe')
            if os.path.exists(relative_ffmpeg):
                return relative_ffmpeg
            
            return "ffmpeg.exe"
        
        return ffmpeg_path
    else:
        # 开发环境，使用系统ffmpeg
        system_ffmpeg = r"D:\systemenv\ffmpeg\bin\ffmpeg.exe"
        if os.path.exists(system_ffmpeg):
            return system_ffmpeg
        else:
            # 尝试系统PATH
            import shutil
            which_ffmpeg = shutil.which('ffmpeg.exe')
            if which_ffmpeg:
                return which_ffmpeg
            return "ffmpeg.exe"

def setup_ffmpeg():
    """
    设置pydub使用的ffmpeg路径
    """
    from pydub import AudioSegment
    import pydub.utils
    
    ffmpeg_path = get_ffmpeg_path()
    
    # 设置pydub的ffmpeg路径
    if os.path.exists(ffmpeg_path):
        pydub.utils.get_encoder_path = lambda: ffmpeg_path
        pydub.utils.get_prober_path = lambda: ffmpeg_path.replace('ffmpeg.exe', 'ffprobe.exe')
        
        # 设置环境变量
        ffmpeg_dir = os.path.dirname(ffmpeg_path)
        os.environ['PATH'] = ffmpeg_dir + os.pathsep + os.environ.get('PATH', '')
    
    return ffmpeg_path
