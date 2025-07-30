"""
B站视频爬虫 - 使用已登录浏览器版本
避免登录弹窗问题
"""
import time
import csv
import re
from datetime import datetime
import os

def get_chrome_user_data_path():
    """获取Chrome用户数据路径"""
    possible_paths = [
        "C:/Users/Administrator/AppData/Local/Google/Chrome/User Data",
        "C:/Users/{}/AppData/Local/Google/Chrome/User Data".format(os.getenv('USERNAME')),
        "~/AppData/Local/Google/Chrome/User Data",
        "~/Library/Application Support/Google/Chrome",  # macOS
        "~/.config/google-chrome"  # Linux
    ]
    
    for path in possible_paths:
        expanded_path = os.path.expanduser(path)
        if os.path.exists(expanded_path):
            return expanded_path
    
    return None

def crawl_with_logged_browser(url, max_videos=500):
    """使用已登录的浏览器爬取"""
    try:
        from selenium import webdriver
        from selenium.webdriver.common.by import By
        from selenium.webdriver.chrome.options import Options
        from webdriver_manager.chrome import ChromeDriverManager
        from selenium.webdriver.chrome.service import Service
        
        print("=" * 60)
        print("B站视频爬取 - 使用已登录浏览器")
        print("=" * 60)
        print(f"目标URL: {url}")
        print(f"最大视频数: {max_videos}")
        
        # 获取Chrome用户数据路径
        user_data_path = get_chrome_user_data_path()
        if not user_data_path:
            print("❌ 未找到Chrome用户数据目录")
            print("请确保已安装Chrome浏览器")
            return []
        
        print(f"✓ 找到Chrome用户数据: {user_data_path}")
        
        # Chrome选项配置
        options = Options()
        
        # 使用现有的用户数据（保持登录状态）
        options.add_argument(f'--user-data-dir={user_data_path}')
        options.add_argument('--profile-directory=Default')
        
        # 反检测配置
        options.add_argument('--disable-blink-features=AutomationControlled')
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option('useAutomationExtension', False)
        
        # 基础配置
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--disable-gpu')
        options.add_argument('--window-size=1366,768')
        
        # 如果需要无头模式，取消下面的注释（建议先测试有头模式）
        # options.add_argument('--headless')
        
        print("正在启动Chrome浏览器...")
        
        try:
            service = Service(ChromeDriverManager().install())
            driver = webdriver.Chrome(service=service, options=options)
        except Exception as e:
            print(f"启动失败: {e}")
            print("尝试直接启动Chrome...")
            driver = webdriver.Chrome(options=options)
        
        # 执行反检测脚本
        driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
        
        print("✓ 浏览器启动成功")
        print("正在访问页面...")
        
        driver.get(url)
        time.sleep(5)
        
        # 检查页面状态
        page_title = driver.title
        current_url = driver.current_url
        
        print(f"页面标题: {page_title}")
        print(f"当前URL: {current_url}")
        
        # 检查是否需要登录
        if any(keyword in page_title.lower() for keyword in ['登录', 'login', '验证']):
            print("❌ 检测到登录页面！")
            print("\n解决方案：")
            print("1. 请先在正常的Chrome浏览器中登录B站")
            print("2. 访问目标UP主页面确认可以正常查看")
            print("3. 关闭所有Chrome窗口后重新运行脚本")
            input("完成上述步骤后，按Enter键继续...")
            driver.get(url)
            time.sleep(3)
        
        print("开始爬取视频...")
        all_videos = []
        page_num = 1
        max_pages = 30  # 限制最大页数
        
        while len(all_videos) < max_videos and page_num <= max_pages:
            # 构建URL
            if page_num == 1:
                current_url = url
            else:
                separator = "&" if "?" in url else "?"
                current_url = f"{url}{separator}pn={page_num}"
            
            print(f"\n[第{page_num}页] 访问: {current_url}")
            
            if page_num > 1:
                driver.get(current_url)
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
                ".video-card a",
                ".bili-video-card a"
            ]
            
            video_links = []
            for selector in video_selectors:
                try:
                    elements = driver.find_elements(By.CSS_SELECTOR, selector)
                    if elements:
                        video_links = elements
                        print(f"  ✓ 使用选择器 '{selector}' 找到 {len(elements)} 个元素")
                        break
                except:
                    continue
            
            if not video_links:
                print(f"  ❌ 第{page_num}页未找到视频")
                if page_num == 1:
                    print("  可能原因：需要登录、页面结构变化、或UP主无视频")
                    # 保存页面源码调试
                    with open(f"debug_page_{page_num}.html", "w", encoding="utf-8") as f:
                        f.write(driver.page_source)
                    print(f"  页面源码已保存到 debug_page_{page_num}.html")
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
                    title = link.get_attribute('title') or link.text or f"视频_{bv_id}"
                    title = title.strip()
                    
                    video_info = {
                        'bv': bv_id,
                        'title': title,
                        'url': href,
                        'page': page_num
                    }
                    
                    # 避免重复
                    if not any(v['bv'] == bv_id for v in all_videos):
                        page_videos.append(video_info)
                
                except Exception as e:
                    continue
            
            if page_videos:
                all_videos.extend(page_videos)
                print(f"  ✓ 第{page_num}页获取 {len(page_videos)} 个新视频，总计: {len(all_videos)}")
                
                # 显示前3个视频标题
                for i, video in enumerate(page_videos[:3]):
                    print(f"    {i+1}. {video['title'][:40]}...")
            else:
                print(f"  ❌ 第{page_num}页无新视频")
                break
            
            page_num += 1
            
            # 避免请求过快
            time.sleep(2)
        
        driver.quit()
        print(f"\n爬取完成！总共获取 {len(all_videos)} 个视频")
        return all_videos
        
    except Exception as e:
        print(f"爬取过程出错: {e}")
        import traceback
        traceback.print_exc()
        return []

