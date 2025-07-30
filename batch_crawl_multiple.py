"""
批量爬取多个up主的视频
使用config.py中的配置
"""

import os
import time
from config import uploader_configs, global_settings
from bilibili_batch_crawler import fetch_videos_selenium, save_videos_to_csv, save_videos_to_json

def ensure_directory(directory):
    """确保目录存在"""
    if not os.path.exists(directory):
        os.makedirs(directory)
        print(f"创建目录: {directory}")

def batch_crawl():
    """批量爬取多个up主"""
    print("=" * 60)
    print("B站up主视频批量爬取工具 - 多UP主模式")
    print("=" * 60)
    
    # 确保输出目录存在
    save_dir = global_settings.get("save_directory", "./output/")
    ensure_directory(save_dir)
    
    total_videos = 0
    successful_ups = 0
    
    for i, config in enumerate(uploader_configs, 1):
        print(f"\n[{i}/{len(uploader_configs)}] 开始爬取: {config['name']}")
        print("-" * 40)
        
        try:
            # 爬取视频
            videos = fetch_videos_selenium(
                url=config['url'],
                max_videos=config['max_videos'],
                delay=global_settings['delay']
            )
            
            if videos:
                # 构建输出文件路径
                base_filename = os.path.join(save_dir, config['output_file'])
                
                # 根据设置保存文件
                output_format = global_settings.get('output_format', 'csv')
                if output_format in ['csv', 'both']:
                    save_videos_to_csv(videos, f"{base_filename}.csv")
                if output_format in ['json', 'both']:
                    save_videos_to_json(videos, f"{base_filename}.json")
                
                total_videos += len(videos)
                successful_ups += 1
                
                print(f"✓ {config['name']} 爬取成功: {len(videos)} 个视频")
                
                # 显示前3个视频作为示例
                print("  前3个视频:")
                for j, video in enumerate(videos[:3], 1):
                    title = video['title'][:25] + "..." if len(video['title']) > 25 else video['title']
                    print(f"    {j}. {title}")
                    
            else:
                print(f"✗ {config['name']} 爬取失败")
                
        except Exception as e:
            print(f"✗ {config['name']} 爬取出错: {e}")
        
        # 在爬取不同up主之间添加延迟，避免被反爬虫
        if i < len(uploader_configs):
            print("等待5秒后继续...")
            time.sleep(5)
    
    # 显示总结
    print("\n" + "=" * 60)
    print("批量爬取完成！")
    print("=" * 60)
    print(f"成功爬取UP主数: {successful_ups}/{len(uploader_configs)}")
    print(f"总视频数: {total_videos}")
    print(f"文件保存在: {save_dir}")
    print("=" * 60)

if __name__ == "__main__":
    batch_crawl()
