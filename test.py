#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
音乐格式转换器 - 功能测试脚本
用于验证核心功能是否正常工作
"""

import sys
import os
from pathlib import Path

# 添加当前目录到Python路径
sys.path.insert(0, os.path.dirname(__file__))

def test_imports():
    """测试导入"""
    print("🔍 测试模块导入...")
    try:
        from converter import MusicConverter
        print("✅ converter 模块导入成功")
        return True
    except ImportError as e:
        print(f"❌ converter 模块导入失败: {e}")
        return False

def test_converter_class():
    """测试转换器类"""
    print("\n🔍 测试转换器类...")
    try:
        from converter import MusicConverter
        
        # 创建实例
        converter = MusicConverter()
        print("✅ 转换器实例创建成功")
        
        # 测试支持的格式
        formats = converter.get_supported_formats()
        print(f"✅ 支持的输出格式: {', '.join(formats)}")
        
        # 测试音频文件检测
        test_files = [
            ("test.mp3", True),
            ("test.wav", True),
            ("test.flac", True),
            ("test.txt", False),
            ("test.unknown", False)
        ]
        
        for filename, expected in test_files:
            result = converter.is_audio_file(filename)
            status = "✅" if result == expected else "❌"
            print(f"{status} 检测 {filename}: {result}")
        
        return True
        
    except Exception as e:
        print(f"❌ 转换器测试失败: {e}")
        return False

def test_ui_import():
    """测试UI模块导入"""
    print("\n🔍 测试UI模块...")
    try:
        from ui import MusicConverterUI
        print("✅ ui 模块导入成功")
        return True
    except ImportError as e:
        print(f"❌ ui 模块导入失败: {e}")
        return False

def test_environment():
    """测试环境"""
    print("\n🔍 测试Python环境...")
    print(f"Python版本: {sys.version}")
    print(f"当前路径: {os.getcwd()}")
    
    # 检查关键依赖
    try:
        import PyQt6
        print("✅ PyQt6 可用")
    except ImportError:
        print("❌ PyQt6 不可用")
        return False
    
    try:
        import pydub
        print("✅ pydub 可用")
    except ImportError:
        print("❌ pydub 不可用")
        return False
    
    return True

def main():
    """主测试函数"""
    print("=" * 50)
    print("🎵 音乐格式转换器 - 环境测试")
    print("=" * 50)
    
    tests = [
        test_environment,
        test_imports,
        test_converter_class,
        test_ui_import
    ]
    
    results = []
    for test in tests:
        try:
            result = test()
            results.append(result)
        except Exception as e:
            print(f"❌ 测试异常: {e}")
            results.append(False)
    
    print("\n" + "=" * 50)
    print("📊 测试结果汇总")
    print("=" * 50)
    
    passed = sum(results)
    total = len(results)
    
    if passed == total:
        print(f"🎉 所有测试通过！({passed}/{total})")
        print("\n✅ 程序可以正常运行！")
        print("\n启动方式:")
        print("  1. 运行: run.bat")
        print("  2. 或者: python main.py")
        return True
    else:
        print(f"⚠️  部分测试失败 ({passed}/{total})")
        print("\n请检查上述错误信息并修复环境问题。")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
