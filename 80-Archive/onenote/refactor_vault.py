from collections import Counter, defaultdict
from dataclasses import dataclass
from pathlib import Path
import re


ROOT = Path.cwd()
VAULT = ROOT / "Obsidian_Vault"
CATEGORIES = ["来源", "概念", "方法", "模型", "洞察"]
REPORT = VAULT / "Refactor_Report.md"

FRONTMATTER = "---\ntype: concept\nstatus: merged\n---\n\n"


@dataclass
class Topic:
    name: str
    category: str
    patterns: list[str]
    related: list[str]


TOPICS = [
    Topic("薄膜铌酸锂调制器", "方法", [
        "tfln", "lithium niobate", "铌酸锂", "v-cm", "消光比", "i-line", "ebl",
        "刻蚀", "电极间隙", "光学损耗", "调制器", "制备与测量", "本文工作亮点",
        "器件设计", "研究启发",
    ], ["光学微腔与 Purcell 效应", "XPS UPS 与能级测量", "Python 数据平滑绘图"]),
    Topic("α-tellurene 量子点", "概念", [
        "tellurene", "量子点", "载流子迁移率", "量子限域", "局域场效应",
        "可调节的带隙", "优异的光学性质",
    ], ["半导体光吸收机制", "光子晶体能带与模式选择", "XPS UPS 与能级测量"]),
    Topic("半导体光吸收机制", "模型", [
        "本征吸收", "激子", "自由载流子", "杂质吸收", "晶格振动", "禁带宽度",
        "半导体材料对光的吸收", "光子能量", "导带", "价带", "电子-空穴",
        "图1.", "图2.", "图3.", "图4.", "eg",
    ], ["α-tellurene 量子点", "XPS UPS 与能级测量", "增益带宽与单模激光"]),
    Topic("XPS UPS 与能级测量", "方法", [
        "ups", "x射线光电子", "xps", "光电子", "结合能", "谱峰", "真空能级",
        "homo-lumo", "fundamental gap", "optical gap", "欧姆接触", "肖特基",
        "横坐标：电子束缚能", "纵坐标：cps", "本底为轫致辐射",
    ], ["半导体光吸收机制", "薄膜铌酸锂调制器", "扫描隧道谱 STS"]),
    Topic("扫描隧道谱 STS", "方法", [
        "扫描隧道谱", "sts", "di dv", "dI dV", "隧穿", "局域态密度", "泡利原理",
        "针尖", "锁相放大",
    ], ["XPS UPS 与能级测量", "电磁腔本征模式与边界条件", "半导体光吸收机制"]),
    Topic("拉曼与手性光学", "概念", [
        "拉曼", "手性光学", "圆偏振", "弹性散射", "非弹性散射",
    ], ["XPS UPS 与能级测量", "半导体光吸收机制", "光学微腔与 Purcell 效应"]),
    Topic("压电陶瓷材料性质", "概念", [
        "压电陶瓷", "压电效应", "介电性", "弹性系数", "极化强度", "电介质",
        "钛酸钡", "锆钛酸铅", "sr1-x", "nb2o5", "胡克定律",
    ], ["材料物性与功能陶瓷", "XPS UPS 与能级测量", "半导体光吸收机制"]),
    Topic("增益带宽与单模激光", "概念", [
        "增益带宽", "光学增益带宽", "gain curve", "fsr", "free spectral range",
        "自由光谱范围", "单模", "多模", "增益曲线", "调谐", "脉冲", "nw",
        "半高全宽", "fwhm",
    ], ["光子晶体能带与模式选择", "共振与激射", "激光模式与半导体巴条"]),
    Topic("光子晶体能带与模式选择", "模型", [
        "bandgap", "带隙", "能带", "band", "光子晶体", "笼目", "kagome", "mid-gap",
        "singlet", "模式选择", "优化后 fsr", "能带图", "红线",
    ], ["增益带宽与单模激光", "拓扑与狄拉克涡旋腔", "光学微腔与 Purcell 效应"]),
    Topic("激光模式与半导体巴条", "概念", [
        "巴条", "laser diode bar", "横模", "纵模", "基模", "高阶模", "光斑形状",
        "一维阵列", "高功率",
    ], ["增益带宽与单模激光", "共振与激射", "光子晶体能带与模式选择"]),
    Topic("共振与激射", "模型", [
        "共振", "resonance", "激射", "lasing", "谐振腔", "粒子数反转", "增益介质",
        "阈值", "dfb", "vcsel", "n2", "i(z)", "自激振荡", "相位匹配",
    ], ["增益带宽与单模激光", "电磁腔本征模式与边界条件", "光学微腔与 Purcell 效应"]),
    Topic("电磁腔本征模式与边界条件", "模型", [
        "本征值", "本征频率", "简并", "正交性", "完备性", "pec", "pmc", "impedence",
        "impedance", "边界条件", "电磁腔", "特征值", "谐振器频率", "无损腔",
        "电场与模式", "离散特征频率", "简谐振子",
    ], ["共振与激射", "光学微腔与 Purcell 效应", "拓扑与狄拉克涡旋腔"]),
    Topic("光学微腔与 Purcell 效应", "模型", [
        "purcell", "珀塞尔", "光存储时间", "photo storage", "模式体积", "q因子",
        "波长尺度", "强局域化", "光与物质相互作用", "腔相关核心概念",
        "腔谐振频率", "发光加速", "wavelength-scale",
    ], ["共振与激射", "电磁腔本征模式与边界条件", "拓扑与狄拉克涡旋腔"]),
    Topic("拓扑学基础", "模型", [
        "拓扑学", "topology", "莫比乌斯", "拓扑等价", "拓扑性质", "拓扑变换",
        "球面", "环面", "连续变换", "平面几何", "欧拉", "不变量",
    ], ["拓扑与狄拉克涡旋腔", "电磁腔本征模式与边界条件", "光子晶体能带与模式选择"]),
    Topic("拓扑与狄拉克涡旋腔", "模型", [
        "dirac", "狄拉克", "拓扑禁带", "平带", "topological mechanics", "topological",
        "拓扑把频率锁定", "狄拉克涡旋腔",
    ], ["拓扑学基础", "光子晶体能带与模式选择", "光学微腔与 Purcell 效应"]),
    Topic("激光雷达与毫米波雷达", "概念", [
        "激光雷达", "毫米波雷达", "低空探测", "自动驾驶", "大气环境监测",
        "三维建筑模型", "测速测距", "探测精度", "全天候", "地物回波",
        "雷达", "遥感探测",
    ], ["光学微腔与 Purcell 效应", "Python 数据平滑绘图", "科研汇报与 PPT 准备"]),
    Topic("Python 数据平滑绘图", "方法", [
        "matplotlib", "scipy", "make_interp_spline", "linspace", "numpy", "平滑曲线",
        "样条插值", "数据", "x值序列", "代码示例", "使用模型计算",
    ], ["激光雷达与毫米波雷达", "科研汇报与 PPT 准备", "实验与数据分析写作"]),
    Topic("文献综述写作流程", "方法", [
        "文献综述", "撰写论文", "研究领域", "收集文献", "评估文献", "组织文献",
        "撰写综述", "参考文献", "未来研究方向", "提供背景", "总结和分析",
    ], ["实验与数据分析写作", "科研汇报与 PPT 准备", "学习方法与四赢法"]),
    Topic("实验与数据分析写作", "方法", [
        "实验结果", "实验所采用", "局限性", "未来的发展方向", "分析实验",
        "实验的局限", "方法和损耗", "制备", "测量结果",
    ], ["文献综述写作流程", "科研汇报与 PPT 准备", "薄膜铌酸锂调制器"]),
    Topic("学习方法与四赢法", "洞察", [
        "四赢", "学习", "习题册", "课本", "取势", "行业解决方案", "死记硬背",
        "看书速度", "考试", "章节", "请教牛人", "检索信息", "成年人",
    ], ["文献综述写作流程", "科研汇报与 PPT 准备", "博士面试准备"]),
    Topic("博士面试准备", "来源", [
        "phd", "tell us about yourself", "why do you want", "interested in this program",
        "good candidate", "proposal", "strengths and weaknesses", "career plans",
        "setback", "difficulties", "questions for us", "面试问题", "学术背景",
    ], ["科研汇报与 PPT 准备", "学习方法与四赢法", "文献综述写作流程"]),
    Topic("科研汇报与 PPT 准备", "洞察", [
        "ppt", "presentation", "讲稿", "师兄师姐", "汇报", "把每一篇都做成",
        "提问题", "文献中找答案", "总结ppt",
    ], ["文献综述写作流程", "实验与数据分析写作", "博士面试准备"]),
    Topic("书籍资料获取记录", "来源", [
        "pdf drive", "z library", "busybook", "授权码", "备用网址", "使用方法", "打开书籍",
        "kdocs", "sobereva", "完成！！！", "loop123",
    ], ["原始链接与临时记录", "学习方法与四赢法", "文献综述写作流程"]),
    Topic("原始链接与临时记录", "来源", [
        "来自 http", "来自 https", "http ", "https ", "21 45", "2024年", "mn", "mnpq",
        "=c", "式中c", "频率 ν", "——————————————————", "等所有要求",
    ], ["书籍资料获取记录", "文献综述写作流程", "科研汇报与 PPT 准备"]),
]

