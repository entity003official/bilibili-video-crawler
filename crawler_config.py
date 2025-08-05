"""
B站爬虫配置文件
================

包含所有可配置的参数和设置
"""

# 爬虫基础配置
DEFAULT_CONFIG = {
    # 请求参数
    'MAX_VIDEOS': 100,              # 最大爬取视频数量
    'PAGE_SIZE': 30,                # 每页视频数量
    'REQUEST_TIMEOUT': 30,          # 请求超时时间(秒)
    'RETRY_DELAY': 2,               # 重试延迟时间(秒)
    'MAX_RETRIES': 3,               # 最大重试次数
    
    # 反爬虫设置
    'USE_RANDOM_DELAY': True,       # 是否使用随机延迟
    'MIN_DELAY': 1,                 # 最小延迟时间(秒)
    'MAX_DELAY': 3,                 # 最大延迟时间(秒)
    
    # 输出设置
    'OUTPUT_FORMAT': 'csv',         # 输出格式: csv, json, xlsx
    'INCLUDE_TIMESTAMP': True,      # 是否在文件名中包含时间戳
    'ENCODING': 'utf-8-sig',        # 文件编码
    
    # 调试设置
    'DEBUG_MODE': False,            # 是否开启调试模式
    'SAVE_HTML': False,             # 是否保存HTML调试文件
    'VERBOSE_LOGGING': True,        # 是否显示详细日志
}

# 用户代理列表 (用于轮换)
USER_AGENTS = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/119.0',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
]

# 常用UP主配置 (示例)
POPULAR_UPS = {
    'test_up': {
        'uid': '93796936',
        'name': '测试UP主',
        'url': 'https://space.bilibili.com/93796936',
        'description': '用于测试的UP主账号'
    }
}

def get_config(key=None, default=None):
    """
    获取配置项
    
    Args:
        key: 配置项键名
        default: 默认值
    
    Returns:
        配置值或默认值
    """
    if key is None:
        return DEFAULT_CONFIG
    return DEFAULT_CONFIG.get(key, default)

def update_config(updates):
    """
    更新配置项
    
    Args:
        updates: 要更新的配置字典
    """
    DEFAULT_CONFIG.update(updates)
