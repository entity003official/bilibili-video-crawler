"""
B站Selenium批量爬虫核心模块
============================

功能说明：
- 🌐 浏览器驱动：基于Selenium + Chrome的传统爬虫方案
- 🎯 批量爬取：支持大规模UP主视频数据采集
- 📊 多格式输出：支持CSV、JSON等多种数据格式
- 🔧 高度可配：支持自定义参数和爬取策略

核心功能：
1. fetch_videos_selenium() - Selenium爬虫主函数
2. save_videos_to_csv() - CSV格式数据保存
3. save_videos_to_json() - JSON格式数据保存
4. setup_driver() - 浏览器驱动配置

适用场景：
- API爬虫失效时的备用方案
- 需要渲染JavaScript的页面
- 需要模拟真实用户行为的场景

技术特点：
- 支持无头模式运行
- 自动处理页面加载等待
- 完善的错误恢复机制

依赖要求：
- Chrome浏览器
- ChromeDriver
- selenium库

作者：GitHub Copilot
状态：稳定版本，备用推荐
"""
import requests
from bs4 import BeautifulSoup
import re
import time
import csv
import json
from urllib.parse import urljoin
import argparse

def fetch_videos_selenium(url, max_videos=50, delay=2):
    """
    使用selenium批量爬取up主的视频
    :param url: up主视频页面URL 
    :param max_videos: 最大爬取视频数量
    :param delay: 页面加载等待时间
    :return: 视频列表
    """
    try:
        from selenium import webdriver
        from selenium.webdriver.common.by import By
        from selenium.webdriver.support.ui import WebDriverWait
        from selenium.webdriver.support import expected_conditions as EC
        from selenium.webdriver.chrome.options import Options
        from selenium.common.exceptions import TimeoutException, NoSuchElementException
        
        print(f"正在用selenium批量爬取: {url}")
        print(f"目标视频数量: {max_videos}, 页面等待时间: {delay}秒")
        
        # Chrome选项
        options = Options()
        options.add_argument('--headless')  # 无头模式
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--disable-gpu')
        options.add_argument('--window-size=1920,1080')
        options.add_argument('--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36')
        
        driver = webdriver.Chrome(options=options)
        driver.get(url)
        
        videos = []
        page = 1
        consecutive_empty_pages = 0  # 连续空页面计数
        
        while len(videos) < max_videos and consecutive_empty_pages < 3:
            print(f"正在爬取第{page}页...")
            
            # 等待页面加载
            time.sleep(delay)
            
            # 尝试多种选择器获取所有视频
            selectors = [
                "a.bili-cover-card",
                "a[href*='/video/BV']",
                "a[href*='bilibili.com/video']",
                ".video-card a"
            ]
            
            video_elements = []
            for selector in selectors:
                try:
                    elements = driver.find_elements(By.CSS_SELECTOR, selector)
                    if elements:
                        video_elements = elements
                        print(f"使用选择器 {selector} 找到 {len(elements)} 个视频元素")
                        break
                except:
                    continue
            
            if not video_elements:
                print(f"第{page}页未找到视频元素")
                consecutive_empty_pages += 1
                page += 1
                continue
            
            # 提取当前页面的视频信息
            current_page_videos = []
            for element in video_elements:
                try:
                    href = element.get_attribute('href')
                    if not href or '/video/BV' not in href:
                        continue
                        
                    bv_match = re.search(r'/video/(BV[\w]+)', href)
                    if not bv_match:
                        continue
                        
                    bv_id = bv_match.group(1)
                    
                    # 获取视频标题（增强版）
                    title = get_video_title(element, bv_id)
                    
                    # 获取视频时长（如果有）
                    duration = get_video_duration(element)
                    
                    # 获取播放量（如果有）
                    play_count = get_video_play_count(element)
                    
                    video_info = {
                        "bv": bv_id,
                        "url": href,
                        "title": title.strip(),
                        "duration": duration,
                        "play_count": play_count,
                        "page": page
                    }
                    
                    # 避免重复添加
                    if not any(v["bv"] == bv_id for v in videos):
                        current_page_videos.append(video_info)
                        
                except Exception as e:
                    print(f"解析视频元素出错: {e}")
                    continue
            
            if not current_page_videos:
                print(f"第{page}页没有新的视频")
                consecutive_empty_pages += 1
            else:
                consecutive_empty_pages = 0  # 重置连续空页面计数
                videos.extend(current_page_videos)
                print(f"第{page}页获取了 {len(current_page_videos)} 个视频，总计: {len(videos)}")
            
            # 检查是否已达到目标数量
            if len(videos) >= max_videos:
                videos = videos[:max_videos]  # 截取到指定数量
                break
            
            # 尝试翻页
            success = try_next_page(driver, url, page)
            if not success:
                print("无法翻页，可能已到最后一页")
                break
                
            page += 1
        
        driver.quit()
        print(f"爬取完成，共获取 {len(videos)} 个视频")
        return videos
            
    except ImportError:
        print("selenium未安装，请运行: pip install selenium")
        return []
    except Exception as e:
        print(f"selenium批量爬取错误: {e}")
        return []

