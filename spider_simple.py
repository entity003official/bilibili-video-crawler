"""
简化版B站爬虫 - 基于之前成功的版本
"""
import time
import csv
import re
from datetime import datetime

def crawl_bilibili_simple():
    """简化版爬虫"""
    try:
        from selenium import webdriver
        from selenium.webdriver.common.by import By
        from selenium.webdriver.chrome.options import Options
        from webdriver_manager.chrome import ChromeDriverManager
        from selenium.webdriver.chrome.service import Service
        
        # 使用你指定的URL
        url = "https://space.bilibili.com/93796936/upload/video"
        print(f"开始爬取: {url}")
        
        # Chrome选项 - 使用之前成功的配置
        options = Options()
        options.add_argument('--headless')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36')
        
        # 启动浏览器
        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=options)
        
        all_videos = []
        page = 1
        max_pages = 20  # 限制最大页数
        
        while page <= max_pages:
            # 构建URL
            if page == 1:
                current_url = url
            else:
                current_url = f"{url}?pn={page}"
            
            print(f"正在爬取第{page}页: {current_url}")
            driver.get(current_url)
            time.sleep(3)
            
            # 尝试找到视频链接
            video_links = driver.find_elements(By.CSS_SELECTOR, "a[href*='/video/BV']")
            
            if not video_links:
                print(f"第{page}页没有找到视频，尝试其他选择器...")
                # 尝试其他选择器
                video_links = driver.find_elements(By.CSS_SELECTOR, "a.bili-cover-card")
            
            if not video_links:
                print(f"第{page}页仍然没有找到视频，可能已到末尾")
                if page == 1:
                    print("第一页就没有视频，可能URL有问题")
                    # 保存页面源码用于调试
                    with open(f"debug_page_{page}.html", "w", encoding="utf-8") as f:
                        f.write(driver.page_source)
                    print(f"页面源码已保存到 debug_page_{page}.html")
                break
            
            print(f"第{page}页找到 {len(video_links)} 个视频链接")
            
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
                    title = link.get_attribute('title') or f"视频_{bv_id}"
                    
                    video_info = {
                        'bv': bv_id,
                        'title': title,
                        'url': href,
                        'page': page
                    }
                    
                    # 避免重复
                    if not any(v['bv'] == bv_id for v in all_videos):
                        page_videos.append(video_info)
                        
                except Exception as e:
                    print(f"处理链接时出错: {e}")
                    continue
            
            if page_videos:
                all_videos.extend(page_videos)
                print(f"第{page}页成功获取 {len(page_videos)} 个视频，总计: {len(all_videos)}")
            else:
                print(f"第{page}页没有获取到新视频")
                break
            
            page += 1
        
        driver.quit()
        return all_videos
        
    except Exception as e:
        print(f"爬取出错: {e}")
        return []

def save_to_csv(videos, filename):
    """保存到CSV文件"""
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
    
    print(f"已保存 {len(videos)} 个视频到 {filename}")

if __name__ == "__main__":
    print("=" * 60)
    print("B站UP主视频爬取工具 - 简化版")
    print("=" * 60)
    
    start_time = datetime.now()
    print(f"开始时间: {start_time.strftime('%Y-%m-%d %H:%M:%S')}")
    
    # 开始爬取
    videos = crawl_bilibili_simple()
    
    if videos:
        # 保存结果
        timestamp = start_time.strftime("%Y%m%d_%H%M%S")
        filename = f"bilibili_videos_simple_{timestamp}.csv"
        save_to_csv(videos, filename)
        
        # 显示结果
        print("\n" + "=" * 60)
        print(f"爬取完成！共获取 {len(videos)} 个视频")
        print(f"文件保存为: {filename}")
        
        # 显示前5个视频
        print("\n前5个视频:")
        for i, video in enumerate(videos[:5], 1):
            print(f"{i}. {video['title'][:50]} - {video['bv']}")
    else:
        print("爬取失败，没有获取到视频数据")
    
    end_time = datetime.now()
    print(f"\n结束时间: {end_time.strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"总耗时: {end_time - start_time}")
