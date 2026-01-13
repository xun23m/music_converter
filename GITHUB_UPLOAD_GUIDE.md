# GitHub 上传指南

本指南将帮助您将音乐格式转换器项目上传到GitHub。

## 前置要求

1. **Git已安装** - 检查版本：`git --version`
2. **GitHub账号** - 没有请注册：https://github.com/join
3. **GitHub Access Token** - 用于认证（推荐）或使用SSH密钥

## 步骤1：创建GitHub仓库

### 方法A：通过GitHub网站（推荐）
1. 登录GitHub
2. 点击右上角 "+" → "New repository"
3. 填写仓库信息：
   - **Repository name**: `music-converter`
   - **Description**: "Modern music format converter with GUI - MP3, WAV, FLAC, AAC, OGG, M4A"
   - **Public/Private**: 选择Public（推荐）
   - **Initialize with README**: 不勾选（我们已有）
   - **Add .gitignore**: 不勾选（我们已有）
   - **Choose license**: 不勾选（我们已有）
4. 点击 "Create repository"

### 方法B：使用GitHub CLI
```bash
# 安装GitHub CLI（如果未安装）
# Windows: winget install --id GitHub.cli

# 登录
gh auth login

# 创建仓库
gh repo create music-converter --public --description "Modern music format converter with GUI"
```

## 步骤2：配置远程仓库

在项目目录中执行以下命令：

```bash
cd music_converter

# 设置远程仓库（将YOUR_USERNAME替换为您的GitHub用户名）
git remote add origin https://github.com/YOUR_USERNAME/music-converter.git

# 如果使用SSH（推荐）
# git remote add origin git@github.com:YOUR_USERNAME/music-converter.git

# 验证远程配置
git remote -v
```

## 步骤3：推送代码到GitHub

```bash
# 推送所有代码到GitHub
git push -u origin master

# 如果遇到权限问题，使用Personal Access Token
# 当提示输入密码时，输入您的Token
```

## 步骤4：验证上传

1. 刷新GitHub仓库页面
2. 您应该能看到所有文件：
   - ✅ main.py
   - ✅ converter.py
   - ✅ ui.py
   - ✅ requirements.txt
   - ✅ README.md (中文)
   - ✅ README_EN.md (英文)
   - ✅ LICENSE
   - ✅ .gitignore
   - ✅ run.bat & start.bat
   - ✅ test.py
   - ✅ 快速开始.md

## 步骤5：设置仓库信息（可选）

### 添加仓库主题
在GitHub仓库页面：
1. 点击 "Settings" → "Topics"
2. 添加标签：`python`, `pyqt6`, `music-converter`, `audio`, `gui`

### 设置默认分支
```bash
git branch -M main  # 如果想用main而不是master
git push -u origin main
```

## 常见问题

### 问题1：Authentication failed
**解决方案**：
1. 生成Personal Access Token：
   - GitHub → Settings → Developer settings → Personal access tokens → Tokens (classic)
   - 点击 "Generate new token"
   - 选择权限：`repo` (全部仓库权限)
   - 复制生成的Token

2. 使用Token认证：
   ```bash
   git remote set-url origin https://YOUR_USERNAME:YOUR_TOKEN@github.com/YOUR_USERNAME/music-converter.git
   git push -u origin master
   ```

### 问题2：Remote already exists
**解决方案**：
```bash
# 查看现有远程
git remote -v

# 如果URL错误，先删除再添加
git remote remove origin
git remote add origin https://github.com/YOUR_USERNAME/music-converter.git
```

### 问题3：Push rejected
**解决方案**：
```bash
# 如果远程有本地没有的提交（比如创建了README）
git pull origin master --allow-unrelated-histories

# 解决冲突后重新推送
git push -u origin master
```

## 完成后的检查清单

- [ ] 代码已成功推送到GitHub
- [ ] README.md正确显示（包括图片和格式）
- [ ] LICENSE文件存在
- [ ] .gitignore正确配置
- [ ] 可以克隆仓库到新位置测试
- [ ] 仓库描述和主题已设置

## 测试上传结果

```bash
# 在临时目录测试克隆
cd /tmp
git clone https://github.com/YOUR_USERNAME/music-converter.git
cd music-converter
ls -la
```

## 后续维护

### 发布新版本
```bash
# 添加新文件
git add .

# 提交更改
git commit -m "描述您的更改"

# 推送到GitHub
git push origin master

# 创建版本标签（可选）
git tag v1.1.0
git push origin v1.1.0
```

### 更新README
- 修改 README.md 或 README_EN.md
- 提交并推送更改
- GitHub会自动更新显示

## 获取帮助

如果遇到问题：
1. 查看GitHub帮助文档：https://docs.github.com
2. 使用命令：`git status` 查看当前状态
3. 使用命令：`git log` 查看提交历史
4. 检查网络连接和权限设置

---

**祝您上传成功！** 🎉
