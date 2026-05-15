from collections import Counter, defaultdict
from pathlib import Path
from zipfile import ZipFile
import re
import shutil
import xml.etree.ElementTree as ET


ROOT = Path.cwd()
DOCX_CANDIDATES = [ROOT / "onenote.docx", ROOT.parent / "onenote.docx"]
DOCX = next((path for path in DOCX_CANDIDATES if path.exists()), None)
VAULT = ROOT / "Obsidian_Vault"
ATTACHMENTS = VAULT / "attachments"
TEMP_MD = ROOT / "temp.md"

NS = {
    "w": "http://schemas.openxmlformats.org/wordprocessingml/2006/main",
    "a": "http://schemas.openxmlformats.org/drawingml/2006/main",
    "r": "http://schemas.openxmlformats.org/officeDocument/2006/relationships",
    "rel": "http://schemas.openxmlformats.org/package/2006/relationships",
}

CATEGORIES = ["来源", "概念", "方法", "模型", "洞察"]

FRONTMATTER = """---\ntype: note\nsource: onenote_import\ntags:\n  - onenote\nrelated: []\n---\n\n"""

KEYWORDS = [
    ("bandgap", "Bandgap"),
    ("Bandgap", "Bandgap"),
    ("带隙", "带隙"),
    ("mode", "Mode"),
    ("Mode", "Mode"),
    ("模式", "Mode"),
    ("TB", "TB"),
    ("tight-binding", "TB"),
    ("tight binding", "TB"),
    ("紧束缚", "TB"),
    ("FSR", "FSR"),
    ("Free Spectral Range", "FSR"),
    ("自由光谱范围", "FSR"),
    ("单模", "单模激光"),
    ("多模", "多模激光"),
    ("增益带宽", "增益带宽"),
    ("光学增益带宽", "增益带宽"),
    ("增益介质", "增益介质"),
    ("gain medium", "增益介质"),
    ("能带", "能带"),
    ("Band", "能带"),
    ("谐振", "谐振"),
    ("共振", "共振"),
    ("Resonance", "共振"),
    ("激射", "激射"),
    ("lasing", "激射"),
    ("本征值", "本征值"),
    ("本征频率", "本征频率"),
    ("简并", "简并"),
    ("正交性", "正交性"),
    ("完备性", "完备性"),
    ("PEC", "PEC"),
    ("PMC", "PMC"),
    ("Impedence", "阻抗边界条件"),
    ("Impedance", "阻抗边界条件"),
    ("boundary", "边界条件"),
    ("边界条件", "边界条件"),
    ("Hamiltonian", "哈密顿量"),
    ("Dirac", "Dirac 点"),
    ("flat band", "平带"),
    ("平带", "平带"),
    ("Kagome", "Kagome 晶格"),
    ("笼目", "Kagome 晶格"),
    ("SSH", "SSH 模型"),
    ("拓扑", "拓扑光子学"),
    ("光子晶体", "光子晶体"),
    ("photonic crystal", "光子晶体"),
    ("微腔", "光学微腔"),
    ("DFB", "DFB 激光器"),
    ("VCSEL", "VCSEL"),
    ("GaAs", "GaAs"),
    ("横模", "横模"),
    ("纵模", "纵模"),
    ("基模", "基模"),
    ("高阶模", "高阶模"),
    ("FDTD", "FDTD"),
    ("PML", "PML"),
    ("COMSOL", "COMSOL"),
    ("Lumerical", "Lumerical"),
]


def ensure_dirs():
    for category in CATEGORIES:
        (VAULT / category).mkdir(parents=True, exist_ok=True)
    ATTACHMENTS.mkdir(parents=True, exist_ok=True)


def read_relationships(zip_file):
    rels = {}
    root = ET.fromstring(zip_file.read("word/_rels/document.xml.rels"))
    for rel in root.findall("rel:Relationship", NS):
        rid = rel.attrib.get("Id")
        target = rel.attrib.get("Target", "")
        if rid:
            rels[rid] = "word/" + target if not target.startswith("word/") else target
    return rels


