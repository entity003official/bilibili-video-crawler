# 🎬 Bilibili Video Crawler

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/)
[![Asyncio](https://img.shields.io/badge/Asyncio-Supported-brightgreen.svg)](https://docs.python.org/3/library/asyncio.html)
[![Selenium](https://img.shields.io/badge/Selenium-4.0+-green.svg)](https://selenium.dev/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](./LICENSE)

一个功能强大的B站UP主视频批量爬取工具，支持**无浏览器异步API爬取**和传统Selenium浏览器爬取两种模式，具备强大的反爬虫能力和多种输出格式。

## ✨ 功能特点

- 🌟 **异步API爬取**: 基于MediaCrawler设计思路，无需Chrome浏览器，速度快，资源占用少
- 🛡️ **强大反爬虫**: 多重User-Agent轮换、智能频率控制、备用方案自动切换
- 🚀 **批量爬取**: 支持批量爬取UP主的所有视频
- 🔐 **自动登录**: 使用Chrome用户数据保持登录状态（Selenium模式）
- 📊 **多种格式**: 支持CSV、JSON等多种输出格式
- 👥 **批量UP主**: 支持同时爬取多个UP主
- 🔄 **智能去重**: 自动去重，避免重复爬取
- ⚙️ **灵活配置**: 支持自定义爬取数量和等待时间
- 🛡️ **安全退出**: 支持Ctrl+C安全中断
- 🎯 **错误处理**: 完善的错误处理和重试机制

## 🎯 推荐使用方式

### 方式1：异步API爬取（推荐⭐）

**优点**: 无需浏览器、速度快、稳定性高、资源占用少

```bash
python spider_bilibili.py
```

**特性**:
- ✅ 无需Chrome浏览器，直接调用B站API
- ✅ 异步并发处理，速度提升显著
- ✅ 智能反爬虫机制，突破频率限制
- ✅ 多重备用方案，确保稳定运行
- ✅ 自动保存为CSV格式，便于后续分析

### 方式2：传统Selenium爬取

**适用场景**: API失效时的备用方案，或需要模拟真实用户行为

```bash
python run_crawler.py
```

## 环境要求

### 异步API模式（推荐）
```bash
pip install aiohttp asyncio beautifulsoup4 pandas
```

### Selenium模式
1. Python 3.8+
2. 安装依赖包：
   ```bash
   pip install selenium beautifulsoup4 requests aiohttp pandas
   ```
3. 安装Chrome浏览器
4. 下载ChromeDriver（或使用自动管理工具）

## 📁 项目文件结构

### 🌟 核心爬虫文件
- `spider_bilibili.py` ⭐ - **主推荐**，异步API爬虫，无浏览器依赖
- `run_crawler.py` - Selenium版本，Chrome浏览器爬虫（备用方案）
- `batch_crawl_multiple.py` - 批量爬取多个UP主
- `bilibili_batch_crawler.py` - Selenium爬虫核心模块

### ⚙️ 配置和工具
- `config.py` - 多UP主配置管理
- `clean_data.py` - 数据清洗和去重工具
- `monitor_progress.py` - 爬取进度监控工具
- `requirements.txt` - 项目依赖包列表

### 🚀 启动脚本
- `run_crawler.bat` - Windows一键启动脚本
- `run_safe_crawler.bat` - 安全模式启动脚本

### 📚 文档文件
- `README.md` - 项目主文档（当前文件）
- `QUICKSTART.md` - 5分钟快速上手指南
- `FILE_GUIDE.md` - 详细的文件功能说明

### 📊 示例数据
- `bilibili_videos_async_*.csv` - 异步爬虫生成的数据文件
- `bilibili_videos.csv` - 通用数据文件

> 💡 **快速开始**: 查看 [FILE_GUIDE.md](FILE_GUIDE.md) 了解每个文件的详细功能

### 🎯 推荐使用优先级
1. **spider_bilibili.py** (首选) - 异步API，高性能
2. **run_crawler.py** (备用) - 浏览器版本，兼容性好
3. **batch_crawl_multiple.py** (批量) - 多UP主同时爬取

### 📊 最新爬取结果示例
最新成功爬取数据（2025-08-05）：
- **总视频数**: 60个
- **总播放量**: 11,151,208次  
- **平均播放量**: 185,853次
- **输出文件**: `bilibili_videos_async_20250805_101559.csv`

## 使用方法

### 方法1：简单使用（推荐新手）

1. 编辑 `run_crawler.py` 文件：
   ```python
   # 修改这些配置
   up_url = "https://space.bilibili.com/你的UP主ID/video"  # 替换为目标UP主
   max_videos = 50  # 要爬取的视频数量
   delay = 3  # 页面加载等待时间
   ```

2. 运行脚本：
   ```bash
   python run_crawler.py
   ```

### 方法2：命令行使用

```bash
# 基本使用
python bilibili_batch_crawler.py -u "https://space.bilibili.com/93796936/video" -n 50

# 完整参数示例
python bilibili_batch_crawler.py \
  --url "https://space.bilibili.com/93796936/video" \
  --max-videos 100 \
  --delay 3 \
  --output "my_videos" \
  --format both
```

参数说明：
- `-u, --url`: UP主视频页面URL（必需）
- `-n, --max-videos`: 最大爬取视频数量（默认50）
- `-d, --delay`: 页面加载等待时间/秒（默认2）
- `-o, --output`: 输出文件名前缀（默认bilibili_videos）
- `-f, --format`: 输出格式 csv/json/both（默认csv）

### 方法3：批量爬取多个UP主

1. 编辑 `config.py` 文件，添加UP主信息：
   ```python
   uploader_configs = [
       {
           "name": "UP主1",
           "url": "https://space.bilibili.com/123456/video",
           "max_videos": 50,
           "output_file": "up1_videos"
       },
       {
           "name": "UP主2",
           "url": "https://space.bilibili.com/789012/video", 
           "max_videos": 30,
           "output_file": "up2_videos"
       }
   ]
   ```

2. 运行批量爬取：
   ```bash
   python batch_crawl_multiple.py
   ```

## 输出格式

### CSV格式
包含以下字段：
- 序号
- BV号
- 视频标题
- 视频链接
- 时长
- 播放量
- 页码

### JSON格式
包含完整的视频信息结构化数据。

## 常见问题

### 1. 爬取失败或获取不到视频
- 检查UP主URL是否正确
- 确认UP主有公开视频
- 增加 `delay` 参数值，给页面更多加载时间
- 检查网络连接

### 2. ChromeDriver相关错误
```bash
# 安装ChromeDriver管理工具
pip install webdriver-manager

# 或手动下载ChromeDriver并加入PATH
```

### 3. 爬取速度慢
- 适当减少 `delay` 参数（但不要太小，避免被反爬虫）
- 确保网络连接良好
- 避免同时运行多个爬虫实例

### 4. 被B站反爬虫限制
- 增加延迟时间
- 不要频繁爬取同一个UP主
- 考虑使用代理IP（需要自行修改代码）

## 注意事项

1. **遵守网站规则**：请合理使用，不要过度频繁地爬取
2. **尊重版权**：爬取的内容仅供学习研究使用
3. **稳定性**：B站页面结构可能会变化，如果爬取失败，可能需要更新选择器
4. **性能**：建议爬取数量不要设置过大，避免长时间占用资源

## 更新日志

- **v2.0 (2025-08-05)**: 🌟 **重大更新**
  - ✅ 新增异步API爬虫，无需Chrome浏览器
  - ✅ 基于MediaCrawler设计思路，性能大幅提升
  - ✅ 智能反爬虫机制，突破B站风控限制
  - ✅ 多重备用方案，确保爬取稳定性
  - ✅ 自动生成时间戳文件名，便于管理
- v1.3: 支持多UP主批量爬取
- v1.2: 增强标题获取和错误处理
- v1.1: 添加批量爬取和多种输出格式
- v1.0: 基础爬取功能

## 技术支持

如果遇到问题，请检查：
1. Python版本是否符合要求
2. 依赖包是否正确安装
3. Chrome浏览器是否正常工作
4. UP主URL格式是否正确

## 免责声明

本工具仅供学习和研究使用，使用者需要遵守相关法律法规和网站服务条款，不得用于商业用途或违法活动。