FALLBACK = Topic("未分类原始记录", "来源", [], ["原始链接与临时记录", "科研汇报与 PPT 准备", "学习方法与四赢法"])


@dataclass
class Note:
    path: Path
    title: str
    body: str
    category: str
    topic: Topic | None = None


def strip_frontmatter(text: str) -> str:
    if text.startswith("---"):
        parts = text.split("---", 2)
        if len(parts) == 3:
            return parts[2].strip()
    return text.strip()


def read_note(path: Path) -> Note:
    text = strip_frontmatter(path.read_text(encoding="utf-8"))
    lines = text.splitlines()
    title = path.stem
    body_lines = []
    for line in lines:
        stripped = line.strip()
        if stripped.startswith("# "):
            title = stripped[2:].strip()
            continue
        if stripped.startswith("关联概念："):
            continue
        body_lines.append(line.rstrip())
    body = clean_body("\n".join(body_lines), title)
    return Note(path=path, title=clean_title(title), body=body, category=path.parent.name)


def clean_title(title: str) -> str:
    title = re.sub(r"\s+", " ", title).strip()
    title = title.strip(" #")
    return title or "未命名片段"


def clean_body(body: str, title: str) -> str:
    body = re.sub(r"\n{3,}", "\n\n", body.strip())
    if not body:
        return title
    if normalize(body) == normalize(title):
        return title
    return body


