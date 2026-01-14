#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Pydub黑窗口补丁模块
通过猴子补丁的方式修改pydub的subprocess.Popen调用
"""

import os
import sys
import subprocess
import pydub.audio_segment

def patch_pydub_for_no_window():
    """
    修补pydub库，防止ffmpeg调用时弹出黑窗口
    通过替换pydub内部的subprocess.Popen调用
    """
    
    # 保存原始的from_file方法
    original_from_file = pydub.audio_segment.AudioSegment.from_file
    
    # 保存原始的export方法
    original_export = pydub.audio_segment.AudioSegment.export
    
    def patched_from_file(file, format=None, codec=None, parameters=None, 
                         start_second=None, duration=None, **kwargs):
        """修补后的from_file方法"""
        # 检查是否在打包环境中
        if getattr(sys, 'frozen', False):
            # 在打包环境中，使用我们的补丁
            import pydub.utils
            original_popen = subprocess.Popen
            
            def patched_popen(*args, **kwargs):
                # 检查是否是ffmpeg/ffprobe调用
                if args and len(args) > 0:
                    cmd = args[0]
                    if isinstance(cmd, list) and len(cmd) > 0:
                        cmd_name = cmd[0].lower()
                        if 'ffmpeg' in cmd_name or 'ffprobe' in cmd_name:
                            # 添加隐藏窗口参数
                            if os.name == 'nt':
                                kwargs['creationflags'] = kwargs.get('creationflags', 0) | subprocess.CREATE_NO_WINDOW
                
                return original_popen(*args, **kwargs)
            
            # 临时替换subprocess.Popen
            subprocess.Popen = patched_popen
            pydub.utils.Popen = patched_popen
            
            try:
                result = original_from_file(file, format, codec, parameters, 
                                          start_second, duration, **kwargs)
            finally:
                # 恢复原始的Popen
                subprocess.Popen = original_popen
                pydub.utils.Popen = original_popen
            
            return result
        else:
            # 开发环境，直接调用原始方法
            return original_from_file(file, format, codec, parameters, 
                                    start_second, duration, **kwargs)
    
    def patched_export(self, out_f=None, format='mp3', codec=None, bitrate=None, 
                      parameters=None, tags=None, id3v2_version='4', cover=None):
        """修补后的export方法"""
        # 检查是否在打包环境中
        if getattr(sys, 'frozen', False):
            # 在打包环境中，使用我们的补丁
            import pydub.utils
            original_popen = subprocess.Popen
            
            def patched_popen(*args, **kwargs):
                # 检查是否是ffmpeg/ffprobe调用
                if args and len(args) > 0:
                    cmd = args[0]
                    if isinstance(cmd, list) and len(cmd) > 0:
                        cmd_name = cmd[0].lower()
                        if 'ffmpeg' in cmd_name or 'ffprobe' in cmd_name:
                            # 添加隐藏窗口参数
                            if os.name == 'nt':
                                kwargs['creationflags'] = kwargs.get('creationflags', 0) | subprocess.CREATE_NO_WINDOW
                
                return original_popen(*args, **kwargs)
            
            # 临时替换subprocess.Popen
            subprocess.Popen = patched_popen
            pydub.utils.Popen = patched_popen
            
            try:
                result = original_export(self, out_f, format, codec, bitrate, 
                                       parameters, tags, id3v2_version, cover)
            finally:
                # 恢复原始的Popen
                subprocess.Popen = original_popen
                pydub.utils.Popen = original_popen
            
            return result
        else:
            # 开发环境，直接调用原始方法
            return original_export(self, out_f, format, codec, bitrate, 
                                 parameters, tags, id3v2_version, cover)
    
    # 应用猴子补丁
    pydub.audio_segment.AudioSegment.from_file = staticmethod(patched_from_file)
    pydub.audio_segment.AudioSegment.export = patched_export
    
    print("✅ Pydub黑窗口补丁已应用")

if __name__ == "__main__":
    patch_pydub_for_no_window()