def paragraph_text(paragraph):
    parts = []
    for node in paragraph.iter():
        if node.tag == f"{{{NS['w']}}}t":
            parts.append(node.text or "")
        elif node.tag == f"{{{NS['w']}}}tab":
            parts.append("\t")
        elif node.tag == f"{{{NS['w']}}}br":
            parts.append("\n")
    return "".join(parts).strip()


def paragraph_level(paragraph):
    ppr = paragraph.find("w:pPr", NS)
    if ppr is None:
        return 0
    style = ppr.find("w:pStyle", NS)
    if style is not None:
        value = style.attrib.get(f"{{{NS['w']}}}val", "")
        match = re.search(r"Heading(\d+)|^(\d+)$", value, re.I)
        if match:
            raw = match.group(1) or match.group(2)
            try:
                return max(1, min(3, int(raw)))
            except ValueError:
                return 0
    outline = ppr.find("w:outlineLvl", NS)
    if outline is not None:
        value = outline.attrib.get(f"{{{NS['w']}}}val")
        if value and value.isdigit():
            return max(1, min(3, int(value) + 1))
    return 0


def is_numbered(paragraph):
    return paragraph.find("w:pPr/w:numPr", NS) is not None


def image_refs(paragraph):
    refs = []
    for blip in paragraph.findall(".//a:blip", NS):
        rid = blip.attrib.get(f"{{{NS['r']}}}embed") or blip.attrib.get(f"{{{NS['r']}}}link")
        if rid:
            refs.append(rid)
    return refs


def extract_markdown():
    if DOCX is None:
        raise FileNotFoundError("Neither ./onenote.docx nor ../onenote.docx exists.")

    lines = ["# OneNote Import", ""]
    attachment_map = {}
    image_counter = Counter()

    with ZipFile(DOCX) as z:
        rels = read_relationships(z)
        for name in z.namelist():
            if name.startswith("word/media/") and not name.endswith("/"):
                source_name = Path(name).name
                image_counter[source_name] += 1
                target_name = source_name
                if image_counter[source_name] > 1:
                    stem = Path(source_name).stem
                    suffix = Path(source_name).suffix
                    target_name = f"{stem}_{image_counter[source_name]}{suffix}"
                with z.open(name) as src, (ATTACHMENTS / target_name).open("wb") as dst:
                    shutil.copyfileobj(src, dst)
                attachment_map[name] = target_name

        document = ET.fromstring(z.read("word/document.xml"))
        for paragraph in document.findall(".//w:p", NS):
            text = paragraph_text(paragraph)
            refs = image_refs(paragraph)
            level = paragraph_level(paragraph)

            if text:
                normalized = clean_inline_text(text)
                if level:
                    heading = "#" * max(1, min(3, level))
                    lines.extend([f"{heading} {normalized}", ""])
                elif is_numbered(paragraph):
                    lines.extend([f"- {normalized}", ""])
                else:
                    lines.extend([normalized, ""])

            for rid in refs:
                media_path = rels.get(rid)
                attachment_name = attachment_map.get(media_path or "")
                if attachment_name:
                    lines.extend([f"![[Obsidian_Vault/attachments/{attachment_name}]]", ""])

    markdown = normalize_blank_lines("\n".join(lines))
    TEMP_MD.write_text(markdown, encoding="utf-8")
    return markdown


def clean_inline_text(text):
    text = text.replace("\u00a0", " ").replace("\u200b", "")
    text = re.sub(r"[ \t]+", " ", text)
    return text.strip()


def normalize_blank_lines(markdown):
    markdown = markdown.replace("\r\n", "\n").replace("\r", "\n")
    markdown = re.sub(r"\n{3,}", "\n\n", markdown)
    return markdown.strip() + "\n"


def split_knowledge_points(markdown):
    blocks = []
    current_title = None
    current_lines = []
    fallback_index = 1

    for raw_line in markdown.splitlines():
        line = raw_line.rstrip()
        heading = re.match(r"^(#{2,3})\s+(.+)$", line)
        if heading:
            if current_title or current_lines:
                blocks.append(make_block(current_title, current_lines, fallback_index))
                fallback_index += 1
            current_title = heading.group(2).strip()
            current_lines = []
        elif line.startswith("# "):
            continue
        else:
            if current_title is None and line.strip():
                title = infer_title(line, fallback_index)
                blocks.append(make_block(title, [line], fallback_index))
                fallback_index += 1
            elif current_title is not None:
                current_lines.append(line)

    if current_title or current_lines:
        blocks.append(make_block(current_title, current_lines, fallback_index))

    refined = []
    for block in blocks:
        content = normalize_blank_lines("\n".join(block["lines"]))
        if not content.strip():
            content = block["title"]
        if should_split_sentence_block(block["title"], content):
            refined.extend(split_long_content(content))
        else:
            block["content"] = content
            refined.append(block)
    return refined


