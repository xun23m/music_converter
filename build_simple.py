#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
简化版打包脚本 - 创建独立exe
"""

import os
import sys
import subprocess
import shutil

def build_exe():
    """打包成独立exe"""
    
    print("=" * 60)
    print("🎵 音乐格式转换器 - 独立exe打包工具")
    print("=" * 60)
    
    # 检查必要文件
    required_files = ['main.py', 'converter.py', 'ui.py', 'language_manager.py', 'ffmpeg_config.py', 'ffmpeg_patch.py']
    for file in required_files:
        if not os.path.exists(file):
            print(f"❌ 缺失必要文件: {file}")
            return False
    
    # 检查ffmpeg
    if not os.path.exists('ffmpeg/bin/ffmpeg.exe'):
        print("❌ 缺失ffmpeg，请先运行: xcopy /E /I \"D:\\systemenv\\ffmpeg\" \"ffmpeg\"")
        return False
    
    print("✅ 所有必要文件检查通过")
    
    # 清理旧文件
    for dir_name in ['build', 'dist']:
        if os.path.exists(dir_name):
            shutil.rmtree(dir_name)
            print(f"🗑️  清理旧目录: {dir_name}")
    
    # 构建PyInstaller命令
    cmd = [
        'pyinstaller',
        '--name=music_converter',
        '--onefile',
        '--windowed',
        '--clean',
        '--noconfirm',
        '--add-data=main.py;.',
        '--add-data=converter.py;.',
        '--add-data=ui.py;.',
        '--add-data=language_manager.py;.',
        '--add-data=ffmpeg_config.py;.',
        '--add-data=ffmpeg_patch.py;.',
        '--add-data=ffmpeg;ffmpeg',
        'main.py'
    ]
    
    print(f"\n🔧 执行打包命令...")
    print(f"命令: {' '.join(cmd)}")
    print()
    
    try:
        # 执行打包
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        if result.returncode != 0:
            print("❌ 打包失败！")
            print("错误信息:", result.stderr)
            return False
        
        # 检查结果
        exe_path = os.path.join('dist', 'music_converter.exe')
        if not os.path.exists(exe_path):
            print("❌ 未找到生成的exe文件")
            return False
        
        # 显示结果
        file_size = os.path.getsize(exe_path) / (1024 * 1024)
        print(f"\n✅ 打包成功！")
        print(f"📁 文件位置: {os.path.abspath(exe_path)}")
        print(f"📊 文件大小: {file_size:.2f} MB")
        
        # 创建说明文件
        create_readme()
        
        print(f"\n🎉 完成！")
        print(f"\n使用方法:")
        print(f"1. 双击运行: {os.path.basename(exe_path)}")
        print(f"2. 拖拽音频文件到程序窗口")
        print(f"3. 选择输出格式，开始转换")
        
        return True
        
    except Exception as e:
        print(f"❌ 打包过程中发生错误: {e}")
        return False

def create_readme():
    """创建使用说明"""
    content = """音乐格式转换器 - 使用说明

🎵 功能特点
• 支持单个文件和批量文件夹转换
• 支持9种输入格式: mp3, wav, flac, aac, m4a, ogg, wma, ape, tta
• 支持6种输出格式: mp3, wav, flac, aac, ogg, m4a
• 支持拖拽操作
• 支持深色/浅色主题
• 支持中英文切换

🚀 使用方法
1. 双击运行 music_converter.exe
2. 选择要转换的文件或文件夹
3. 选择输出格式和目录
4. 点击"开始转换"

💡 小技巧
• 可以直接拖拽文件到程序窗口
• 可以拖拽文件夹批量转换
• 支持多选文件

🔧 系统要求
• Windows 10 或更高版本
• 无需安装Python或ffmpeg（已内置）

⚠️ 注意事项
• 首次运行可能需要几秒钟初始化
• 转换大文件时请耐心等待
• 确保有足够的磁盘空间

版本: 1.0
更新日期: 2026-01-14
"""
    
    readme_path = os.path.join('dist', '使用说明.txt')
    with open(readme_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"📝 使用说明已生成: {readme_path}")

if __name__ == '__main__':
    # 确保在正确目录
    if os.path.basename(os.getcwd()) != 'music_converter':
        if os.path.exists('music_converter'):
            os.chdir('music_converter')
        else:
            print("❌ 请在music_converter目录下运行")
            sys.exit(1)
    
    success = build_exe()
    sys.exit(0 if success else 1)
