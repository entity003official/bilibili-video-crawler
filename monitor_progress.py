"""
爬虫进度监控脚本
实时监控爬取进度和结果
"""
import os
import time
import glob
from datetime import datetime

def monitor_crawling():
    """监控爬取进度"""
    print("=" * 60)
    print("B站视频爬取进度监控")
    print("=" * 60)
    
    start_time = datetime.now()
    last_file_count = 0
    
    while True:
        try:
            # 查找所有相关的CSV文件
            csv_files = glob.glob("bilibili_videos*.csv")
            
            if csv_files:
                # 找到最新的文件
                latest_file = max(csv_files, key=os.path.getctime)
                
                # 统计行数（减去表头）
                try:
                    with open(latest_file, 'r', encoding='utf-8-sig') as f:
                        line_count = sum(1 for line in f) - 1  # 减去表头
                except:
                    line_count = 0
                
                # 计算运行时间
                elapsed = datetime.now() - start_time
                elapsed_str = str(elapsed).split('.')[0]  # 去掉微秒
                
                # 清屏并显示进度
                os.system('cls' if os.name == 'nt' else 'clear')
                print("=" * 60)
                print("B站视频爬取进度监控")
                print("=" * 60)
                print(f"开始时间: {start_time.strftime('%Y-%m-%d %H:%M:%S')}")
                print(f"运行时间: {elapsed_str}")
                print(f"最新文件: {latest_file}")
                print(f"已爬取视频数: {line_count}")
                
                if line_count != last_file_count:
                    print(f"新增视频: {line_count - last_file_count}")
                    last_file_count = line_count
                
                print("-" * 60)
                print("按 Ctrl+C 停止监控")
                print("=" * 60)
            else:
                print(f"等待爬虫开始... (运行时间: {datetime.now() - start_time})")
            
            time.sleep(5)  # 每5秒更新一次
            
        except KeyboardInterrupt:
            print("\n监控已停止")
            break
        except Exception as e:
            print(f"监控出错: {e}")
            time.sleep(5)

if __name__ == "__main__":
    monitor_crawling()
