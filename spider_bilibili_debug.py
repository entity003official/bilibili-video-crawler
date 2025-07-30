"""
B站UP主视频爬取工具 - 调试版本
专门用于爬取指定UP主的所有视频
"""
import requests
from bs4 import BeautifulSoup
import re
import time
import csv
from urllib.parse import urljoin
import datetime

def fetch_videos_selenium_debug(url, max_videos=1000):
    """
    使用selenium批量爬取up主的视频 - 调试版本
    """
    try:
        from selenium import webdriver
        from selenium.webdriver.common.by import By
        from selenium.webdriver.support.ui import WebDriverWait
        from selenium.webdriver.support import expected_conditions as EC
        from selenium.webdriver.chrome.options import Options
        from selenium.common.exceptions import TimeoutException, NoSuchElementException
        from webdriver_manager.chrome import ChromeDriverManager
        from selenium.webdriver.chrome.service import Service
        
        print(f"正在用selenium批量爬取: {url}")
        print(f"目标最大视频数: {max_videos}")
        
        # Chrome选项
        options = Options()
        # 注释掉headless模式，方便调试
        # options.add_argument('--headless')  
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--disable-gpu')
        options.add_argument('--window-size=1920,1080')
        options.add_argument('--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36')
        
        # 使用webdriver-manager自动管理ChromeDriver
        try:
            service = Service(ChromeDriverManager().install())
            driver = webdriver.Chrome(service=service, options=options)
        except:
            # 如果webdriver-manager失败，尝试直接使用Chrome
            driver = webdriver.Chrome(options=options)
        
        print(f"浏览器启动成功，正在访问: {url}")
        driver.get(url)
        
        # 等待页面加载
        time.sleep(5)
        
        # 保存当前页面HTML用于调试
        with open(f"debug_page_source.html", "w", encoding="utf-8") as f:
            f.write(driver.page_source)
        print("页面源码已保存到 debug_page_source.html")
        
        # 检查页面标题
        page_title = driver.title
        print(f"页面标题: {page_title}")
        
        # 检查当前URL
        current_url = driver.current_url
        print(f"当前URL: {current_url}")
        
        videos = []
        page = 1
        consecutive_empty_pages = 0
        
        while len(videos) < max_videos and consecutive_empty_pages < 5:
            print(f"\n正在爬取第{page}页...")
            print(f"当前页面URL: {driver.current_url}")
            
            # 等待页面加载
            time.sleep(3)
            
            # 尝试多种选择器
            selectors = [
                "a.bili-cover-card",
                "a[href*='/video/BV']", 
                "a[href*='bilibili.com/video']",
                ".video-card a",
                ".bili-video-card a",
                ".small-item a",
                ".video-item a"
            ]
            
            found_elements = False
            video_elements = []
            
            for selector in selectors:
                try:
                    elements = driver.find_elements(By.CSS_SELECTOR, selector)
                    if elements:
                        video_elements = elements
                        print(f"✓ 使用选择器 '{selector}' 找到 {len(elements)} 个元素")
                        found_elements = True
                        break
                    else:
                        print(f"✗ 选择器 '{selector}' 没有找到元素")
                except Exception as e:
                    print(f"✗ 选择器 '{selector}' 出错: {e}")
                    continue
            
            if not found_elements:
                print(f"第{page}页未找到任何视频元素")
                
                # 尝试查找是否有其他可能的视频链接
                all_links = driver.find_elements(By.TAG_NAME, "a")
                video_links = [link for link in all_links if link.get_attribute('href') and '/video/BV' in link.get_attribute('href')]
                
                if video_links:
                    print(f"通过搜索所有链接找到 {len(video_links)} 个视频链接")
                    video_elements = video_links
                    found_elements = True
                else:
                    print("页面中没有找到任何视频链接")
                    consecutive_empty_pages += 1
                    
                    # 如果是第一页就没有视频，可能URL有问题
                    if page == 1:
                        print("第一页就没有视频，可能URL不正确或需要登录")
                        # 检查是否需要登录
                        login_elements = driver.find_elements(By.PARTIAL_LINK_TEXT, "登录")
                        if login_elements:
                            print("页面提示需要登录")
                        
                        # 检查是否有错误信息
                        error_elements = driver.find_elements(By.CLASS_NAME, "error")
                        if error_elements:
                            print(f"页面错误信息: {error_elements[0].text}")
                    
                    # 尝试下一页
                    if consecutive_empty_pages < 5:
                        page += 1
                        next_url = f"{url}?pn={page}" if "?" not in url else f"{url}&pn={page}"
                        print(f"尝试访问第{page}页: {next_url}")
                        driver.get(next_url)
                        continue
                    else:
                        break
            
            if found_elements:
                consecutive_empty_pages = 0
                current_page_videos = []
                
                print(f"开始解析 {len(video_elements)} 个视频元素...")
                
                for i, element in enumerate(video_elements):
                    try:
                        href = element.get_attribute('href')
                        if not href or '/video/BV' not in href:
                            continue
                            
                        bv_match = re.search(r'/video/(BV[\w]+)', href)
                        if not bv_match:
                            continue
                            
                        bv_id = bv_match.group(1)
                        
                        # 获取视频标题
                        title = ""
                        try:
                            title = element.get_attribute('title')
                            if not title:
                                title_selectors = [
                                    '.bili-video-card__info--tit',
                                    '.video-name',
                                    '.title',
                                    'p[title]',
                                    '.info .title'
                                ]
                                for title_selector in title_selectors:
                                    try:
                                        title_element = element.find_element(By.CSS_SELECTOR, title_selector)
                                        title = title_element.get_attribute('title') or title_element.text
                                        if title:
                                            break
                                    except:
                                        continue
                            
                            if not title:
                                title = element.get_attribute('aria-label') or f"视频_{bv_id}"
                                
                        except:
                            title = f"视频_{bv_id}"
                        
                        video_info = {
                            "bv": bv_id,
                            "url": href,
                            "title": title.strip(),
                            "page": page
                        }
                        
                        # 避免重复
                        if not any(v["bv"] == bv_id for v in videos):
                            current_page_videos.append(video_info)
                            print(f"  {len(current_page_videos)}. {title[:50]}... - {bv_id}")
                            
                    except Exception as e:
                        print(f"解析第{i+1}个元素出错: {e}")
                        continue
                
                if current_page_videos:
                    videos.extend(current_page_videos)
                    print(f"✓ 第{page}页成功获取 {len(current_page_videos)} 个视频，总计: {len(videos)}")
                else:
                    print(f"✗ 第{page}页没有获取到新视频")
                    consecutive_empty_pages += 1
            
            # 检查是否达到目标数量
            if len(videos) >= max_videos:
                print(f"已达到目标数量 {max_videos}，停止爬取")
                break
            
            # 尝试翻页
            page += 1
            if page <= 50:  # 限制最大页数，避免无限循环
                next_url = f"{url}?pn={page}" if "?" not in url else f"{url}&pn={page}"
                print(f"准备访问第{page}页...")
                driver.get(next_url)
                time.sleep(3)
            else:
                print("已达到最大页数限制(50页)")
                break
        
        driver.quit()
        print(f"\n爬取完成！共获取 {len(videos)} 个视频")
        return videos
            
    except ImportError:
        print("selenium未安装，请运行: pip install selenium")
        return []
    except Exception as e:
        print(f"selenium批量爬取错误: {e}")
        import traceback
        traceback.print_exc()
        return []

