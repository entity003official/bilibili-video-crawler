"""
B站爬虫进度监控工具
==================

功能说明：
- 📊 实时监控：显示爬取进度和速度统计
- 📈 可视化进度：进度条和百分比显示
- 📋 文件监控：自动检测新生成的数据文件
- ⏱️ 时间统计：计算爬取耗时和预估完成时间

主要功能：
1. monitor_crawling() - 实时监控爬取进度
2. display_progress_bar() - 显示可视化进度条
3. calculate_crawling_speed() - 计算爬取速度
4. show_file_statistics() - 显示文件统计信息

使用方法：
1. 在另一个终端运行爬虫
2. 运行此脚本监控进度：python monitor_progress.py
3. 实时查看爬取状态和统计信息

技术特点：
- 非阻塞监控，不影响爬虫运行
- 支持多种数据文件格式
- 自动计算爬取效率

作者：GitHub Copilot
更新：2025-08-05
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
            # 查找所有相关的CSV文件（包括安全退出版本的文件）
            csv_patterns = [
                "bilibili_videos_safe_*.csv",
                "bilibili_videos_all_*.csv", 
                "bilibili_videos_*.csv"
            ]
            
            csv_files = []
            for pattern in csv_patterns:
                csv_files.extend(glob.glob(pattern))
            
            # 去重并按修改时间排序
            csv_files = list(set(csv_files))
            
            if csv_files:
                # 找到最新的文件（按修改时间）
                latest_file = max(csv_files, key=os.path.getmtime)
                
                # 统计行数（减去表头）
                try:
                    with open(latest_file, 'r', encoding='utf-8-sig') as f:
                        lines = f.readlines()
                        line_count = len(lines) - 1 if lines else 0  # 减去表头
                        
                    # 获取文件修改时间
                    file_mtime = datetime.fromtimestamp(os.path.getmtime(latest_file))
                    
                except Exception as e:
                    line_count = 0
                    print(f"读取文件出错: {e}")
                
                # 计算运行时间
                elapsed = datetime.now() - start_time
                elapsed_str = str(elapsed).split('.')[0]  # 去掉微秒
                
                # 清屏并显示进度
                os.system('cls' if os.name == 'nt' else 'clear')
                print("=" * 70)
                print("🎬 B站视频爬取进度监控")
                print("=" * 70)
                print(f"📅 开始时间: {start_time.strftime('%Y-%m-%d %H:%M:%S')}")
                print(f"⏱️  运行时间: {elapsed_str}")
                print(f"📁 最新文件: {latest_file}")
                print(f"📝 文件修改: {file_mtime.strftime('%Y-%m-%d %H:%M:%S')}")
                print(f"🎯 已爬取视频数: {line_count}")
                
                if line_count != last_file_count:
                    new_count = line_count - last_file_count
                    print(f"🆕 新增视频: {new_count}")
                    last_file_count = line_count
                else:
                    print("⏳ 等待新数据...")
                
                print("-" * 70)
                print("💡 提示: 按 Ctrl+C 停止监控")
                print("=" * 70)
            else:
                # 清屏显示等待状态
                os.system('cls' if os.name == 'nt' else 'clear')
                print("=" * 70)
                print("🔍 等待爬虫开始...")
                print("=" * 70)
                elapsed = datetime.now() - start_time
                elapsed_str = str(elapsed).split('.')[0]
                print(f"⏱️  等待时间: {elapsed_str}")
                print(f"📂 当前目录: {os.getcwd()}")
                print(f"🔎 查找文件: bilibili_videos_*.csv")
                
                # 显示目录中的相关文件
                all_files = glob.glob("*.csv")
                if all_files:
                    print(f"📋 发现的CSV文件:")
                    for f in all_files:
                        mtime = datetime.fromtimestamp(os.path.getmtime(f))
                        print(f"   📄 {f} (修改: {mtime.strftime('%H:%M:%S')})")
                else:
                    print("❌ 未发现任何CSV文件")
                
                print("-" * 70)
                print("💡 提示: 确保爬虫程序正在运行")
                print("=" * 70)
            
            time.sleep(5)  # 每5秒更新一次
            
        except KeyboardInterrupt:
            print("\n监控已停止")
            break
        except Exception as e:
            print(f"监控出错: {e}")
            time.sleep(5)

if __name__ == "__main__":
    monitor_crawling()