def normalize(text: str) -> str:
    text = text.lower()
    text = re.sub(r"!\[\[attachments/[^\]]+\]\]", "", text)
    text = re.sub(r"\[\[[^\]]+\]\]", "", text)
    text = re.sub(r"\s+", "", text)
    text = re.sub(r"[，。；：、,.!?;:（）()【】\\[\\]\"'“”‘’<>《》-]", "", text)
    return text


def assign_topic(note: Note) -> Topic:
    haystack = f"{note.title}\n{note.body}".lower()
    for topic in TOPICS:
        for pattern in topic.patterns:
            if pattern.lower() in haystack:
                return topic
    return FALLBACK


def section_title(title: str, index: int) -> str:
    title = re.sub(r"^#+\s*", "", title).strip()
    title = re.sub(r"\s+", " ", title)
    title = title.strip("。；;：:")
    if len(title) > 52:
        title = title[:52].rstrip("，。；;：:、 ") + "..."
    return title or f"片段 {index}"


def section_body(note: Note) -> str:
    body = note.body.strip()
    if not body:
        return note.title.strip()
    return body


def sanitize_filename(name: str) -> str:
    clean = "".join(" " if ch in '\\/:*?\"<>|#^[]' else ch for ch in name)
    clean = re.sub(r"\s+", " ", clean).strip(" .")
    return clean[:80] or "未命名知识单元"


def wikilink(name: str) -> str:
    return f"[[{name}]]"