def get_video_title(element, bv_id):
    """获取视频标题"""
    title = ""
    try:
        # 尝试从title属性获取
        title = element.get_attribute('title')
        if not title:
            # 尝试从子元素获取标题
            title_selectors = [
                '.bili-video-card__info--tit',
                '.video-name',
                '.title',
                'p[title]',
                '.info .title',
                '.video-title'
            ]
            for title_selector in title_selectors:
                try:
                    from selenium.webdriver.common.by import By
                    title_element = element.find_element(By.CSS_SELECTOR, title_selector)
                    title = title_element.get_attribute('title') or title_element.text
                    if title:
                        break
                except:
                    continue
        
        if not title:
            # 最后尝试从aria-label获取
            title = element.get_attribute('aria-label') or f"视频_{bv_id}"
            
    except:
        title = f"视频_{bv_id}"
    
    return title

def get_video_duration(element):
    """获取视频时长"""
    try:
        from selenium.webdriver.common.by import By
        duration_selectors = [
            '.bili-video-card__stats__duration',
            '.duration',
            '.video-duration'
        ]
        for selector in duration_selectors:
            try:
                duration_element = element.find_element(By.CSS_SELECTOR, selector)
                return duration_element.text
            except:
                continue
        return ""
    except:
        return ""

def get_video_play_count(element):
    """获取播放量"""
    try:
        from selenium.webdriver.common.by import By
        play_selectors = [
            '.bili-video-card__stats__view',
            '.play-count',
            '.video-play'
        ]
        for selector in play_selectors:
            try:
                play_element = element.find_element(By.CSS_SELECTOR, selector)
                return play_element.text
            except:
                continue
        return ""
    except:
        return ""

def try_next_page(driver, base_url, current_page):
    """尝试翻页"""
    try:
        # 滚动到页面底部
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)
        
        # 检查是否有"加载更多"按钮或翻页按钮
        from selenium.webdriver.common.by import By
        load_more_selectors = [
            ".load-more-btn",
            ".pagination-btn-next", 
            ".page-next",
            "button[aria-label='下一页']",
            ".be-pager-next"
        ]
        
        for selector in load_more_selectors:
            try:
                button = driver.find_element(By.CSS_SELECTOR, selector)
                if button.is_enabled() and button.is_displayed():
                    driver.execute_script("arguments[0].click();", button)
                    print(f"点击了翻页按钮: {selector}")
                    time.sleep(3)
                    return True
            except:
                continue
        
        # 如果没有翻页按钮，尝试修改URL翻页
        next_page = current_page + 1
        if "pn=" in base_url:
            new_url = re.sub(r'pn=\d+', f'pn={next_page}', base_url)
        else:
            separator = "&" if "?" in base_url else "?"
            new_url = f"{base_url}{separator}pn={next_page}"
        
        driver.get(new_url)
        time.sleep(3)
        return True
        
    except Exception as e:
        print(f"翻页失败: {e}")
        return False

