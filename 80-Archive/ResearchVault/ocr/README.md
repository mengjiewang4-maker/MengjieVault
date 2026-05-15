# OCR 配置说明

本知识库已配置本地 OCR：

- 引擎：Tesseract 5.5.2
- 中文语言包：`chi_sim`
- 英文语言包：`eng`
- 脚本：`scripts/ocr_pdf.py`

## 试跑目录页

```bash
python3 scripts/ocr_pdf.py "书籍/量子力学教程 (曾谨言) (Z-Library).pdf" --from-page 27 --to-page 31 --psm 6
```

输出：

- `ocr/量子力学教程 (曾谨言) (Z-Library)/combined.md`
- `ocr/量子力学教程 (曾谨言) (Z-Library)/pages/page_0027.md`

## 试跑正文页

```bash
python3 scripts/ocr_pdf.py "书籍/量子力学教程 (曾谨言) (Z-Library).pdf" --from-page 14 --to-page 14 --psm 3 --out-dir ocr/test_body_page
```

正文页建议使用 `--psm 3`。目录页和表格页可尝试 `--psm 6`。

## OCR 整本书

```bash
python3 scripts/ocr_pdf.py "书籍/量子力学教程 (曾谨言) (Z-Library).pdf" --from-page 32 --to-page 298 --psm 3
```

说明：

- 这本 PDF 是扫描版，OCR 无法做到完全无误，公式、脚注编号、目录点线最容易出错。
- 当前脚本按 PDF 页码处理；本书正文教材页码与 PDF 页码约满足：`PDF 页码 = 教材页码 + 31`。
- 如果只学习某一章，建议按目录页码换算后分章 OCR，便于人工校对。

