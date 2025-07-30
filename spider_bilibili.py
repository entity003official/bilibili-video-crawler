import requests
from bs4 import BeautifulSoup
import re
import time
import csv
from urllib.parse import urljoin

def fetch_videos_selenium(url, max_videos=50):
    """
    使用selenium批量爬取up主的视频
    :param url: up主视频页面URL 
    :param max_videos: 最大爬取视频数量
    :return: 视频列表
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
        
        # Chrome选项 - 使用已登录的浏览器配置
        options = Options()
        # 使用现有的Chrome用户数据目录，这样可以保持登录状态
        # 注意：请先手动登录Chrome浏览器并访问B站
        options.add_argument('--user-data-dir=C:/Users/Administrator/AppData/Local/Google/Chrome/User Data')
        options.add_argument('--profile-directory=Default')  # 使用默认配置文件
        
        # 如果仍需要无头模式，可以启用下面这行（但建议先测试有头模式）
        # options.add_argument('--headless')  
        
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--disable-gpu')
        options.add_argument('--window-size=1920,1080')
        options.add_argument('--disable-blink-features=AutomationControlled')  # 避免被检测为自动化
        options.add_experimental_option("excludeSwitches", ["enable-automation"])  # 移除自动化标识
        options.add_experimental_option('useAutomationExtension', False)  # 禁用自动化扩展
        options.add_argument('--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36')
        
        # 使用webdriver-manager自动管理ChromeDriver
        try:
            service = Service(ChromeDriverManager().install())
            driver = webdriver.Chrome(service=service, options=options)
        except Exception as e:
            print(f"使用webdriver-manager启动失败: {e}")
            print("尝试直接使用Chrome...")
            driver = webdriver.Chrome(options=options)
        
        print("浏览器启动成功，正在访问页面...")
        driver.get(url)
        
        # 检查是否需要登录
        time.sleep(3)
        page_title = driver.title
        current_url = driver.current_url
        
        print(f"页面标题: {page_title}")
        print(f"当前URL: {current_url}")
        
        # 检查是否跳转到登录页面
        if "登录" in page_title or "login" in current_url.lower():
            print("⚠️  检测到需要登录！")
            print("请按以下步骤操作：")
            print("1. 手动在Chrome浏览器中登录B站")
            print("2. 确保可以正常访问UP主页面")
            print("3. 重新运行此脚本")
            print("🔄 继续尝试爬取（可能需要手动在浏览器中登录）...")
            # 给用户一些时间手动登录，而不是停止程序
            time.sleep(10)
            # 尝试重新访问页面
            driver.get(url)
            time.sleep(5)
        
        # 等待页面加载
        wait = WebDriverWait(driver, 10)
        
        videos = []
        page = 1
        consecutive_empty_pages = 0  # 连续空页面计数器
        
        while len(videos) < max_videos and consecutive_empty_pages < 3:
            print(f"正在爬取第{page}页...")
            
            # 等待视频列表加载
            time.sleep(2)
            
            # 尝试多种选择器获取所有视频
            selectors = [
                "a.bili-cover-card",
                "a[href*='/video/BV']",
                "a[href*='bilibili.com/video']",
                ".video-card a",
                ".bili-video-card a"
            ]
            
            video_elements = []
            for selector in selectors:
                try:
                    elements = driver.find_elements(By.CSS_SELECTOR, selector)
                    if elements:
                        video_elements = elements
                        print(f"使用选择器 {selector} 找到 {len(elements)} 个视频")
                        break
                except:
                    continue
            
            if not video_elements:
                print(f"第{page}页未找到视频元素")
                consecutive_empty_pages += 1
                # 如果连续多页都没有视频，可能已经到底了
                if consecutive_empty_pages >= 3:
                    print("连续3页没有找到视频，可能已到最后一页")
                    break
                # 继续尝试下一页
                page += 1
                continue
            else:
                consecutive_empty_pages = 0  # 重置计数器
            
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
                    
                    # 获取视频标题（尝试多种方式）
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
                            # 最后尝试从aria-label获取
                            title = element.get_attribute('aria-label') or f"视频_{bv_id}"
                            
                    except:
                        title = f"视频_{bv_id}"
                    
                    video_info = {
                        "bv": bv_id,
                        "url": href,
                        "title": title.strip(),
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
                consecutive_empty_pages = 0  # 重置计数器
                videos.extend(current_page_videos)
                print(f"第{page}页获取了 {len(current_page_videos)} 个视频，总计: {len(videos)}")
                
            # 检查是否已达到目标数量
            if len(videos) >= max_videos:
                videos = videos[:max_videos]  # 截取到指定数量
                break
            
            # 尝试翻页
            try:
                # 滚动到页面底部，触发懒加载
                driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                time.sleep(2)
                
                # 再次滚动确保加载完成
                driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                time.sleep(2)
                
                # 检查是否有"加载更多"按钮或翻页按钮
                load_more_selectors = [
                    ".load-more-btn",
                    ".pagination-btn-next", 
                    ".page-next",
                    "button[aria-label='下一页']",
                    ".be-pager-next",
                    ".bili-pagination .bili-pagination-next"
                ]
                
                clicked = False
                for selector in load_more_selectors:
                    try:
                        button = driver.find_element(By.CSS_SELECTOR, selector)
                        if button.is_enabled() and button.is_displayed():
                            driver.execute_script("arguments[0].click();", button)
                            clicked = True
                            print(f"点击了翻页按钮: {selector}")
                            time.sleep(3)
                            break
                    except:
                        continue
                
                if not clicked:
                    # 如果没有翻页按钮，尝试修改URL翻页
                    next_page = page + 1
                    if "pn=" in url:
                        new_url = re.sub(r'pn=\d+', f'pn={next_page}', url)
                    else:
                        separator = "&" if "?" in url else "?"
                        new_url = f"{url}{separator}pn={next_page}"
                    
                    print(f"尝试访问第{next_page}页: {new_url}")
                    driver.get(new_url)
                    time.sleep(3)
                
                page += 1
                
            except Exception as e:
                print(f"翻页失败: {e}")
                consecutive_empty_pages += 1
                if consecutive_empty_pages >= 3:
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

def fetch_first_video(url):
    print(f"正在爬取: {url}")
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
        "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
        "Accept-Encoding": "gzip, deflate, br",
        "DNT": "1",
        "Connection": "keep-alive",
        "Upgrade-Insecure-Requests": "1",
        "Cache-Control": "max-age=0"
    }
    session = requests.Session()
    session.headers.update(headers)
    resp = session.get(url, timeout=15)
    resp.raise_for_status()
    resp.raise_for_status()
    soup = BeautifulSoup(resp.text, "html.parser")
    
    # 调试：保存HTML到文件查看结构
    with open("debug_html.html", "w", encoding="utf-8") as f:
        f.write(resp.text)
    print("HTML已保存到debug_html.html，请检查结构")
    
    # 尝试多种可能的选择器
    selectors = [
        ("a.bili-cover-card", "bili-cover-card类"),
        ("a[href*='/video/BV']", "包含BV的链接"),
        ("a[href*='bilibili.com/video']", "B站视频链接"),
        (".video-item a", "video-item下的链接"),
        (".video-card a", "video-card下的链接")
    ]
    
    for selector, desc in selectors:
        video_a = soup.select_one(selector)
        if video_a:
            print(f"使用选择器 {desc} 找到视频")
            break
    else:
        print("所有选择器都未找到视频，可能需要JavaScript渲染")
        return None
    if video_a:
        href = video_a["href"]
        # 处理相对链接
        if href.startswith("//"):
            href = "https:" + href
        bv_match = re.search(r"/video/(BV[\w]+)", href)
        bv_id = bv_match.group(1) if bv_match else ""
        print(f"BV号: {bv_id}")
        print(f"视频链接: {href}")
        return {"bv": bv_id, "url": href}
    else:
        print("未找到视频条目")
        return None

def save_videos_to_csv(videos, filename="bilibili_videos.csv"):
    """
    将视频列表保存到CSV文件
    """
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
    # 在此填写up主空间url，如 https://space.bilibili.com/xxxx/video
    up_url = "https://space.bilibili.com/93796936/upload/video"
    
    # 设置要爬取的视频数量 - 设置为很大的数字来获取所有视频
    max_videos = 1000  # 设置较大数字，实际会在没有更多视频时自动停止
    
    print(f"开始批量爬取up主视频，目标数量: {max_videos} (实际会在没有更多视频时停止)")
    print(f"UP主链接: {up_url}")
    
    # 使用selenium批量爬取
    videos = fetch_videos_selenium(up_url, max_videos)
    
    if videos:
        # 生成带时间戳的文件名
        import datetime
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        csv_filename = f"bilibili_videos_all_{timestamp}.csv"
        
        # 保存到CSV文件
        save_videos_to_csv(videos, csv_filename)
        
        # 显示前几个视频作为示例
        print("\n前5个视频示例:")
        for i, video in enumerate(videos[:5], 1):
            print(f"{i}. {video['title']} - {video['bv']} - {video['url']}")
            
        print(f"\n总计成功爬取 {len(videos)} 个视频")
    else:
        print("爬取失败，没有获取到视频数据")
