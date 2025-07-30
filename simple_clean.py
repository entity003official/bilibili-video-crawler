import csv

def clean_csv():
    input_file = 'bilibili_videos_simple_20250730_103945.csv'
    output_file = 'bilibili_videos_final_cleaned.csv'
    
    seen_bv = set()
    cleaned_data = []
    
    with open(input_file, 'r', encoding='utf-8-sig') as f:
        reader = csv.DictReader(f)
        for row in reader:
            bv_id = row['BV号']
            if bv_id not in seen_bv:
                seen_bv.add(bv_id)
                cleaned_data.append(row)
    
    # 重新编号
    for i, row in enumerate(cleaned_data, 1):
        row['序号'] = i
    
    # 保存清理后的数据
    with open(output_file, 'w', newline='', encoding='utf-8-sig') as f:
        if cleaned_data:
            fieldnames = cleaned_data[0].keys()
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(cleaned_data)
    
    print(f"去重完成: {len(cleaned_data)} 个唯一视频")
    print(f"保存到: {output_file}")
    
    # 显示前10个
    for i, video in enumerate(cleaned_data[:10], 1):
        print(f"{i:2d}. {video['BV号']} - {video['视频标题']}")

if __name__ == "__main__":
    clean_csv()
