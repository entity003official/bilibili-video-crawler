# 常见问题解答 (FAQ)

## 🤔 使用问题

### Q: 爬虫运行失败，显示"风控"错误？
**A:** 这是B站的反爬虫机制。解决方案：
- 降低爬取频率（增加延迟时间）
- 使用备用方法（程序会自动切换）
- 更换User-Agent或添加Cookie

### Q: 如何修改目标UP主？
**A:** 编辑 `spider_bilibili.py` 文件中的 `up_url` 变量：
```python
up_url = "https://space.bilibili.com/你的目标UID"
```

### Q: 可以同时爬取多个UP主吗？
**A:** 可以使用 `batch_crawl_multiple.py` 脚本，在 `config.py` 中配置多个UP主信息。

### Q: 输出的CSV文件乱码怎么办？
**A:** 文件使用UTF-8编码保存。如果Excel打开乱码，请：
- 使用记事本打开查看
- 或在Excel中选择"数据"->"来自文本"，指定UTF-8编码

## 🛠️ 技术问题

### Q: 需要安装哪些依赖？
**A:** 运行以下命令安装：
```bash
pip install aiohttp beautifulsoup4 pandas brotli
```

### Q: 支持哪些Python版本？
**A:** 推荐Python 3.8+，需要asyncio支持。

### Q: 如何开启调试模式？
**A:** 在 `crawler_config.py` 中设置：
```python
DEFAULT_CONFIG['DEBUG_MODE'] = True
```

## 🚀 性能优化

### Q: 如何提高爬取速度？
**A:** 
- 增加并发数量（注意不要触发风控）
- 使用SSD硬盘
- 确保网络稳定

### Q: 爬取大量数据时内存占用过高？
**A:**
- 分批处理，设置较小的 `max_videos`
- 及时释放无用的数据
- 考虑使用数据库存储

## 📊 数据分析

### Q: 如何分析爬取的数据？
**A:** 可以使用：
- Excel进行基础分析
- Python pandas进行数据处理
- 第三方数据分析工具

### Q: 播放量数据是实时的吗？
**A:** 数据是爬取时的快照，不是实时更新的。

## 🔒 法律声明

### Q: 使用爬虫是否合法？
**A:** 
- 仅用于学习和研究目的
- 不要用于商业用途
- 遵守网站的robots.txt规则
- 尊重数据版权

## 📝 贡献指南

### Q: 如何报告Bug？
**A:** 请在GitHub Issues中报告，包含：
- 错误信息
- 运行环境
- 复现步骤

### Q: 如何贡献代码？
**A:**
1. Fork项目
2. 创建功能分支
3. 提交Pull Request
