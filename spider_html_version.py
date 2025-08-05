"""
B站爬虫 - 简化requests版本
使用requests直接爬取页面HTML，无需浏览器
"""
import requests
import csv
import re
import time
from datetime import datetime
from bs4 import BeautifulSoup
import signal
import sys
import json

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

def get_videos_from_html(url, max_pages=10):
    """从HTML页面解析视频信息"""
    global should_stop
    
    print(f"🚀 开始使用HTML解析方式爬取")
    print(f"🔗 目标URL: {url}")
    print("=" * 60)
    
    # 设置请求头
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
        'Accept-Encoding': 'gzip, deflate, br',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
        'Sec-Fetch-Dest': 'document',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-Site': 'none',
        'Cache-Control': 'max-age=0'
    }
    
    session = requests.Session()
    session.headers.update(headers)
    
    all_videos = []
    
    # 先尝试获取第一页，看看页面结构
    try:
        print("📄 正在获取第1页...")
        response = session.get(url, timeout=15)
        response.raise_for_status()
        
        print(f"✓ 页面获取成功，状态码: {response.status_code}")
        print(f"✓ 页面大小: {len(response.text)} 字符")
        
        # 保存HTML用于调试
        with open("debug_page.html", "w", encoding="utf-8") as f:
            f.write(response.text)
        print("📝 页面HTML已保存到 debug_page.html")
        
        # 使用BeautifulSoup解析
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # 尝试多种选择器找视频链接
        selectors = [
            'a[href*="/video/BV"]',  # 包含BV号的链接
            '.bili-cover-card',      # B站封面卡片
            '.video-card',           # 视频卡片
            '.bili-video-card',      # B站视频卡片
            'a[title]'               # 有标题的链接
        ]
        
        videos_found = []
        for selector in selectors:
            elements = soup.select(selector)
            if elements:
                print(f"✓ 使用选择器 '{selector}' 找到 {len(elements)} 个元素")
                
                for element in elements:
                    href = element.get('href', '')
                    if '/video/BV' in href:
                        videos_found.append(element)
                        
                if videos_found:
                    break
        
        if not videos_found:
            print("❌ 未找到视频链接，可能需要登录或页面结构已变化")
            
            # 尝试查找页面中的JSON数据
            print("🔍 尝试查找页面中的JSON数据...")
            
            # 查找window.__INITIAL_STATE__或__RENDER_DATA__
            script_tags = soup.find_all('script')
            json_found = False
            
            for script in script_tags:
                # 检查__RENDER_DATA__
                if script.get('id') == '__RENDER_DATA__':
                    print("✓ 找到__RENDER_DATA__")
                    try:
                        import urllib.parse
                        encoded_data = script.string or script.text
                        decoded_data = urllib.parse.unquote(encoded_data)
                        json_data = json.loads(decoded_data)
                        
                        with open("debug_render_data.json", "w", encoding="utf-8") as f:
                            json.dump(json_data, f, ensure_ascii=False, indent=2)
                        print("📝 RENDER_DATA已保存到 debug_render_data.json")
                        json_found = True
                        
                    except Exception as e:
                        print(f"❌ RENDER_DATA解析失败: {e}")
                
                # 检查其他JavaScript数据
                elif script.string and any(keyword in script.string for keyword in ['__INITIAL_STATE__', 'window._render_data_', 'videoList']):
                    print("✓ 找到可能的视频数据")
                    
                    # 尝试提取JSON
                    json_patterns = [
                        r'window\.__INITIAL_STATE__\s*=\s*({.*?});',
                        r'window\._render_data_\s*=\s*({.*?});',
                        r'videoList\s*:\s*(\[.*?\])',
                        r'"vlist"\s*:\s*(\[.*?\])'
                    ]
                    
                    for pattern in json_patterns:
                        match = re.search(pattern, script.string, re.DOTALL)
                        if match:
                            try:
                                json_data = json.loads(match.group(1))
                                
                                with open("debug_extracted_data.json", "w", encoding="utf-8") as f:
                                    json.dump(json_data, f, ensure_ascii=False, indent=2)
                                print(f"📝 提取的数据已保存到 debug_extracted_data.json")
                                
                                videos_from_json = extract_videos_from_json(json_data)
                                if videos_from_json:
                                    print(f"✓ 从JSON数据中提取到 {len(videos_from_json)} 个视频")
                                    return videos_from_json
                                json_found = True
                                break
                                
                            except json.JSONDecodeError as e:
                                print(f"❌ JSON解析失败: {e}")
                                continue
                
                if json_found:
                    break
            
            if not json_found:
                print("❌ 未找到可解析的JSON数据")
            
            # 最后尝试：直接访问API
            print("🔄 尝试直接访问B站API...")
            mid = re.search(r'/(\d+)/', url)
            if mid:
                mid = mid.group(1)
                api_videos = try_api_fallback(mid, session)
                if api_videos:
                    return api_videos
            
            return []
        
        # 解析视频信息
        print(f"📺 开始解析 {len(videos_found)} 个视频...")
        
        for i, element in enumerate(videos_found, 1):
            if should_stop:
                break
                
            try:
                href = element.get('href', '')
                if not href:
                    continue
                    
                # 处理相对链接
                if href.startswith('//'):
                    href = 'https:' + href
                elif href.startswith('/'):
                    href = 'https://www.bilibili.com' + href
                
                # 提取BV号
                bv_match = re.search(r'/video/(BV[\w]+)', href)
                if not bv_match:
                    continue
                    
                bv_id = bv_match.group(1)
                
                # 获取标题
                title = (element.get('title') or 
                        element.get('aria-label') or 
                        element.text.strip() or 
                        f"视频_{bv_id}")
                
                video_info = {
                    'bvid': bv_id,
                    'title': title.strip(),
                    'url': href,
                    'page': 1
                }
                
                all_videos.append(video_info)
                
                if i % 10 == 0:
                    print(f"  处理进度: {i}/{len(videos_found)}")
                    
            except Exception as e:
                print(f"❌ 解析视频 {i} 出错: {e}")
                continue
        
        print(f"✅ 成功解析 {len(all_videos)} 个视频")
        return all_videos
        
    except requests.RequestException as e:
        print(f"❌ 网络请求失败: {e}")
        return []
    except Exception as e:
        print(f"❌ 解析过程出错: {e}")
        return []

