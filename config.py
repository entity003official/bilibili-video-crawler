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
