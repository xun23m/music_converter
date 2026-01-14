#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
打包脚本 - 使用PyInstaller创建独立exe
"""

import os
import sys
import shutil
import subprocess

def build_exe():
    """打包成独立exe"""
    
    # 检查是否安装了PyInstaller
    try:
        import PyInstaller
    except ImportError:
        print("❌ 未安装PyInstaller，请先安装: pip install pyinstaller")
        return False
    
    print("🚀 开始打包音乐格式转换器...")
    
    # 清理旧的构建文件
    for dir_name in ['build', 'dist', '__pycache__']:
        if os.path.exists(dir_name):
            shutil.rmtree(dir_name)
            print(f"🗑️  清理旧目录: {dir_name}")
    
    # 创建临时ffmpeg目录（用于打包）
    temp_ffmpeg_dir = os.path.join('dist', 'music_converter', 'ffmpeg', 'bin')
    os.makedirs(temp_ffmpeg_dir, exist_ok=True)
    
    # 复制ffmpeg文件
    print("📦 复制ffmpeg文件...")
    system_ffmpeg_dir = r"D:\systemenv\ffmpeg"
    if os.path.exists(system_ffmpeg_dir):
        # 复制整个ffmpeg目录结构
        shutil.copytree(system_ffmpeg_dir, os.path.join('dist', 'music_converter', 'ffmpeg'), 
                       dirs_exist_ok=True)
        print("✅ ffmpeg文件复制完成")
    else:
        print("⚠️  未找到系统ffmpeg，将尝试从PATH加载")
    
    # PyInstaller命令
    pyinstaller_cmd = [
        'pyinstaller',
        '--name=music_converter',           # 输出文件名
        '--onefile',                        # 单个exe文件
        '--windowed',                       # 无控制台窗口
        '--clean',                          # 清理临时文件
        '--noconfirm',                      # 覆盖现有文件
        '--add-data=ffmpeg_config.py;.',    # 添加配置文件
        '--add-data=converter.py;.',        # 添加转换器
        '--add-data=ui.py;.',               # 添加UI
        '--add-data=language_manager.py;.', # 添加语言管理器
        '--add-data=tray_manager.py;.',     # 添加托盘管理器
        '--add-data=main.py;.',             # 添加主程序
        '--add-data=ffmpeg;ffmpeg',         # 添加ffmpeg（如果存在）
        '--icon=assets/icon.ico',           # 图标（如果有）
        'main.py'                           # 入口文件
    ]
    
    # 移除不存在的文件
    valid_files = ['converter.py', 'ui.py', 'language_manager.py', 'tray_manager.py', 'main.py', 'ffmpeg_config.py']
    cmd = ['pyinstaller', '--name=music_converter', '--onefile', '--windowed', '--clean', '--noconfirm']
    
    for file in valid_files:
        if os.path.exists(file):
            cmd.extend(['--add-data', f'{file};.'])
    
    # 添加ffmpeg目录（如果存在）
    if os.path.exists(r"D:\systemenv\ffmpeg"):
        cmd.extend(['--add-data', f'ffmpeg;ffmpeg'])
    
    # 添加图标（如果存在）
    if os.path.exists('assets/icon.ico'):
        cmd.extend(['--icon', 'assets/icon.ico'])
    
    cmd.append('main.py')
    
    print(f"🔧 执行命令: {' '.join(cmd)}")
    
    try:
        # 执行打包命令
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        if result.returncode == 0:
            print("✅ 打包成功！")
            
            # 检查输出文件
            exe_path = os.path.join('dist', 'music_converter.exe')
            if os.path.exists(exe_path):
                file_size = os.path.getsize(exe_path) / (1024 * 1024)  # MB
                print(f"📦 生成文件: {exe_path}")
                print(f"📊 文件大小: {file_size:.2f} MB")
                
                # 创建说明文件
                create_readme_file()
                
                print("\n🎉 打包完成！")
                print(f"📁 可执行文件: {os.path.abspath(exe_path)}")
                print("\n使用方法:")
                print("1. 双击运行 music_converter.exe")
                print("2. 或者拖拽音频文件到exe文件上")
                return True
            else:
                print("❌ 未找到生成的exe文件")
                return False
        else:
            print("❌ 打包失败！")
            print("错误输出:", result.stderr)
            return False
            
    except Exception as e:
        print(f"❌ 打包过程中发生错误: {e}")
        return False

def create_readme_file():
    """创建使用说明文件"""
    readme_content = """音乐格式转换器 - 使用说明

🎵 功能介绍
- 支持单个文件和批量文件夹转换
- 支持9种输入格式: mp3, wav, flac, aac, m4a, ogg, wma, ape, tta
- 支持6种输出格式: mp3, wav, flac, aac, ogg, m4a
- 支持拖拽操作
- 支持深色/浅色主题切换
- 支持中英文语言切换

🚀 使用方法
1. 双击运行 music_converter.exe
2. 选择要转换的文件或文件夹
3. 选择输出格式和目录
4. 点击"开始转换"

🔧 系统要求
- Windows 10 或更高版本
- 无需安装Python或ffmpeg（已内置）

⚠️ 注意事项
- 首次运行可能需要几秒钟初始化
- 转换大文件时请耐心等待
- 确保有足够的磁盘空间

💡 技巧
- 可以直接拖拽文件到程序窗口
- 可以拖拽文件夹批量转换
- 支持多选文件

版本: 1.0
更新日期: 2026-01-14
"""
    
    readme_path = os.path.join('dist', 'README.txt')
    with open(readme_path, 'w', encoding='utf-8') as f:
        f.write(readme_content)
    
    print(f"📝 使用说明已生成: {readme_path}")

if __name__ == '__main__':
    # 确保在music_converter目录下运行
    if os.path.basename(os.getcwd()) != 'music_converter':
        if os.path.exists('music_converter'):
            os.chdir('music_converter')
        else:
            print("❌ 请在music_converter目录下运行此脚本")
            sys.exit(1)
    
    success = build_exe()
    sys.exit(0 if success else 1)
