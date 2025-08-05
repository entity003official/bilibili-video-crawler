# 📁 项目文件功能说明

## 🌟 核心爬虫文件

### spider_bilibili.py ⭐ (主推荐)
- **功能**: 异步API爬虫，无浏览器依赖
- **特点**: 高性能、智能反爬、稳定可靠
- **使用**: `python spider_bilibili.py`
- **状态**: ✅ 生产就绪

### run_crawler.py (传统版本)
- **功能**: Selenium浏览器爬虫
- **特点**: 兼容性好，适合API失效时使用
- **使用**: 需要Chrome浏览器
- **状态**: 🔄 备用方案

### batch_crawl_multiple.py
- **功能**: 批量爬取多个UP主
- **特点**: 配置驱动，自动管理输出
- **使用**: 配合config.py使用
- **状态**: ✅ 生产可用

## ⚙️ 配置和工具

### config.py
- **功能**: 多UP主配置管理
- **用途**: 批量爬取的配置文件
- **说明**: 模板化配置，易于扩展

### bilibili_batch_crawler.py
- **功能**: 传统爬虫核心模块
- **用途**: 提供Selenium爬虫功能
- **状态**: 稳定版本

## 📋 数据处理

### clean_data.py
- **功能**: 数据清洗和处理
- **用途**: 清理重复数据，格式标准化
- **特点**: 支持多种数据格式

### monitor_progress.py
- **功能**: 爬取进度监控
- **用途**: 实时显示爬取状态
- **特点**: 可视化进度条

## 📚 文档文件

### README.md
- **功能**: 项目主文档
- **内容**: 完整的使用指南和功能介绍

### QUICKSTART.md
- **功能**: 快速开始指南
- **内容**: 5分钟上手教程

### requirements.txt
- **功能**: 依赖包列表
- **用途**: `pip install -r requirements.txt`

## 🔧 工具脚本

### run_crawler.bat
- **功能**: Windows批处理启动脚本
- **用途**: 双击运行爬虫

### run_safe_crawler.bat
- **功能**: 安全模式启动脚本
- **特点**: 包含错误处理

## 📊 示例数据

### bilibili_videos_async_*.csv
- **功能**: 异步爬虫生成的数据文件
- **格式**: CSV格式，包含完整视频信息
- **用途**: 数据分析和研究

## 🗂️ 版本管理

### .gitignore
- **功能**: Git忽略文件配置
- **内容**: 排除临时文件和敏感数据

### LICENSE
- **功能**: 开源许可证
- **类型**: MIT License

---

## 🎯 推荐使用流程

### 新手用户
1. 安装依赖: `pip install -r requirements.txt`
2. 运行主爬虫: `python spider_bilibili.py`
3. 查看结果: 检查生成的CSV文件

### 高级用户
1. 编辑config.py添加多个UP主
2. 运行批量爬虫: `python batch_crawl_multiple.py`
3. 使用数据处理工具清洗数据

### 开发者
1. 参考README.md了解技术细节
2. 基于核心模块开发自定义功能
3. 贡献代码到GitHub项目

---

**更新时间**: 2025-08-05  
**项目地址**: https://github.com/entity003official/bilibili-video-crawler
