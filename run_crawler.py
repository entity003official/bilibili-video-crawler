"""
B站爬虫使用示例
你可以修改这个文件来自定义爬取参数
"""

# 导入爬虫模块
from bilibili_batch_crawler import fetch_videos_selenium, save_videos_to_csv, save_videos_to_json

def main():
    # ========== 在这里修改你的配置 ==========
    
    # up主视频页面URL (必须修改为你要爬取的up主)
    up_url = "https://space.bilibili.com/93796936/video"
    
    # 要爬取的视频数量
    max_videos = 50
    
    # 页面加载等待时间（秒），如果网络较慢可以增加
    delay = 3
    
    # 输出文件名
    output_filename = "my_bilibili_videos"
    
    # ==========================================
    
    print("=" * 50)
    print("B站up主视频批量爬取工具")
    print("=" * 50)
    print(f"UP主URL: {up_url}")
    print(f"目标数量: {max_videos}")
    print(f"等待时间: {delay}秒")
    print("=" * 50)
    
    # 开始爬取
    videos = fetch_videos_selenium(up_url, max_videos, delay)
    
    if videos:
        # 保存为CSV格式
        save_videos_to_csv(videos, f"{output_filename}.csv")
        
        # 保存为JSON格式  
        save_videos_to_json(videos, f"{output_filename}.json")
        
        # 显示统计信息
        print("\n" + "=" * 50)
        print("爬取完成！统计信息:")
        print("=" * 50)
        print(f"总视频数: {len(videos)}")
        print(f"CSV文件: {output_filename}.csv")
        print(f"JSON文件: {output_filename}.json")
        
        # 显示前10个视频
        print(f"\n前10个视频:")
        print("-" * 80)
        for i, video in enumerate(videos[:10], 1):
            title = video['title'][:30] + "..." if len(video['title']) > 30 else video['title']
            print(f"{i:2d}. {title:35s} | {video['bv']:15s} | 第{video['page']}页")
        
        if len(videos) > 10:
            print(f"... 还有 {len(videos) - 10} 个视频")
            
    else:
        print("爬取失败，请检查:")
        print("1. 网络连接是否正常")
        print("2. URL是否正确")
        print("3. 是否安装了selenium: pip install selenium")
        print("4. Chrome浏览器是否已安装")

if __name__ == "__main__":
    main()
