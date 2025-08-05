"""
B站爬虫 - 无浏览器版本
使用requests + BeautifulSoup进行爬取，避免浏览器依赖
"""
import requests
import json
import csv
import re
import time
from datetime import datetime
from bs4 import BeautifulSoup
import signal
import sys

# 全局变量用于控制程序退出
should_stop = False

def signal_handler(sig, frame):
    """处理Ctrl+C信号"""
    global should_stop
    print('\n\n🛑 检测到退出信号...')
    should_stop = True
    print('✅ 程序已安全退出')
    sys.exit(0)

# 注册信号处理器
signal.signal(signal.SIGINT, signal_handler)

def get_bilibili_videos_api(mid, page_size=50, max_pages=20):
    """使用B站API获取UP主视频列表"""
    global should_stop
    
    print(f"🚀 开始使用API方式爬取UP主视频")
    print(f"📊 UP主ID: {mid}")
    print(f"📄 每页数量: {page_size}")
    print(f"🔢 最大页数: {max_pages}")
    print("=" * 60)
    
    # 设置请求头，模拟真实浏览器
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Accept': 'application/json, text/plain, */*',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
        'Accept-Encoding': 'gzip, deflate, br',
        'Referer': f'https://space.bilibili.com/{mid}/',
        'Origin': 'https://space.bilibili.com',
        'Connection': 'keep-alive',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-site'
    }
    
    session = requests.Session()
    session.headers.update(headers)
    
    all_videos = []
    
    for page in range(1, max_pages + 1):
        if should_stop:
            print(f"\n用户中断，已获取 {len(all_videos)} 个视频")
            break
            
        print(f"\n📄 正在获取第{page}页...")
        
        # B站API接口
        api_url = 'https://api.bilibili.com/x/space/wbi/arc/search'
        params = {
            'mid': mid,
            'pn': page,
            'ps': page_size,
            'index': 1,
            'order': 'pubdate',
            'order_avoided': 'true',
            'platform': 'web',
            'web_location': '1550101'
        }
        
        try:
            response = session.get(api_url, params=params, timeout=15)
            
            if response.status_code != 200:
                print(f"  ❌ 请求失败，状态码: {response.status_code}")
                break
                
            data = response.json()
            
            if data.get('code') != 0:
                print(f"  ❌ API返回错误: {data.get('message', '未知错误')}")
                break
            
            page_data = data.get('data', {})
            videos = page_data.get('list', {}).get('vlist', [])
            
            if not videos:
                print(f"  ❌ 第{page}页没有更多视频")
                break
            
            print(f"  ✓ 第{page}页获取到 {len(videos)} 个视频")
            
            # 处理视频数据
            page_videos = []
            for video in videos:
                if should_stop:
                    break
                    
                try:
                    video_info = {
                        'bvid': video.get('bvid', ''),
                        'aid': video.get('aid', ''),
                        'title': video.get('title', '').strip(),
                        'description': video.get('description', '').strip(),
                        'created': video.get('created', 0),
                        'length': video.get('length', ''),
                        'play': video.get('play', 0),
                        'video_review': video.get('video_review', 0),
                        'comment': video.get('comment', 0),
                        'pic': video.get('pic', ''),
                        'url': f"https://www.bilibili.com/video/{video.get('bvid', '')}",
                        'page': page
                    }
                    
                    # 转换时间戳为可读格式
                    if video_info['created']:
                        video_info['publish_time'] = datetime.fromtimestamp(video_info['created']).strftime('%Y-%m-%d %H:%M:%S')
                    else:
                        video_info['publish_time'] = '未知'
                    
                    page_videos.append(video_info)
                    
                except Exception as e:
                    print(f"  ⚠️ 解析视频数据出错: {e}")
                    continue
            
            all_videos.extend(page_videos)
            print(f"  ✅ 第{page}页处理完成，总计: {len(all_videos)} 个视频")
            
            # 检查是否还有更多页面
            total_count = page_data.get('page', {}).get('count', 0)
            current_count = len(all_videos)
            
            if current_count >= total_count:
                print(f"  🎯 已获取所有视频，共 {total_count} 个")
                break
            
            # 避免请求过快
            if not should_stop:
                time.sleep(1)
                
        except requests.RequestException as e:
            print(f"  ❌ 网络请求出错: {e}")
            break
        except json.JSONDecodeError as e:
            print(f"  ❌ JSON解析出错: {e}")
            break
        except Exception as e:
            print(f"  ❌ 未知错误: {e}")
            break
    
    return all_videos

def save_videos_to_csv(videos, filename=None):
    """保存视频数据到CSV文件"""
    if not videos:
        print("❌ 没有视频数据可保存")
        return None
    
    if not filename:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"bilibili_videos_api_{timestamp}.csv"
    
    try:
        with open(filename, 'w', newline='', encoding='utf-8-sig') as csvfile:
            fieldnames = [
                '序号', 'BV号', 'AV号', '视频标题', '视频描述', '视频链接', 
                '发布时间', '时长', '播放量', '弹幕数', '评论数', '封面图', '页码'
            ]
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            
            writer.writeheader()
            for i, video in enumerate(videos, 1):
                writer.writerow({
                    '序号': i,
                    'BV号': video['bvid'],
                    'AV号': video['aid'],
                    '视频标题': video['title'],
                    '视频描述': video['description'][:100] + '...' if len(video['description']) > 100 else video['description'],
                    '视频链接': video['url'],
                    '发布时间': video['publish_time'],
                    '时长': video['length'],
                    '播放量': video['play'],
                    '弹幕数': video['video_review'],
                    '评论数': video['comment'],
                    '封面图': video['pic'],
                    '页码': video['page']
                })
        
        print(f"✅ 已保存 {len(videos)} 个视频到 {filename}")
        return filename
        
    except Exception as e:
        print(f"❌ 保存文件出错: {e}")
        return None

def extract_mid_from_url(url):
    """从B站空间URL中提取UP主ID"""
    # 匹配 https://space.bilibili.com/93796936/upload/video 格式
    match = re.search(r'space\.bilibili\.com/(\d+)', url)
    if match:
        return match.group(1)
    return None

def main():
    global should_stop
    
    print("=" * 70)
    print("🎯 B站UP主视频爬取工具 - API版本")
    print("💡 特点:")
    print("   - 无需启动浏览器，速度更快")
    print("   - 使用官方API，数据更准确")
    print("   - 支持Ctrl+C安全退出")
    print("   - 包含详细的视频统计信息")
    print("=" * 70)
    
    # 目标UP主
    space_url = "https://space.bilibili.com/93796936/upload/video"
    mid = extract_mid_from_url(space_url)
    
    if not mid:
        print("❌ 无法从URL中提取UP主ID")
        return
    
    print(f"🎯 目标UP主: {space_url}")
    print(f"📊 UP主ID: {mid}")
    print(f"⏰ 开始时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    start_time = datetime.now()
    
    try:
        # 开始爬取
        videos = get_bilibili_videos_api(mid)
        
        if videos and not should_stop:
            # 保存结果
            filename = save_videos_to_csv(videos)
            
            if filename:
                end_time = datetime.now()
                duration = end_time - start_time
                
                print("\n" + "=" * 70)
                print("🎉 爬取完成!")
                print("=" * 70)
                print(f"✅ 成功获取: {len(videos)} 个视频")
                print(f"✅ 保存文件: {filename}")
                print(f"✅ 总耗时: {duration}")
                
                # 显示视频统计
                if videos:
                    total_play = sum(v['play'] for v in videos)
                    total_comment = sum(v['comment'] for v in videos)
                    print(f"📊 总播放量: {total_play:,}")
                    print(f"💬 总评论数: {total_comment:,}")
                
                # 显示前5个视频预览
                print(f"\n📺 视频预览:")
                for i, video in enumerate(videos[:5], 1):
                    title = video['title'][:40] + "..." if len(video['title']) > 40 else video['title']
                    print(f"{i}. {title} (播放: {video['play']}, {video['publish_time']})")
                
                if len(videos) > 5:
                    print(f"... 还有 {len(videos) - 5} 个视频")
                    
        elif should_stop:
            print(f"\n🛑 用户中断，已获取 {len(videos) if videos else 0} 个视频")
            if videos:
                save_videos_to_csv(videos)
        else:
            print("\n📝 没有获取到视频数据")
            
    except KeyboardInterrupt:
        print("\n\n🛑 程序被用户中断")
        if 'videos' in locals() and videos:
            print("💾 正在保存已获取的数据...")
            save_videos_to_csv(videos)
    except Exception as e:
        print(f"\n❌ 程序异常: {e}")
    finally:
        print("\n👋 程序结束")

if __name__ == "__main__":
    main()
