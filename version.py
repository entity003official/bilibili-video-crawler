"""
版本信息
========

当前版本: v2.1.0
发布日期: 2025-08-05
"""

__version__ = "2.1.0"
__author__ = "GitHub Copilot & Math_error@163.com"
__description__ = "B站UP主视频异步爬虫工具"

# 版本历史
VERSION_HISTORY = {
    "2.1.0": {
        "date": "2025-08-05",
        "features": [
            "新增配置管理模块（crawler_config.py）",
            "新增日志记录模块（crawler_logger.py）",
            "优化错误处理和用户提示",
            "增强数据统计显示功能",
            "改进代码文档和注释",
        ],
        "improvements": [
            "更好的模块化设计",
            "增强的日志记录",
            "优化的统计信息显示",
            "更友好的错误提示",
        ]
    },
    "2.0.0": {
        "date": "2025-08-05",
        "features": [
            "基于MediaCrawler设计的异步API爬虫",
            "无浏览器依赖的高性能爬取",
            "智能反爬虫机制",
            "多重备用方案",
            "自动CSV输出",
        ],
        "breaking_changes": [
            "重构核心爬取逻辑",
            "改用异步编程模式",
        ]
    },
    "1.0.0": {
        "date": "2025-08-04",
        "features": [
            "基础Selenium爬虫功能",
            "批量UP主爬取",
            "CSV数据输出",
            "Chrome用户数据支持",
        ]
    }
}

def get_version():
    """获取当前版本号"""
    return __version__

def get_version_info():
    """获取详细版本信息"""
    current = VERSION_HISTORY.get(__version__, {})
    return {
        "version": __version__,
        "author": __author__,
        "description": __description__,
        "release_date": current.get("date", "未知"),
        "features": current.get("features", []),
        "improvements": current.get("improvements", []),
    }

if __name__ == "__main__":
    info = get_version_info()
    print(f"B站爬虫工具 v{info['version']}")
    print(f"作者: {info['author']}")
    print(f"发布日期: {info['release_date']}")
    print(f"功能: {info['description']}")
    
    if info['features']:
        print("\n✨ 新功能:")
        for feature in info['features']:
            print(f"  • {feature}")
    
    if info['improvements']:
        print("\n🚀 改进:")
        for improvement in info['improvements']:
            print(f"  • {improvement}")
