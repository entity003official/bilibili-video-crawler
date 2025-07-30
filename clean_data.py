"""
数据去重和清理工具
"""
import csv
import pandas as pd
from datetime import datetime

def remove_duplicates_from_csv(input_file, output_file=None):
    """从CSV文件中去除重复数据"""
    try:
        # 读取CSV文件
        df = pd.read_csv(input_file, encoding='utf-8-sig')
        
        print(f"原始数据: {len(df)} 行")
        print(f"字段: {list(df.columns)}")
        
        # 基于BV号去重，保留第一次出现的记录
        df_unique = df.drop_duplicates(subset=['BV号'], keep='first')
        
        print(f"去重后: {len(df_unique)} 行")
        print(f"移除重复: {len(df) - len(df_unique)} 行")
        
        # 重新编号
        df_unique = df_unique.reset_index(drop=True)
        df_unique['序号'] = range(1, len(df_unique) + 1)
        
        # 生成输出文件名
        if not output_file:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_file = f"bilibili_videos_cleaned_{timestamp}.csv"
        
        # 保存去重后的数据
        df_unique.to_csv(output_file, index=False, encoding='utf-8-sig')
        
        print(f"✅ 清理完成，保存到: {output_file}")
        
        # 显示前几条数据
        print("\n📺 前10个视频:")
        print("-" * 80)
        for i, row in df_unique.head(10).iterrows():
            title = row['视频标题'][:50] + "..." if len(str(row['视频标题'])) > 50 else row['视频标题']
            print(f"{row['序号']:2d}. {title:55s} | {row['BV号']}")
        
        if len(df_unique) > 10:
            print(f"    ... 还有 {len(df_unique) - 10} 个视频")
        
        return output_file
        
    except Exception as e:
        print(f"❌ 处理失败: {e}")
        return None

def analyze_csv_data(filename):
    """分析CSV数据"""
    try:
        df = pd.read_csv(filename, encoding='utf-8-sig')
        
        print("=" * 60)
        print(f"📊 数据分析: {filename}")
        print("=" * 60)
        print(f"总记录数: {len(df)}")
        print(f"字段数: {len(df.columns)}")
        print(f"字段名: {list(df.columns)}")
        
        if 'BV号' in df.columns:
            unique_bv = df['BV号'].nunique()
            total_bv = len(df)
            print(f"唯一BV号: {unique_bv}")
            print(f"重复记录: {total_bv - unique_bv}")
        
        if '页码' in df.columns:
            page_counts = df['页码'].value_counts().sort_index()
            print(f"页面分布: {dict(page_counts)}")
        
        print("=" * 60)
        
    except Exception as e:
        print(f"❌ 分析失败: {e}")

def main():
    print("🧹 B站视频数据清理工具")
    print("=" * 60)
    
    # 查找所有bilibili视频CSV文件
    import glob
    csv_files = glob.glob("bilibili_videos*.csv")
    
    if not csv_files:
        print("❌ 未找到bilibili视频CSV文件")
        return
    
    print("📁 找到以下CSV文件:")
    for i, file in enumerate(csv_files, 1):
        print(f"{i}. {file}")
    
    # 处理最新的文件
    latest_file = max(csv_files, key=lambda x: x.split('_')[-1] if '_' in x else x)
    print(f"\n🎯 处理最新文件: {latest_file}")
    
    # 分析原始数据
    analyze_csv_data(latest_file)
    
    # 去重处理
    print("\n🧹 开始去重处理...")
    cleaned_file = remove_duplicates_from_csv(latest_file)
    
    if cleaned_file:
        print(f"\n✅ 处理完成！")
        print(f"原文件: {latest_file}")
        print(f"清理后: {cleaned_file}")
    
    # 提供所有文件的快速分析
    print("\n📈 所有文件快速统计:")
    print("-" * 60)
    for file in csv_files:
        try:
            df = pd.read_csv(file, encoding='utf-8-sig')
            unique_count = df['BV号'].nunique() if 'BV号' in df.columns else 0
            total_count = len(df)
            print(f"{file:35s} | 总计:{total_count:3d} | 唯一:{unique_count:3d} | 重复:{total_count-unique_count:3d}")
        except:
            print(f"{file:35s} | 读取失败")

if __name__ == "__main__":
    main()
