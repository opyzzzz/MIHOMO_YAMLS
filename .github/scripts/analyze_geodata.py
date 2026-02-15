import os
import json
import subprocess
import datetime
import shutil

# 定义工作目录
WORKSPACE_DIR = "workspace"
OLD_STATS_FILE = "old_data/stats.json"
# 新的 stats 文件存放在 workspace 根目录，用于推送到仓库
STATS_FILE = os.path.join(WORKSPACE_DIR, "stats.json")

def run_command(cmd):
    """运行系统命令"""
    try:
        subprocess.check_call(cmd, shell=True, stderr=subprocess.DEVNULL, stdout=subprocess.DEVNULL)
    except subprocess.CalledProcessError:
        print(f"⚠️ Warning: Command failed: {cmd}")

def count_lines(filepath):
    """计算文件行数"""
    try:
        with open(filepath, 'rb') as f:
            return sum(1 for _ in f)
    except:
        return 0

def process_dat_files():
    """遍历目录，解包 dat 文件，并返回统计数据"""
    current_stats = {}
    
    # 遍历 workspace 下的所有作者目录
    for author in os.listdir(WORKSPACE_DIR):
        author_path = os.path.join(WORKSPACE_DIR, author)
        # 排除非文件夹或隐藏文件夹
        if not os.path.isdir(author_path) or author.startswith("."):
            continue
            
        print(f"🔍 Analyzing {author}...")
        current_stats[author] = {}

        # 遍历作者目录下的子文件夹 (geoip, geosite)
        for category in ["geoip", "geosite"]:
            cat_dir = os.path.join(author_path, category)
            if not os.path.exists(cat_dir):
                continue
                
            # 找到目录下的 .dat 文件
            for file in os.listdir(cat_dir):
                if not file.endswith(".dat"):
                    continue
                
                dat_path = os.path.join(cat_dir, file)
                # 创建导出目录 (例如 workspace/MetaCubeX/geoip/geoip_text)
                # 注意：为了目录整洁，建议把解包的文本放在单独文件夹，避免污染
                export_dir = os.path.join(cat_dir, f"{file}_text")
                if os.path.exists(export_dir):
                    shutil.rmtree(export_dir)
                os.makedirs(export_dir, exist_ok=True)
                
                print(f"  -> Extracting {file}...")
                
                mode = "geoip" if "geoip" in file.lower() else "geosite"
                
                try:
                    # 使用 v2dat 解包
                    run_command(f"v2dat unpack {mode} -o {export_dir} {dat_path}")
                    
                    # 统计解包后的文件
                    if os.path.exists(export_dir):
                        files = os.listdir(export_dir)
                        # 这里我们统计所有解包出来的 txt 文件，不仅仅是热门的
                        # 因为现在有分页了，数据多一点也没关系
                        for tag_file in files:
                            if not tag_file.endswith(".txt"): continue
                            
                            tag_name = os.path.splitext(tag_file)[0]
                            full_path = os.path.join(export_dir, tag_file)
                            count = count_lines(full_path)
                            
                            # 记录格式： "geoip.dat::CN": 5000
                            current_stats[author][f"{file}::{tag_name}"] = count
                                
                except Exception as e:
                    print(f"Failed to unpack {file}: {e}")

    return current_stats

def generate_reports(current_stats, old_stats):
    """生成主 README 和 作者子 README"""
    
    update_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    # --- 1. 生成主页 README.md (Root) ---
    root_lines = [
        "# 🌍 GeoData Assets Collection", 
        "", 
        f"> Last Updated: {update_time} (UTC+8)",
        "",
        "## 📂 规则集概览 / Overview",
        "",
        "| 数据来源 (Author) | 包含规则集数量 | 详细报告 |",
        "|---|---|---|"
    ]

    # --- 2. 遍历每个作者，生成子页 README，并更新主页行 ---
    for author, rules in sorted(current_stats.items()):
        if not rules: 
            continue
            
        rule_count = len(rules)
        # 主页表格添加一行
        # 注意链接写法： ./AuthorName/README.md
        root_lines.append(f"| **{author}** | {rule_count} 个 | [查看详情 / View Details](./{author}/README.md) |")
        
        # --- 生成子页内容 ---
        author_lines = [
            f"# 📊 {author} - 详细规则统计",
            "",
            f"> 更新时间: {update_time}",
            f"> [🔙 返回主页 / Back to Home](../README.md)", 
            "",
            "## 📈 规则变动详情",
            "",
            "| 规则文件::标签 | 当前条目数 | 较昨日变化 |",
            "|---|---|---|"
        ]
        
        # 填充子页表格
        for key, count in sorted(rules.items()):
            # key 格式为 "geoip.dat::cn"
            old_count = old_stats.get(author, {}).get(key, 0)
            diff = count - old_count
            
            diff_str = "-"
            if diff > 0: 
                diff_str = f"🔺 +{diff}"
            elif diff < 0: 
                diff_str = f"🔻 {diff}"
            elif old_count == 0:
                diff_str = "🆕 New"
            
            author_lines.append(f"| {key} | {count} | {diff_str} |")
        
        author_lines.append("")
        author_lines.append("## 📥 如何使用")
        author_lines.append(f"此目录包含了 `{author}` 的原始 `.dat` 文件以及解包后的文本规则。")
        
        # 写入子页 README
        author_readme_path = os.path.join(WORKSPACE_DIR, author, "README.md")
        with open(author_readme_path, "w", encoding='utf-8') as f:
            f.write("\n".join(author_lines))

    # 写入主页 README
    root_readme_path = os.path.join(WORKSPACE_DIR, "README.md")
    with open(root_readme_path, "w", encoding='utf-8') as f:
        f.write("\n".join(root_lines))
    
    # 保存 stats.json
    with open(STATS_FILE, "w", encoding='utf-8') as f:
        json.dump(current_stats, f, indent=2)

def main():
    print("⏳ Loading old stats...")
    old_stats = {}
    if os.path.exists(OLD_STATS_FILE):
        try:
            with open(OLD_STATS_FILE, 'r') as f:
                old_stats = json.load(f)
        except:
            print("Old stats file corrupted, skipping diff.")

    print("⏳ Processing assets...")
    current_stats = process_dat_files()
    
    print("⏳ Generating reports...")
    generate_reports(current_stats, old_stats)
    print("✅ Done.")

if __name__ == "__main__":
    main()