def extract_videos_from_json(json_data):
    """从JSON数据中提取视频信息"""
    videos = []
    
    try:
        # 尝试多种可能的JSON结构
        possible_paths = [
            ['videoData', 'list'],
            ['archive', 'list'],
            ['data', 'list', 'vlist'],
            ['page', 'list'],
            ['result', 'data']
        ]
        
        video_list = None
        for path in possible_paths:
            current = json_data
            try:
                for key in path:
                    current = current[key]
                if isinstance(current, list) and current:
                    video_list = current
                    print(f"✓ 在路径 {' -> '.join(path)} 找到视频列表")
                    break
            except (KeyError, TypeError):
                continue
        
        if not video_list:
            print("❌ 未在JSON数据中找到视频列表")
            return []
        
        for item in video_list:
            try:
                bvid = item.get('bvid') or item.get('bv_id') or ''
                title = item.get('title') or item.get('name') or f"视频_{bvid}"
                
                if bvid:
                    videos.append({
                        'bvid': bvid,
                        'title': title.strip(),
                        'url': f"https://www.bilibili.com/video/{bvid}",
                        'play': item.get('play', 0),
                        'comment': item.get('comment', 0),
                        'page': 1
                    })
            except Exception as e:
                continue
                
    except Exception as e:
        print(f"❌ JSON数据解析出错: {e}")
    
    return videos