def build_topic_file(topic: Topic, notes: list[Note]) -> str:
    seen = set()
    sections = []
    for idx, note in enumerate(notes, 1):
        body = section_body(note)
        key = normalize(body)
        if key in seen:
            continue
        seen.add(key)
        heading = section_title(note.title, idx)
        sections.append(f"## {heading}\n\n{body}")

    related = [name for name in topic.related if name != topic.name]
    related = [name for name in related if name in ALL_TOPIC_NAMES]
    related_line = "相关知识：" + " ".join(wikilink(name) for name in related[:6])
    content = FRONTMATTER + f"# {topic.name}\n\n" + "\n\n".join(sections).strip() + "\n\n" + related_line + "\n"
    return re.sub(r"\n{3,}", "\n\n", content)


def write_report(merged_groups, deleted_count, manual, before_count, after_count, category_stats, old_to_new):
    lines = [
        "# Refactor Report",
        "",
        f"- 原始碎片笔记数量: {before_count}",
        f"- 合并后知识单元数量: {after_count}",
        f"- 合并分组数量: {len(merged_groups)}",
        f"- 删除碎片文件数量: {deleted_count}",
        "",
        "## 分类统计",
        "",
    ]
    for category in CATEGORIES:
        lines.append(f"- {category}: {category_stats.get(category, 0)}")
    lines.extend(["", "## 合并清单", ""])
    for topic_name, notes in sorted(merged_groups.items()):
        lines.append(f"- {topic_name}: {len(notes)} 篇碎片")
    lines.extend(["", "## 双链更新", ""])
    lines.append(f"- 已建立旧文件名到新知识单元的映射: {len(old_to_new)} 条")
    lines.append("- 合并后的笔记使用新知识单元之间的有效双链。")
    lines.extend(["", "## 仍需人工优化", ""])
    if manual:
        for item in manual:
            lines.append(f"- {item}")
    else:
        lines.append("- 无。")
    REPORT.write_text("\n".join(lines) + "\n", encoding="utf-8")


def line_count(path: Path) -> int:
    return len([line for line in path.read_text(encoding="utf-8").splitlines() if line.strip()])


ALL_TOPIC_NAMES = {topic.name for topic in TOPICS} | {FALLBACK.name}


def main():
    note_paths = sorted(p for category in CATEGORIES for p in (VAULT / category).glob("*.md"))
    notes = [read_note(path) for path in note_paths if path.name not in {"Migration_Report.md", "Refactor_Report.md"}]
    before_count = len(notes)

    groups = defaultdict(list)
    old_to_new = {}
    for note in notes:
        topic = assign_topic(note)
        note.topic = topic
        groups[topic.name].append(note)
        old_to_new[note.path.stem] = topic.name

    for path in note_paths:
        if path.name not in {"Migration_Report.md", "Refactor_Report.md"}:
            path.unlink()

    written = []
    category_stats = Counter()
    for topic in TOPICS + [FALLBACK]:
        topic_notes = groups.get(topic.name, [])
        if not topic_notes:
            continue
        target_dir = VAULT / topic.category
        target_dir.mkdir(parents=True, exist_ok=True)
        target = target_dir / f"{sanitize_filename(topic.name)}.md"
        target.write_text(build_topic_file(topic, topic_notes), encoding="utf-8")
        written.append(target)
        category_stats[topic.category] += 1

    manual = []
    for path in written:
        count = line_count(path)
        if count < 20:
            manual.append(f"{path.parent.name}/{path.name}: {count} 行，内容偏短，可考虑继续并入相邻主题。")
        elif count > 100:
            manual.append(f"{path.parent.name}/{path.name}: {count} 行，内容偏长，建议人工拆出二级主题。")

    deleted_count = before_count
    write_report(groups, deleted_count, manual, before_count, len(written), category_stats, old_to_new)
    print(f"before={before_count}")
    print(f"after={len(written)}")
    print(f"deleted={deleted_count}")
    print("categories=" + ", ".join(f"{category}:{category_stats.get(category, 0)}" for category in CATEGORIES))
    print(f"manual={len(manual)}")


if __name__ == "__main__":
    main()
