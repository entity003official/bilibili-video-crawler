"""
B站爬虫 - 无交互自动运行版本
直接开始爬取，无需用户按键确认
"""
import time
import csv
import re
from datetime import datetime
import os

def auto_crawl_bilibili():
    """自动开始爬取，无需用户交互"""
    try:
        from selenium import webdriver
        from selenium.webdriver.common.by import By
        from selenium.webdriver.chrome.options import Options
        from webdriver_manager.chrome import ChromeDriverManager
        from selenium.webdriver.chrome.service import Service
        
        url = "https://space.bilibili.com/93796936/upload/video"
        
        print("🚀 B站视频自动爬取工具启动")
        print(f"目标UP主: {url}")
        print(f"开始时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("=" * 60)
        
        # Chrome配置
        options = Options()
        
        # 尝试使用用户数据目录保持登录状态
        user_data_dir = f"C:/Users/{os.getenv('USERNAME', 'Administrator')}/AppData/Local/Google/Chrome/User Data"
        if os.path.exists(user_data_dir):
            print(f"✓ 使用Chrome用户数据保持登录状态")
            options.add_argument(f'--user-data-dir={user_data_dir}')
            options.add_argument('--profile-directory=Default')
        
        # 反检测配置
        options.add_argument('--disable-blink-features=AutomationControlled')
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option('useAutomationExtension', False)
        
        # 基础配置
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--window-size=1366,768')
        
        # 无头模式（可选）- 如果不想看到浏览器窗口，取消注释
        # options.add_argument('--headless')
        
        print("正在启动Chrome浏览器...")
        
        try:
            service = Service(ChromeDriverManager().install())
            driver = webdriver.Chrome(service=service, options=options)
        except Exception as e:
            print(f"webdriver-manager失败，尝试直接启动: {e}")
            driver = webdriver.Chrome(options=options)
        
        # 执行反检测脚本
        driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
        
        print("✓ 浏览器启动成功")
        print("正在访问UP主页面...")
        
        driver.get(url)
        time.sleep(5)
        
        # 检查登录状态
        page_title = driver.title
        current_url = driver.current_url
        
        print(f"页面标题: {page_title}")
        
        # 如果需要登录，等待一段时间让用户手动登录
        if any(keyword in page_title.lower() for keyword in ['登录', 'login']):
            print("⚠️  检测到登录页面")
            print("🔄 等待30秒，请在浏览器中手动登录...")
            for i in range(30, 0, -1):
                print(f"剩余等待时间: {i}秒", end='\r')
                time.sleep(1)
            print("\n继续尝试爬取...")
            driver.get(url)
            time.sleep(3)
        
        print("🎬 开始爬取视频数据...")
        
        all_videos = []
        max_pages = 25  # 限制最大页数
        
        for page in range(1, max_pages + 1):
            print(f"\n📄 正在爬取第{page}页...")
            
            # 构建分页URL
            if page > 1:
                page_url = f"{url}?pn={page}"
                driver.get(page_url)
                time.sleep(3)
            
            # 滚动页面确保内容加载
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(2)
            driver.execute_script("window.scrollTo(0, 0);")
            time.sleep(1)
            
            # 查找视频链接
            video_selectors = [
                "a[href*='/video/BV']",
                "a.bili-cover-card",
                ".video-card a"
            ]
            
            video_links = []
            for selector in video_selectors:
                try:
                    elements = driver.find_elements(By.CSS_SELECTOR, selector)
                    if elements:
                        video_links = elements
                        print(f"  ✓ 使用选择器 '{selector}' 找到 {len(elements)} 个视频")
                        break
                except:
                    continue
            
            if not video_links:
                print(f"  ❌ 第{page}页未找到视频")
                if page == 1:
                    print("  可能需要登录或页面结构发生变化")
                    # 保存调试信息
                    with open(f"debug_page_{page}.html", "w", encoding="utf-8") as f:
                        f.write(driver.page_source)
                    print(f"  已保存调试文件: debug_page_{page}.html")
                break
            
            # 解析视频信息
            page_videos = []
            for link in video_links:
                try:
                    href = link.get_attribute('href')
                    if not href or '/video/BV' not in href:
                        continue
                    
                    # 提取BV号
                    bv_match = re.search(r'/video/(BV[\w]+)', href)
                    if not bv_match:
                        continue
                    
                    bv_id = bv_match.group(1)
                    
                    # 获取标题
                    title = link.get_attribute('title') or link.text.strip() or f"视频_{bv_id}"
                    
                    # 避免重复
                    if not any(v['bv'] == bv_id for v in all_videos):
                        page_videos.append({
                            'bv': bv_id,
                            'title': title.strip(),
                            'url': href,
                            'page': page
                        })
                
                except Exception:
                    continue
            
            if page_videos:
                all_videos.extend(page_videos)
                print(f"  ✓ 第{page}页获取 {len(page_videos)} 个新视频，总计: {len(all_videos)}")
                
                # 显示前3个视频标题作为确认
                for i, video in enumerate(page_videos[:3]):
                    title_preview = video['title'][:30] + "..." if len(video['title']) > 30 else video['title']
                    print(f"    - {title_preview}")
            else:
                print(f"  ❌ 第{page}页无新视频，可能已到末尾")
                break
            
            # 短暂延迟避免请求过快
            time.sleep(1)
        
        driver.quit()
        
        print(f"\n🎉 爬取完成！")
        print(f"总计获取: {len(all_videos)} 个视频")
        
        return all_videos
        
    except Exception as e:
        print(f"❌ 爬取过程出错: {e}")
        import traceback
        traceback.print_exc()
        return []

def save_to_csv(videos):
    """保存到CSV文件"""
    if not videos:
        print("❌ 没有数据可保存")
        return None
    
    # 生成文件名
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"bilibili_videos_auto_{timestamp}.csv"
    
    with open(filename, 'w', newline='', encoding='utf-8-sig') as f:
        writer = csv.DictWriter(f, fieldnames=['序号', 'BV号', '视频标题', '视频链接', '页码'])
        writer.writeheader()
        
        for i, video in enumerate(videos, 1):
            writer.writerow({
                '序号': i,
                'BV号': video['bv'],
                '视频标题': video['title'],
                '视频链接': video['url'],
                '页码': video['page']
            })
    
    print(f"✅ 数据已保存到: {filename}")
    return filename

def main():
    print("=" * 70)
    print("🎯 B站UP主视频自动爬取工具")
    print("=" * 70)
    
    start_time = datetime.now()
    
    # 自动开始爬取
    videos = auto_crawl_bilibili()
    
    if videos:
        # 保存结果
        filename = save_to_csv(videos)
        
        if filename:
            # 显示统计信息
            end_time = datetime.now()
            duration = end_time - start_time
            
            print("\n" + "=" * 70)
            print("📊 爬取结果统计")
            print("=" * 70)
            print(f"✅ 成功爬取: {len(videos)} 个视频")
            print(f"✅ 保存文件: {filename}")
            print(f"✅ 开始时间: {start_time.strftime('%H:%M:%S')}")
            print(f"✅ 结束时间: {end_time.strftime('%H:%M:%S')}")
            print(f"✅ 总耗时: {duration}")
            
            # 显示视频预览
            print(f"\n📺 视频列表预览 (前10个):")
            print("-" * 70)
            for i, video in enumerate(videos[:10], 1):
                title = video['title'][:40] + "..." if len(video['title']) > 40 else video['title']
                print(f"{i:2d}. {title:45s} | {video['bv']}")
            
            if len(videos) > 10:
                print(f"     ... 还有 {len(videos) - 10} 个视频")
                
    else:
        print("\n❌ 爬取失败")
        print("可能的原因:")
        print("1. 需要手动登录B站")
        print("2. 网络连接问题") 
        print("3. UP主设置了隐私权限")
        print("4. 页面结构发生变化")

if __name__ == "__main__":
    main()
