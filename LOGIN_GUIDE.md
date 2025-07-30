# B站爬虫登录准备指南

## 🚀 快速开始

### 第一步：准备Chrome浏览器登录状态

1. **打开Chrome浏览器**
2. **访问B站并登录**
   - 前往 https://www.bilibili.com
   - 点击右上角"登录"
   - 完成登录过程

3. **测试目标页面**
   - 访问你要爬取的UP主页面
   - 确认可以看到视频列表
   - 例如：https://space.bilibili.com/93796936/upload/video

4. **关闭所有Chrome窗口**
   - ⚠️ 重要：必须完全关闭Chrome浏览器
   - 确保没有Chrome进程在后台运行

### 第二步：运行爬虫

```bash
# 运行登录版爬虫
python spider_logged_browser.py
```

## 🔧 常见问题解决

### 问题1：仍然跳出登录页面
**解决方案：**
- 确认已完全关闭Chrome浏览器
- 重新登录B站并保持登录状态
- 检查用户数据目录是否正确

### 问题2：找不到Chrome用户数据
**解决方案：**
- Windows默认路径：`C:/Users/你的用户名/AppData/Local/Google/Chrome/User Data`
- 手动检查该路径是否存在
- 如果路径不同，请修改代码中的路径

### 问题3：爬取到的视频很少
**解决方案：**
- 检查UP主是否设置了隐私权限
- 确认网络连接稳定
- 增加页面等待时间

### 问题4：Chrome版本兼容性
**解决方案：**
```bash
# 更新webdriver-manager
pip install --upgrade webdriver-manager

# 或手动下载对应版本的ChromeDriver
```

## 📝 使用技巧

### 1. 修改爬取参数
编辑 `spider_logged_browser.py` 文件：
```python
# 修改目标UP主
up_url = "https://space.bilibili.com/你的UP主ID/upload/video"

# 修改最大爬取数量
max_videos = 1000
```

### 2. 启用无头模式
如果不想看到浏览器窗口：
```python
# 在代码中取消这行的注释
options.add_argument('--headless')
```

### 3. 调试模式
如果遇到问题，脚本会自动生成调试文件：
- `debug_page_1.html` - 第一页的HTML源码
- 可以用浏览器打开查看页面结构

## ⚡ 性能优化建议

1. **合理设置等待时间**
   - 网络较慢时增加 `time.sleep()` 时间
   - 网络较快时可以减少等待时间

2. **批量处理**
   - 一次爬取完所有数据
   - 避免频繁启动浏览器

3. **数据去重**
   - 脚本已内置去重功能
   - 避免重复爬取相同视频

## 🛡️ 注意事项

1. **遵守网站规则**
   - 不要过于频繁地请求
   - 尊重网站的robots.txt

2. **数据使用**
   - 仅用于学习和研究目的
   - 不要用于商业用途

3. **隐私保护**
   - 不要分享包含个人信息的调试文件
   - 注意保护账号安全

## 📊 输出文件说明

爬取完成后会生成CSV文件，包含以下字段：
- `序号`: 视频序列号
- `BV号`: B站视频唯一标识
- `视频标题`: 视频名称
- `视频链接`: 完整的视频URL
- `页码`: 来源页面编号

文件名格式：`bilibili_videos_logged_YYYYMMDD_HHMMSS.csv`
