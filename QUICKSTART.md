# 🚀 快速开始指南

## 5分钟快速上手B站视频爬虫

### 第一步：安装依赖

```bash
# 只需安装核心依赖（推荐）
pip install aiohttp beautifulsoup4 pandas brotli

# 或安装全部依赖
pip install -r requirements.txt
```

### 第二步：直接运行

```bash
python spider_bilibili.py
```

### 第三步：查看结果

程序会自动生成CSV文件，例如：`bilibili_videos_async_20250805_101559.csv`

## 🎯 自定义UP主

编辑 `spider_bilibili.py` 文件，修改第265行：

```python
up_url = "https://space.bilibili.com/你的UP主ID/video"
```

## 📊 最新测试结果

✅ **测试时间**: 2025-08-05  
✅ **爬取状态**: 成功  
✅ **视频数量**: 60个  
✅ **总播放量**: 11,151,208次  
✅ **运行时间**: ~2分钟  

## 🌟 核心优势

- **无浏览器**: 不需要安装Chrome，直接运行
- **高性能**: 异步处理，速度快
- **强稳定**: 智能反爬虫，成功率高
- **零配置**: 开箱即用，无需复杂设置

## ❓ 常见问题

**Q: 出现"风控校验失败"怎么办？**  
A: 程序会自动等待并重试，通常30秒后恢复正常。

**Q: 如何爬取其他UP主？**  
A: 修改代码中的`up_url`变量即可。

**Q: 输出文件在哪里？**  
A: 在脚本同目录下，文件名包含时间戳。

## 🔧 高级用法

### 批量爬取多个UP主

1. 编辑 `config.py` 添加UP主信息
2. 运行 `python batch_crawl_multiple.py`

### 修改爬取数量

在 `spider_bilibili.py` 中修改：
```python
max_videos = 100  # 改为你想要的数量
```

---

💡 **提示**: 如果遇到问题，查看 [完整文档](README.md) 获取详细说明。