def save_videos_to_csv(videos, filename="bilibili_videos.csv"):
    """将视频列表保存到CSV文件"""
    if not videos:
        print("没有视频数据可保存")
        return
        
    with open(filename, 'w', newline='', encoding='utf-8-sig') as csvfile:
        fieldnames = ['序号', 'BV号', '视频标题', '视频链接', '页码']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        
        writer.writeheader()
        for i, video in enumerate(videos, 1):
            writer.writerow({
                '序号': i,
                'BV号': video['bv'],
                '视频标题': video['title'],
                '视频链接': video['url'],
                '页码': video['page']
            })
    
    print(f"已保存 {len(videos)} 个视频到 {filename}")

if __name__ == "__main__":
    # UP主视频页面URL
    up_url = "https://space.bilibili.com/93796936/video"  # 使用/video而不是/upload/video
    
    print("=" * 80)
    print("B站UP主视频批量爬取工具 - 调试版本")
    print("=" * 80)
    print(f"目标UP主: {up_url}")
    print(f"开始时间: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 80)
    
    # 使用selenium批量爬取
    videos = fetch_videos_selenium_debug(up_url)
    
    if videos:
        # 生成带时间戳的文件名
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        csv_filename = f"bilibili_videos_debug_{timestamp}.csv"
        
        # 保存到CSV文件
        save_videos_to_csv(videos, csv_filename)
        
        # 显示统计信息
        print("\n" + "=" * 80)
        print("爬取结果统计:")
        print("=" * 80)
        print(f"总视频数: {len(videos)}")
        print(f"保存文件: {csv_filename}")
        
        # 显示前10个视频
        print(f"\n前10个视频:")
        print("-" * 80)
        for i, video in enumerate(videos[:10], 1):
            print(f"{i:2d}. {video['title'][:60]:60s} | {video['bv']:15s}")
        
        if len(videos) > 10:
            print(f"... 还有 {len(videos) - 10} 个视频")
            
    else:
        print("\n爬取失败，没有获取到视频数据")
        print("可能的原因:")
        print("1. 网络连接问题")
        print("2. UP主ID不存在或没有公开视频")
        print("3. B站需要登录才能查看")
        print("4. 页面结构发生变化")
