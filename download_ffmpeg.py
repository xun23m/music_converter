#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ffmpeg下载脚本
下载并解压ffmpeg到项目目录
"""

import os
import sys
import urllib.request
import zipfile
import shutil

def download_ffmpeg():
    """下载ffmpeg"""
    
    print("=" * 60)
    print("🎵 ffmpeg下载脚本")
    print("=" * 60)
    
    # ffmpeg下载链接
    ffmpeg_url = "https://github.com/BtbN/FFmpeg-Builds/releases/download/latest/ffmpeg-master-latest-win64-gpl.zip"
    
    # 目标目录
    target_dir = "ffmpeg"
    zip_path = "ffmpeg.zip"
    
    # 检查是否已存在
    if os.path.exists(os.path.join(target_dir, "bin", "ffmpeg.exe")):
        print("✅ ffmpeg已存在，无需下载")
        return True
    
    print("🔍 开始下载ffmpeg...")
    print(f"📦 文件较大（约580MB），请耐心等待...")
    print(f"🔗 下载链接: {ffmpeg_url}")
    
    try:
        # 创建临时目录
        os.makedirs(target_dir, exist_ok=True)
        
        # 下载文件
        print("\n📥 正在下载...")
        urllib.request.urlretrieve(ffmpeg_url, zip_path, show_progress)
        
        print("\n📦 正在解压...")
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(target_dir)
        
        # 清理zip文件
        os.remove(zip_path)
        
        # 重新组织目录结构（将解压内容移动到根目录）
        extracted_dir = os.path.join(target_dir, "ffmpeg-master-latest-win64-gpl")
        if os.path.exists(extracted_dir):
            # 移动bin目录
            bin_src = os.path.join(extracted_dir, "bin")
            if os.path.exists(bin_src):
                shutil.move(bin_src, os.path.join(target_dir, "bin"))
            
            # 移动其他重要文件
            for item in ["LICENSE.txt", "README.md"]:
                src = os.path.join(extracted_dir, item)
                if os.path.exists(src):
                    shutil.move(src, os.path.join(target_dir, item))
            
            # 删除临时解压目录
            shutil.rmtree(extracted_dir)
        
        print("\n✅ ffmpeg下载和配置完成！")
        print(f"📁 ffmpeg位置: {os.path.abspath(target_dir)}")
        print("\n现在可以运行打包脚本了:")
        print("  python build_simple.py")
        
        return True
        
    except Exception as e:
        print(f"\n❌ 下载失败: {e}")
        print("\n💡 请手动下载:")
        print(f"1. 访问: {ffmpeg_url}")
        print("2. 下载zip文件")
        print("3. 解压到ffmpeg目录")
        print("4. 确保ffmpeg/bin/ffmpeg.exe存在")
        return False

def show_progress(block_num, block_size, total_size):
    """显示下载进度"""
    downloaded = block_num * block_size
    percent = min(100, downloaded * 100 / total_size)
    bar_length = 40
    filled = int(bar_length * percent / 100)
    bar = "█" * filled + "░" * (bar_length - filled)
    print(f"\r[{bar}] {percent:.1f}% ({downloaded/(1024*1024):.1f}MB/{total_size/(1024*1024):.1f}MB)", end="")

if __name__ == '__main__':
    # 确保在正确目录
    if os.path.basename(os.getcwd()) != 'music_converter':
        if os.path.exists('music_converter'):
            os.chdir('music_converter')
        else:
            print("❌ 请在music_converter目录下运行")
            sys.exit(1)
    
    success = download_ffmpeg()
    sys.exit(0 if success else 1)