def save_videos_to_csv(videos, filename="bilibili_videos.csv"):
    """将视频列表保存到CSV文件"""
    if not videos:
        print("没有视频数据可保存")
        return
        
    with open(filename, 'w', newline='', encoding='utf-8-sig') as csvfile:
        fieldnames = ['序号', 'BV号', '视频标题', '视频链接', '时长', '播放量', '页码']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        
        writer.writeheader()
        for i, video in enumerate(videos, 1):
            writer.writerow({
                '序号': i,
                'BV号': video['bv'],
                '视频标题': video['title'],
                '视频链接': video['url'],
                '时长': video.get('duration', ''),
                '播放量': video.get('play_count', ''),
                '页码': video['page']
            })
    
    print(f"已保存 {len(videos)} 个视频到 {filename}")

def save_videos_to_json(videos, filename="bilibili_videos.json"):
    """将视频列表保存到JSON文件"""
    if not videos:
        print("没有视频数据可保存")
        return
        
    with open(filename, 'w', encoding='utf-8') as jsonfile:
        json.dump(videos, jsonfile, ensure_ascii=False, indent=2)
    
    print(f"已保存 {len(videos)} 个视频到 {filename}")

def main():
    parser = argparse.ArgumentParser(description='B站up主视频批量爬取工具')
    parser.add_argument('--url', '-u', required=True, help='up主视频页面URL')
    parser.add_argument('--max-videos', '-n', type=int, default=50, help='最大爬取视频数量 (默认: 50)')
    parser.add_argument('--delay', '-d', type=int, default=2, help='页面加载等待时间/秒 (默认: 2)')
    parser.add_argument('--output', '-o', default='bilibili_videos', help='输出文件名前缀 (默认: bilibili_videos)')
    parser.add_argument('--format', '-f', choices=['csv', 'json', 'both'], default='csv', help='输出格式 (默认: csv)')
    
    args = parser.parse_args()
    
    print(f"开始批量爬取up主视频")
    print(f"URL: {args.url}")
    print(f"目标数量: {args.max_videos}")
    print(f"输出格式: {args.format}")
    
    # 使用selenium批量爬取
    videos = fetch_videos_selenium(args.url, args.max_videos, args.delay)
    
    if videos:
        # 根据选择的格式保存文件
        if args.format in ['csv', 'both']:
            save_videos_to_csv(videos, f"{args.output}.csv")
        if args.format in ['json', 'both']:
            save_videos_to_json(videos, f"{args.output}.json")
        
        # 显示前几个视频作为示例
        print("\n前5个视频示例:")
        for i, video in enumerate(videos[:5], 1):
            print(f"{i}. {video['title']} - {video['bv']} - {video['url']}")
            
        print(f"\n总计成功爬取 {len(videos)} 个视频")
    else:
        print("爬取失败，没有获取到视频数据")

if __name__ == "__main__":
    # 如果没有命令行参数，使用默认配置
    import sys
    if len(sys.argv) == 1:
        # 默认配置
        up_url = "https://space.bilibili.com/93796936/video"
        max_videos = 100
        
        print(f"使用默认配置:")
        print(f"URL: {up_url}")
        print(f"目标数量: {max_videos}")
        
        videos = fetch_videos_selenium(up_url, max_videos)
        
        if videos:
            save_videos_to_csv(videos, "bilibili_videos_enhanced.csv")
            save_videos_to_json(videos, "bilibili_videos_enhanced.json")
            
            print("\n前5个视频示例:")
            for i, video in enumerate(videos[:5], 1):
                print(f"{i}. {video['title']} - {video['bv']} - {video['url']}")
                
            print(f"\n总计成功爬取 {len(videos)} 个视频")
        else:
            print("爬取失败，没有获取到视频数据")
    else:
        main()
