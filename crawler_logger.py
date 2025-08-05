"""
B站爬虫日志记录模块
==================

提供结构化的日志记录功能
"""

import logging
import os
from datetime import datetime
from pathlib import Path

class CrawlerLogger:
    """爬虫专用日志记录器"""
    
    def __init__(self, log_level=logging.INFO):
        self.logger = logging.getLogger('bilibili_crawler')
        self.logger.setLevel(log_level)
        
        # 避免重复添加处理器
        if not self.logger.handlers:
            self._setup_handlers()
    
    def _setup_handlers(self):
        """设置日志处理器"""
        # 创建logs目录
        log_dir = Path('logs')
        log_dir.mkdir(exist_ok=True)
        
        # 文件处理器
        log_file = log_dir / f'crawler_{datetime.now().strftime("%Y%m%d")}.log'
        file_handler = logging.FileHandler(log_file, encoding='utf-8')
        file_handler.setLevel(logging.DEBUG)
        
        # 控制台处理器
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)
        
        # 设置格式
        file_formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        console_formatter = logging.Formatter(
            '%(levelname)s: %(message)s'
        )
        
        file_handler.setFormatter(file_formatter)
        console_handler.setFormatter(console_formatter)
        
        self.logger.addHandler(file_handler)
        self.logger.addHandler(console_handler)
    
    def info(self, message):
        """记录信息日志"""
        self.logger.info(message)
    
    def warning(self, message):
        """记录警告日志"""
        self.logger.warning(message)
    
    def error(self, message):
        """记录错误日志"""
        self.logger.error(message)
    
    def debug(self, message):
        """记录调试日志"""
        self.logger.debug(message)
    
    def crawl_start(self, up_url, max_videos):
        """记录爬取开始"""
        self.info(f"开始爬取 UP主: {up_url}, 目标数量: {max_videos}")
    
    def crawl_progress(self, current, total, page):
        """记录爬取进度"""
        self.info(f"爬取进度: {current}/{total} (第{page}页)")
    
    def crawl_complete(self, total_videos, total_views, filename):
        """记录爬取完成"""
        self.info(f"爬取完成! 视频数: {total_videos}, 总播放量: {total_views:,}, 保存至: {filename}")
    
    def api_error(self, error_code, error_msg):
        """记录API错误"""
        self.error(f"API错误 - 代码: {error_code}, 消息: {error_msg}")
    
    def network_error(self, url, error):
        """记录网络错误"""
        self.error(f"网络错误 - URL: {url}, 错误: {str(error)}")

# 全局日志实例
crawler_logger = CrawlerLogger()