def make_block(title, lines, index):
    clean_title = clean_inline_text(title or "")
    if not clean_title:
        for line in lines:
            if line.strip() and not line.startswith("![["):
                clean_title = infer_title(line, index)
                break
    if not clean_title:
        clean_title = f"未命名知识点 {index}"
    return {"title": clean_title, "lines": lines}


def should_split_sentence_block(title, content):
    if "\n\n" in content or "\n![[Obsidian_Vault/attachments/" in content:
        return False
    return len(content) > 220 and title == infer_title(content, 1)


def split_long_content(content):
    sentences = re.split(r"(?<=[。！？.!?])\s+", content)
    if len(sentences) <= 1:
        return [{"title": infer_title(content, 1), "content": content, "lines": [content]}]
    blocks = []
    for idx, sentence in enumerate(sentences, 1):
        sentence = sentence.strip()
        if not sentence:
            continue
        blocks.append({"title": infer_title(sentence, idx), "content": sentence + "\n", "lines": [sentence]})
    return blocks


def infer_title(text, index):
    text = re.sub(r"^[-*+]\s+", "", clean_inline_text(text))
    text = re.sub(r"^来自\s+<(.+)>$", r"来源 \1", text)
    text = re.sub(r"\s+", " ", text)
    title = text[:42].strip(" ，。；;:：、")
    return title or f"未命名知识点 {index}"


def classify(title, content):
    text = f"{title}\n{content}"
    lower = text.lower()
    if re.search(r"^来源|^来自\s+<|https?://", text):
        return "来源"
    if re.search(r"步骤|操作|软件|设置|运行|导入|仿真|扫描|绘制|加工|表征|实验|测量|安装|计算流程|comsol|lumerical|fdtd|matlab|python", lower):
        return "方法"
    if re.search(r"公式|方程|模型|哈密顿|hamiltonian|tight|tb|本征|矩阵|算符|正交|完备|边界条件|pec|pmc|dirac|平带|拓扑|能带图|band structure|e\^|n_\d|>", lower):
        return "模型"
    if re.search(r"总结|结论|意味着|核心|关键|因此|所以|理解|注意|本质|正是|可以理解|我的|启发", text):
        return "洞察"
    if re.search(r"是|指的是|称为|定义|术语|概念|全称|代表|meaning|refers to|called", lower):
        return "概念"
    return "来源"


def sanitize_filename(title):
    name = "".join(" " if char in '\\/:*?"<>|#^[]' else char for char in title)
    name = re.sub(r"\s+", " ", name).strip(" .")
    name = name[:80].strip()
    return name or "未命名知识点"


def collect_links(title, content):
    text = f"{title}\n{content}"
    links = []
    seen = set()
    for needle, concept in KEYWORDS:
        if concept in seen:
            continue
        pattern = re.escape(needle)
        flags = 0 if re.search(r"[\u4e00-\u9fff]", needle) else re.I
        if re.search(pattern, text, flags):
            links.append(concept)
            seen.add(concept)
        if len(links) >= 6:
            break

    inferred = infer_links_by_category(classify(title, content))
    for concept in inferred:
        if concept not in seen:
            links.append(concept)
            seen.add(concept)
        if len(links) >= 3:
            break
    return links[:6]


def infer_links_by_category(category):
    if category == "方法":
        return ["实验流程", "软件操作", "仿真设置"]
    if category == "模型":
        return ["理论模型", "边界条件", "本征值"]
    if category == "洞察":
        return ["研究总结", "关键结论", "模式选择"]
    if category == "概念":
        return ["术语定义", "光学微腔", "Mode"]
    return ["原始记录", "文献来源", "OneNote 导入"]