def try_api_fallback(mid, session):
    """尝试使用简化的API作为备选方案"""
    try:
        print(f"🔗 尝试API备选方案，UP主ID: {mid}")
        
        # 简化的API请求
        api_url = f"https://api.bilibili.com/x/space/arc/search?mid={mid}&ps=30&tid=0&pn=1&keyword=&order=pubdate"
        
        response = session.get(api_url, timeout=10)
        if response.status_code == 200:
            data = response.json()
            
            if data.get('code') == 0:
                vlist = data.get('data', {}).get('list', {}).get('vlist', [])
                
                videos = []
                for video in vlist:
                    videos.append({
                        'bvid': video.get('bvid', ''),
                        'title': video.get('title', ''),
                        'url': f"https://www.bilibili.com/video/{video.get('bvid', '')}",
                        'play': video.get('play', 0),
                        'comment': video.get('comment', 0),
                        'page': 1
                    })
                
                if videos:
                    print(f"✓ API备选方案成功获取 {len(videos)} 个视频")
                    return videos
                    
        print("❌ API备选方案也失败了")
        return []
        
    except Exception as e:
        print(f"❌ API备选方案出错: {e}")
        return []

def save_videos_csv(videos, filename=None):
    """保存视频到CSV文件"""
    if not videos:
        print("❌ 没有视频数据可保存")
        return None
    
    if not filename:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"bilibili_videos_html_{timestamp}.csv"
    
    try:
        with open(filename, 'w', newline='', encoding='utf-8-sig') as csvfile:
            fieldnames = ['序号', 'BV号', '视频标题', '视频链接', '播放量', '评论数', '页码']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            
            writer.writeheader()
            for i, video in enumerate(videos, 1):
                writer.writerow({
                    '序号': i,
                    'BV号': video['bvid'],
                    '视频标题': video['title'],
                    '视频链接': video['url'],
                    '播放量': video.get('play', ''),
                    '评论数': video.get('comment', ''),
                    '页码': video['page']
                })
        
        print(f"✅ 已保存 {len(videos)} 个视频到 {filename}")
        return filename
        
    except Exception as e:
        print(f"❌ 保存文件出错: {e}")
        return None

def main():
    global should_stop
    
    print("=" * 70)
    print("🎯 B站UP主视频爬取工具 - HTML解析版本")
    print("💡 特点:")
    print("   - 无需浏览器，直接解析HTML")
    print("   - 支持Ctrl+C安全退出")
    print("   - 生成调试文件便于分析")
    print("=" * 70)
    
    # 目标URL
    url = "https://space.bilibili.com/93796936/video"
    
    print(f"🎯 目标UP主: {url}")
    print(f"⏰ 开始时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    start_time = datetime.now()
    
    try:
        # 开始爬取
        videos = get_videos_from_html(url)
        
        if videos and not should_stop:
            # 保存结果
            filename = save_videos_csv(videos)
            
            if filename:
                end_time = datetime.now()
                duration = end_time - start_time
                
                print("\n" + "=" * 70)
                print("🎉 爬取完成!")
                print("=" * 70)
                print(f"✅ 成功获取: {len(videos)} 个视频")
                print(f"✅ 保存文件: {filename}")
                print(f"✅ 总耗时: {duration}")
                
                # 显示前5个视频预览
                print(f"\n📺 视频预览:")
                for i, video in enumerate(videos[:5], 1):
                    title = video['title'][:50] + "..." if len(video['title']) > 50 else video['title']
                    print(f"{i}. {title}")
                
                if len(videos) > 5:
                    print(f"... 还有 {len(videos) - 5} 个视频")
                    
        else:
            print("\n📝 没有获取到视频数据")
            print("💡 请检查 debug_page.html 和 debug_data.json 文件分析问题")
            
    except KeyboardInterrupt:
        print("\n\n🛑 程序被用户中断")
    except Exception as e:
        print(f"\n❌ 程序异常: {e}")
    finally:
        print("\n👋 程序结束")

if __name__ == "__main__":
    main()
