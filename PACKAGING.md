# 音乐格式转换器 - 打包指南

本指南将帮助您创建独立的exe可执行文件，内置ffmpeg，无需用户安装Python或ffmpeg。

## 📋 前置要求

1. **Python 3.8+** - 用于运行打包脚本
2. **PyInstaller** - 用于创建exe文件
3. **ffmpeg** - 音频处理工具（需要下载）

## 🚀 快速开始

### 步骤1: 安装依赖

```bash
# 安装Python依赖
uv pip install -r requirements.txt

# 安装PyInstaller
uv pip install pyinstaller
```

### 步骤2: 下载ffmpeg

有两种方式下载ffmpeg：

#### 方式A: 使用自动下载脚本（推荐）

```bash
python download_ffmpeg.py
```

脚本会自动下载约580MB的ffmpeg文件并解压到正确位置。

#### 方式B: 手动下载

1. 访问: https://github.com/BtbN/FFmpeg-Builds/releases/latest
2. 下载 `ffmpeg-master-latest-win64-gpl.zip`
3. 解压到 `music_converter/ffmpeg/` 目录
4. 确保目录结构如下：
   ```
   music_converter/
   ├── ffmpeg/
   │   ├── bin/
   │   │   ├── ffmpeg.exe
   │   │   ├── ffprobe.exe
   │   │   └── ffplay.exe
   │   └── LICENSE.txt
   ```

### 步骤3: 运行打包脚本

```bash
python build_simple.py
```

### 步骤4: 获取结果

打包完成后，在 `dist/` 目录下会生成：
- `music_converter.exe` - 主程序（约280MB）
- `使用说明.txt` - 使用说明

## 📦 打包选项

### 简化版打包（推荐）

```bash
python build_simple.py
```

使用PyInstaller创建单文件exe，包含：
- 所有Python代码
- ffmpeg二进制文件
- 无需额外依赖

### 完整版打包

```bash
python build.py
```

功能与简化版相同，但会清理旧文件并显示更详细的信息。

## 🔧 技术细节

### ffmpeg配置

程序使用 `ffmpeg_config.py` 模块来定位ffmpeg：

```python
# 开发环境：使用系统ffmpeg
# 打包环境：从临时目录或内置路径获取
```

### PyInstaller配置

```bash
pyinstaller \
  --name=music_converter \
  --onefile \          # 单文件
  --windowed \         # 无控制台窗口
  --add-data=ffmpeg;ffmpeg \  # 包含ffmpeg
  main.py
```

## 📁 项目结构

```
music_converter/
├── main.py                    # 主程序入口
├── converter.py               # 转换核心
├── ui.py                      # GUI界面
├── language_manager.py        # 多语言支持
├── ffmpeg_config.py           # ffmpeg配置
├── download_ffmpeg.py         # ffmpeg下载脚本
├── build_simple.py            # 简化打包脚本
├── build.py                   # 完整打包脚本
├── ffmpeg/                    # ffmpeg目录（不提交到Git）
│   └── bin/
│       ├── ffmpeg.exe
│       ├── ffprobe.exe
│       └── ffplay.exe
├── dist/                      # 打包输出目录
│   └── music_converter.exe
└── requirements.txt
```

## 🎯 使用方法

### 对于开发者

1. 克隆仓库
2. 运行 `python download_ffmpeg.py` 下载ffmpeg
3. 运行 `python build_simple.py` 打包
4. 分发 `dist/music_converter.exe`

### 对于最终用户

1. 下载 `music_converter.exe`
2. 双击运行
3. 拖拽音频文件或文件夹
4. 选择输出格式
5. 开始转换

## ⚠️ 注意事项

1. **文件大小**: 生成的exe约280MB，包含完整ffmpeg
2. **首次运行**: 可能需要几秒钟初始化
3. **系统要求**: Windows 10 或更高版本
4. **磁盘空间**: 确保有足够的空间（建议2GB以上）

## 🐛 常见问题

### Q: 打包后程序无法运行
A: 检查ffmpeg是否正确下载并放置在 `ffmpeg/bin/` 目录

### Q: ffmpeg下载失败
A: 手动下载并解压到正确目录

### Q: 生成的exe太大
A: 这是正常的，因为包含了完整的ffmpeg（约580MB）

## 📝 更新日志

### v1.0 (2026-01-14)
- ✅ 支持独立exe打包
- ✅ 内置ffmpeg支持
- ✅ 自动下载脚本
- ✅ 完整的打包指南

## 🔗 相关链接

- GitHub仓库: https://github.com/xun23m/music_converter
- ffmpeg下载: https://github.com/BtbN/FFmpeg-Builds/releases
- PyInstaller文档: https://pyinstaller.org/en/stable/

---

**打包完成！** 🎉