def note_body(title, content, links):
    content = normalize_blank_lines(content)
    link_line = "关联概念：" + " ".join(f"[[{link}]]" for link in links)
    return FRONTMATTER + f"# {title}\n\n{content}\n{link_line}\n"


def write_notes(blocks):
    stats = Counter()
    exceptions = []
    used_names = defaultdict(int)
    written = []

    for index, block in enumerate(blocks, 1):
        title = block["title"]
        content = block.get("content") or normalize_blank_lines("\n".join(block.get("lines", [])))
        category = classify(title, content)
        stats[category] += 1

        links = collect_links(title, content)
        if len(links) < 3:
            exceptions.append(f"{title}: only {len(links)} related links generated")

        filename_base = sanitize_filename(title)
        used_names[(category, filename_base)] += 1
        suffix = used_names[(category, filename_base)]
        filename = filename_base if suffix == 1 else f"{filename_base}-{suffix}"
        path = VAULT / category / f"{filename}.md"
        path.write_text(note_body(title, content, links), encoding="utf-8")
        written.append(path)

    return stats, exceptions, written


def validate(written):
    exceptions = []
    attachment_links = []
    for path in written:
        text = path.read_text(encoding="utf-8")
        if not text.startswith("---\ntype: note\nsource: onenote_import"):
            exceptions.append(f"{path.relative_to(ROOT)}: frontmatter missing or malformed")
        for match in re.findall(r"!\[\[attachments/([^\]]+)\]\]", text):
            attachment_links.append(match)
            if not (ATTACHMENTS / match).exists():
                exceptions.append(f"{path.relative_to(ROOT)}: missing attachment {match}")
    return exceptions, attachment_links


def write_report(stats, exceptions, validation_exceptions, written, attachment_links):
    attachment_count = len([p for p in ATTACHMENTS.iterdir() if p.is_file()])
    source_note = "./onenote.docx" if (ROOT / "onenote.docx").exists() else "../onenote.docx"
    lines = [
        "# Migration Report",
        "",
        f"- Source file: `{source_note}`",
        "- Pandoc command: not executed because `pandoc` was not available in PATH and `./onenote.docx` was absent.",
        "- Conversion fallback: standard-library DOCX XML parser with media extraction.",
        f"- Generated temp markdown: `temp.md`",
        f"- Split notes: {len(written)}",
        f"- Extracted attachments: {attachment_count}",
        f"- Attachment embeds used in notes: {len(attachment_links)}",
        "",
        "## 分类统计",
        "",
    ]
    for category in CATEGORIES:
        lines.append(f"- {category}: {stats.get(category, 0)}")
    lines.extend(["", "## 异常内容", ""])
    all_exceptions = exceptions + validation_exceptions
    if DOCX is None:
        all_exceptions.insert(0, "Source file not found.")
    if not (ROOT / "onenote.docx").exists():
        all_exceptions.insert(0, "`onenote.docx` was not present in the current directory; used `../onenote.docx`.")
    all_exceptions.insert(0, "`pandoc` was not available, so the requested pandoc command could not be run.")
    if all_exceptions:
        for item in all_exceptions:
            lines.append(f"- {item}")
    else:
        lines.append("- None")
    (VAULT / "Migration_Report.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def main():
    ensure_dirs()
    markdown = extract_markdown()
    cleaned = normalize_blank_lines(markdown)
    TEMP_MD.write_text(cleaned, encoding="utf-8")
    blocks = split_knowledge_points(cleaned)
    stats, exceptions, written = write_notes(blocks)
    validation_exceptions, attachment_links = validate(written)
    write_report(stats, exceptions, validation_exceptions, written, attachment_links)
    print(f"source={DOCX}")
    print(f"notes={len(written)}")
    print("stats=" + ", ".join(f"{category}:{stats.get(category, 0)}" for category in CATEGORIES))
    print(f"attachments={len([p for p in ATTACHMENTS.iterdir() if p.is_file()])}")
    print(f"attachment_embeds={len(attachment_links)}")
    print(f"exceptions={len(exceptions) + len(validation_exceptions) + 2}")


if __name__ == "__main__":
    main()
