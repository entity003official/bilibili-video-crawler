"""
B站爬虫 - 自动化登录处理版本
"""
import time
import csv
import re
from datetime import datetime
import os

def simple_bilibili_crawler():
    """简化的B站爬虫，自动处理登录问题"""
    try:
        from selenium import webdriver
        from selenium.webdriver.common.by import By
        from selenium.webdriver.chrome.options import Options
        
        url = "https://space.bilibili.com/93796936/upload/video"
        
        print("🚀 启动B站视频爬虫...")
        print(f"目标页面: {url}")
        
        # 简化的Chrome配置
        options = Options()
        
        # 尝试使用用户数据目录
        user_data_dir = f"C:/Users/{os.getenv('USERNAME', 'Administrator')}/AppData/Local/Google/Chrome/User Data"
        if os.path.exists(user_data_dir):
            print(f"✓ 使用Chrome用户数据: {user_data_dir}")
            options.add_argument(f'--user-data-dir={user_data_dir}')
            options.add_argument('--profile-directory=Default')
        else:
            print("⚠️ 未找到Chrome用户数据，使用临时配置")
        
        # 基础配置
        options.add_argument('--disable-blink-features=AutomationControlled')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--window-size=1366,768')
        
        # 启动浏览器
        try:
            driver = webdriver.Chrome(options=options)
            print("✓ Chrome浏览器启动成功")
        except Exception as e:
            print(f"❌ 浏览器启动失败: {e}")
            print("请确保已安装Chrome和ChromeDriver")
            return []
        
        # 访问页面
        print("正在访问目标页面...")
        driver.get(url)
        time.sleep(5)
        
        # 检查页面状态
        title = driver.title
        print(f"页面标题: {title}")
        
        # 如果需要登录，给用户时间手动登录
        if any(keyword in title.lower() for keyword in ['登录', 'login']):
            print("🔐 检测到需要登录")
            print("请在打开的浏览器窗口中手动登录B站")
            print("登录完成后，手动访问UP主页面")
            input("完成登录并确认可以看到视频列表后，按Enter继续...")
            
            # 重新获取当前页面
            current_url = driver.current_url
            if 'space.bilibili.com' not in current_url:
                driver.get(url)
                time.sleep(3)
        
        # 开始爬取
        print("🎬 开始爬取视频...")
        all_videos = []
        max_pages = 20
        
        for page in range(1, max_pages + 1):
            print(f"\n📄 爬取第{page}页...")
            
            # 构建URL
            if page == 1:
                page_url = url
            else:
                page_url = f"{url}?pn={page}"
                driver.get(page_url)
                time.sleep(3)
            
            # 滚动页面加载内容
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(2)
            
            # 查找视频链接
            video_links = []
            selectors = [
                "a[href*='/video/BV']",
                "a.bili-cover-card"
            ]
            
            for selector in selectors:
                elements = driver.find_elements(By.CSS_SELECTOR, selector)
                if elements:
                    video_links = elements
                    print(f"  ✓ 找到 {len(elements)} 个视频链接")
                    break
            
            if not video_links:
                print(f"  ❌ 第{page}页无视频，可能已到末尾")
                break
            
            # 解析视频信息
            page_videos = []
            for link in video_links:
                try:
                    href = link.get_attribute('href')
                    if not href or '/video/BV' not in href:
                        continue
                    
                    bv_match = re.search(r'/video/(BV[\w]+)', href)
                    if not bv_match:
                        continue
                    
                    bv_id = bv_match.group(1)
                    title = link.get_attribute('title') or f"视频_{bv_id}"
                    
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
                print(f"  ✓ 获取 {len(page_videos)} 个新视频，总计: {len(all_videos)}")
            else:
                print(f"  ❌ 第{page}页无新视频")
                break
        
        driver.quit()
        return all_videos
        
    except Exception as e:
        print(f"❌ 爬取失败: {e}")
        return []

def save_results(videos):
    """保存结果"""
    if not videos:
        print("❌ 没有数据可保存")
        return None
    
    # 生成文件名
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"bilibili_videos_auto_{timestamp}.csv"
    
    # 保存CSV
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
    
    return filename

def main():
    print("=" * 60)
    print("🎯 B站UP主视频爬取工具 - 自动化版本")
    print("=" * 60)
    
    start_time = datetime.now()
    
    # 爬取视频
    videos = simple_bilibili_crawler()
    
    if videos:
        # 保存结果
        filename = save_results(videos)
        if filename:
            print("\n" + "=" * 60)
            print("🎉 爬取完成！")
            print("=" * 60)
            print(f"✅ 总视频数: {len(videos)}")
            print(f"✅ 保存文件: {filename}")
            print(f"✅ 用时: {datetime.now() - start_time}")
            
            # 显示部分结果
            print(f"\n📺 视频预览 (前8个):")
            print("-" * 60)
            for i, video in enumerate(videos[:8], 1):
                title = video['title'][:35] + "..." if len(video['title']) > 35 else video['title']
                print(f"{i:2d}. {title:40s} | {video['bv']}")
            
            if len(videos) > 8:
                print(f"    ... 还有 {len(videos) - 8} 个视频")
    else:
        print("\n❌ 爬取失败，请检查：")
        print("1. 网络连接是否正常")
        print("2. Chrome浏览器是否正确安装")
        print("3. 是否需要手动登录B站")

if __name__ == "__main__":
    main()
