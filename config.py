"""
B站爬虫配置文件
==============

功能说明：
- 🎯 集中配置：统一管理多个UP主的爬取配置
- 📋 模板化：提供标准的配置模板，便于快速添加新UP主
- ⚙️ 参数控制：为每个UP主设置独立的爬取参数
- 📁 输出管理：自定义每个UP主的输出文件名

配置项说明：
- name: UP主名称（用于显示和日志）
- url: UP主视频页面URL
- max_videos: 最大爬取视频数量
- output_file: 输出文件名前缀

使用方法：
1. 复制示例配置块
2. 修改URL为目标UP主链接
3. 调整爬取数量和输出文件名
4. 运行batch_crawl_multiple.py

作者：GitHub Copilot
更新：2025-08-05
"""

# B站爬虫配置文件
# 你可以在这里添加多个up主的信息

uploader_configs = [
    {
        "name": "示例UP主1",
        "url": "https://space.bilibili.com/93796936/video",
        "max_videos": 50,
        "output_file": "up1_videos"
    },
    {
        "name": "示例UP主2", 
        "url": "https://space.bilibili.com/xxxxxxx/video",  # 替换为真实URL
        "max_videos": 30,
        "output_file": "up2_videos"
    },
    # 在这里添加更多up主...
]

# 全局设置
global_settings = {
    "delay": 2,  # 页面加载等待时间
    "output_format": "both",  # csv, json, both
    "save_directory": "./output/",  # 输出目录
}
