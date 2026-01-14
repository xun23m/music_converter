#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
多语言支持管理器
支持中文和英文界面切换
"""

class LanguageManager:
    """语言管理器"""
    
    def __init__(self):
        self.current_language = "zh"  # 默认中文
        self.translations = {
            "zh": {
                # 窗口标题
                "window_title": "音乐格式转换器",
                "title": "🎵 音乐格式转换器",
                
                # 按钮文本
                "btn_select_files": "选择音乐文件",
                "btn_select_folder": "选择音乐文件夹",
                "btn_select_dir": "选择目录",
                "btn_start": "开始转换",
                "btn_stop": "停止",
                "btn_clear": "清空选择",
                "btn_toggle_theme": "切换主题",
                
                # 组标题
                "group_input": "📁 输入选择",
                "group_output": "⚙️ 输出设置",
                "group_control": "🎮 转换控制",
                "group_progress": "📊 进度显示",
                "group_log": "📝 操作日志",
                
                # 标签文本
                "label_format": "输出格式:",
                "label_source_formats": "源文件格式:",
                "label_output_dir": "输出目录:",
                "label_drag_hint": "💡 提示：也可以直接拖拽文件或文件夹到此窗口",
                "label_status_ready": "准备就绪",
                
                # 筛选按钮
                "btn_select_all": "全选",
                "btn_select_none": "清空",
                
                # 日志消息
                "log_selected_files": "选择了 {count} 个文件",
                "log_selected_folder": "选择了文件夹: {path}",
                "log_output_dir_set": "输出目录设置为: {path}",
                "log_conversion_start": "开始转换 -> 格式: {format}",
                "log_source_formats": "源文件格式筛选: {formats}",
                "log_output_dir": "输出目录: {path}",
                "log_mode_batch": "模式: 批量转换",
                "log_mode_single": "模式: 单文件转换",
                "log_user_stop": "用户停止转换",
                "log_cleared": "已清空选择",
                "log_status": "状态: {message}",
                "log_error": "❌ 错误: {message}",
                "log_complete": "✅ 转换完成！",
                "log_complete_warning": "⚠️ 转换完成，但可能存在错误",
                "log_theme_dark": "切换到深色主题",
                "log_theme_light": "切换到浅色主题",
                "log_drag_files": "拖拽选择了 {count} 个音频文件",
                "log_drag_folders": "拖拽选择了 {count} 个文件夹",
                
                # 错误提示
                "error_no_selection": "请先选择要转换的文件或文件夹！",
                "error_unsupported_format": "拖拽的文件格式不支持！",
                "error_conversion_failed": "转换失败",
                
                # 确认对话框
                "confirm_exit_title": "确认退出",
                "confirm_exit_message": "转换正在进行中，确定要退出吗？",
                
                # 完成提示
                "complete_title": "完成",
                "complete_message": "所有转换任务已完成！",
                
                # 拖拽提示文字
                "drag_drop_text": "💡 提示：也可以直接拖拽文件或文件夹到此窗口",
                "drag_enter_text": "🎯 释放以添加文件/文件夹",
                
                # 主题按钮文字
                "theme_dark": "🌙 切换主题",
                "theme_light": "☀️ 切换主题",
                
                # 占位符文本
                "placeholder_output_dir": "留空则使用默认输出目录",
                
                # 托盘菜单
                "tray_show": "显示窗口",
                "tray_status": "状态: 运行中",
                "tray_exit": "退出程序",
                "tray_minimized": "程序已最小化到托盘",
                
                # 菜单栏
                "menu_file": "文件",
                "menu_minimize_to_tray": "最小化到托盘",
                "menu_exit": "退出",
                "menu_language": "语言",
                "menu_theme": "主题",
                "minimize_to_tray": "最小化到托盘",
            },
            
            "en": {
                # 窗口标题
                "window_title": "Music Format Converter",
                "title": "🎵 Music Format Converter",
                
                # 按钮文本
                "btn_select_files": "Select Music Files",
                "btn_select_folder": "Select Music Folder",
                "btn_select_dir": "Select Directory",
                "btn_start": "Start Conversion",
                "btn_stop": "Stop",
                "btn_clear": "Clear Selection",
                "btn_toggle_theme": "Toggle Theme",
                
                # 组标题
                "group_input": "📁 Input Selection",
                "group_output": "⚙️ Output Settings",
                "group_control": "🎮 Conversion Control",
                "group_progress": "📊 Progress Display",
                "group_log": "📝 Operation Log",
                
                # 标签文本
                "label_format": "Output Format:",
                "label_source_formats": "Source Formats:",
                "label_output_dir": "Output Directory:",
                "label_drag_hint": "💡 Tip: You can also drag and drop files or folders to this window",
                "label_status_ready": "Ready",
                
                # 筛选按钮
                "btn_select_all": "Select All",
                "btn_select_none": "Select None",
                
                # 日志消息
                "log_selected_files": "Selected {count} files",
                "log_selected_folder": "Selected folder: {path}",
                "log_output_dir_set": "Output directory set to: {path}",
                "log_conversion_start": "Starting conversion -> Format: {format}",
                "log_source_formats": "Source format filter: {formats}",
                "log_output_dir": "Output directory: {path}",
                "log_mode_batch": "Mode: Batch conversion",
                "log_mode_single": "Mode: Single file conversion",
                "log_user_stop": "User stopped conversion",
                "log_cleared": "Selection cleared",
                "log_status": "Status: {message}",
                "log_error": "❌ Error: {message}",
                "log_complete": "✅ Conversion completed!",
                "log_complete_warning": "⚠️ Conversion completed with warnings",
                "log_theme_dark": "Switched to dark theme",
                "log_theme_light": "Switched to light theme",
                "log_drag_files": "Dragged {count} audio files",
                "log_drag_folders": "Dragged {count} folders",
                
                # 错误提示
                "error_no_selection": "Please select files or folder to convert first!",
                "error_unsupported_format": "Dragged file format is not supported!",
                "error_conversion_failed": "Conversion failed",
                
                # 确认对话框
                "confirm_exit_title": "Confirm Exit",
                "confirm_exit_message": "Conversion is in progress. Are you sure you want to exit?",
                
                # 完成提示
                "complete_title": "Completed",
                "complete_message": "All conversion tasks completed!",
                
                # 拖拽提示文字
                "drag_drop_text": "💡 Tip: You can also drag and drop files or folders to this window",
                "drag_enter_text": "🎯 Release to add files/folders",
                
                # 主题按钮文字
                "theme_dark": "🌙 Toggle Theme",
                "theme_light": "☀️ Toggle Theme",
                
                # 占位符文本
                "placeholder_output_dir": "Leave empty for default output directory",
                
                # 托盘菜单
                "tray_show": "Show Window",
                "tray_status": "Status: Running",
                "tray_exit": "Exit Program",
                "tray_minimized": "Program minimized to tray",
                
                # 菜单栏
                "menu_file": "File",
                "menu_minimize_to_tray": "Minimize to Tray",
                "menu_exit": "Exit",
                "menu_language": "Language",
                "menu_theme": "Theme",
                "minimize_to_tray": "Minimize to Tray",
            }
        }
    
    def set_language(self, language):
        """设置语言"""
        if language in ["zh", "en"]:
            self.current_language = language
            return True
        return False
    
    def get_language(self):
        """获取当前语言"""
        return self.current_language
    
    def toggle_language(self):
        """切换语言"""
        self.current_language = "en" if self.current_language == "zh" else "zh"
        return self.current_language
    
    def get_text(self, key, **kwargs):
        """获取翻译文本"""
        text = self.translations[self.current_language].get(key, key)
        if kwargs:
            try:
                return text.format(**kwargs)
            except:
                return text
        return text
    
    def get_all_texts(self):
        """获取当前语言的所有文本"""
        return self.translations[self.current_language]
    
    def get_supported_languages(self):
        """获取支持的语言列表"""
        return ["zh", "en"]
    
    def get_language_name(self, language):
        """获取语言名称"""
        names = {
            "zh": "中文",
            "en": "English"
        }
        return names.get(language, language)