def save_videos_to_csv(videos, filename):
    """保存视频到CSV文件"""
    if not videos:
        print("没有视频数据可保存")
        return
    
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
    
    print(f"✓ 已保存 {len(videos)} 个视频到 {filename}")

def main():
    # 配置参数
    up_url = "https://space.bilibili.com/93796936/upload/video"
    max_videos = 500
    
    print("=" * 70)
    print("🎬 B站UP主视频批量爬取工具 - 登录版")
    print("=" * 70)
    print("⚠️  使用前请确保：")
    print("1. 已在Chrome浏览器中登录B站")
    print("2. 可以正常访问目标UP主页面")
    print("3. 关闭所有Chrome窗口")
    print("=" * 70)
    
    # 等待用户确认
    input("确认完成上述准备工作后，按Enter键开始爬取...")
    
    # 开始爬取
    start_time = datetime.now()
    videos = crawl_with_logged_browser(up_url, max_videos)
    
    if videos:
        # 保存结果
        timestamp = start_time.strftime("%Y%m%d_%H%M%S")
        filename = f"bilibili_videos_logged_{timestamp}.csv"
        save_videos_to_csv(videos, filename)
        
        # 显示统计
        print("\n" + "=" * 70)
        print("📊 爬取结果统计")
        print("=" * 70)
        print(f"✓ 成功爬取视频数: {len(videos)}")
        print(f"✓ 保存文件: {filename}")
        print(f"✓ 耗时: {datetime.now() - start_time}")
        
        # 显示部分视频
        print(f"\n📺 视频列表预览 (前10个):")
        print("-" * 70)
        for i, video in enumerate(videos[:10], 1):
            title = video['title'][:45] + "..." if len(video['title']) > 45 else video['title']
            print(f"{i:2d}. {title:50s} | {video['bv']}")
        
        if len(videos) > 10:
            print(f"... 还有 {len(videos) - 10} 个视频")
            
    else:
        print("\n❌ 爬取失败")
        print("可能的解决方案：")
        print("1. 检查网络连接")
        print("2. 确认已登录B站")
        print("3. 检查UP主ID是否正确")
        print("4. 查看调试文件 debug_page_1.html")

if __name__ == "__main__":
    main()
