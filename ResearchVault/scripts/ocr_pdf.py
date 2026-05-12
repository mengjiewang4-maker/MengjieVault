#!/usr/bin/env python3
"""
OCR helper for scanned PDFs in this vault.

The Zeng Jinyan PDF stores each scanned page as one embedded image. This script
extracts those images with pypdf, optionally preprocesses them with Pillow, and
passes them to the local tesseract CLI.
"""

from __future__ import annotations

import argparse
import re
import shutil
import subprocess
import tempfile
from pathlib import Path

from PIL import Image, ImageOps
from pypdf import PdfReader


ROOT = Path(__file__).resolve().parents[1]


def slugify(path: Path) -> str:
    stem = path.stem
    stem = re.sub(r"[\\/:\*\?\"<>\|]", "_", stem)
    stem = re.sub(r"\s+", " ", stem).strip()
    return stem[:80] or "ocr_output"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="OCR a scanned PDF with tesseract.")
    parser.add_argument("pdf", type=Path, help="PDF path")
    parser.add_argument("--from-page", type=int, default=1, help="first PDF page, 1-based")
    parser.add_argument("--to-page", type=int, default=None, help="last PDF page, inclusive")
    parser.add_argument("--lang", default="chi_sim+eng", help="tesseract language list")
    parser.add_argument("--psm", default="3", help="tesseract page segmentation mode")
    parser.add_argument("--out-dir", type=Path, default=None, help="output directory")
    parser.add_argument("--keep-images", action="store_true", help="save preprocessed page images")
    parser.add_argument("--scale", type=float, default=1.5, help="image upscale factor before OCR")
    return parser.parse_args()


def ensure_tesseract() -> None:
    if shutil.which("tesseract") is None:
        raise SystemExit("tesseract not found. Install it with: brew install tesseract tesseract-lang")


def preprocess_image(raw: bytes, destination: Path, scale: float) -> None:
    with tempfile.NamedTemporaryFile(suffix=".img") as tmp:
        tmp.write(raw)
        tmp.flush()
        image = Image.open(tmp.name).convert("L")
        image = ImageOps.autocontrast(image)
        if scale != 1.0:
            width = max(1, int(image.width * scale))
            height = max(1, int(image.height * scale))
            image = image.resize((width, height), Image.Resampling.LANCZOS)
        image.save(destination)


def ocr_image(image_path: Path, lang: str, psm: str) -> str:
    command = [
        "tesseract",
        str(image_path),
        "stdout",
        "-l",
        lang,
        "--psm",
        psm,
        "--dpi",
        "300",
    ]
    result = subprocess.run(command, check=False, text=True, capture_output=True)
    if result.returncode != 0:
        raise RuntimeError(result.stderr.strip() or f"tesseract failed for {image_path}")
    return result.stdout.strip()


def main() -> None:
    args = parse_args()
    ensure_tesseract()

    pdf_path = args.pdf if args.pdf.is_absolute() else ROOT / args.pdf
    if not pdf_path.exists():
        raise SystemExit(f"PDF not found: {pdf_path}")

    reader = PdfReader(str(pdf_path))
    total_pages = len(reader.pages)
    start = max(1, args.from_page)
    end = args.to_page or total_pages
    end = min(end, total_pages)
    if start > end:
        raise SystemExit(f"invalid page range: {start}-{end}")

    out_dir = args.out_dir or ROOT / "ocr" / slugify(pdf_path)
    pages_dir = out_dir / "pages"
    images_dir = out_dir / "images"
    pages_dir.mkdir(parents=True, exist_ok=True)
    if args.keep_images:
        images_dir.mkdir(parents=True, exist_ok=True)

    combined_parts: list[str] = [
        f"# OCR：{pdf_path.name}",
        "",
        f"- PDF：`{pdf_path}`",
        f"- 页码范围：{start}-{end}",
        f"- OCR 语言：`{args.lang}`",
        "",
    ]

    with tempfile.TemporaryDirectory(prefix="pdf-ocr-") as tmp_dir_raw:
        tmp_dir = Path(tmp_dir_raw)
        for page_number in range(start, end + 1):
            page = reader.pages[page_number - 1]
            if not page.images:
                text = ""
            else:
                image = page.images[0]
                image_path = tmp_dir / f"page_{page_number:04d}.png"
                preprocess_image(image.data, image_path, args.scale)
                text = ocr_image(image_path, args.lang, args.psm)
                if args.keep_images:
                    shutil.copy2(image_path, images_dir / image_path.name)

            page_file = pages_dir / f"page_{page_number:04d}.md"
            page_file.write_text(text + "\n", encoding="utf-8")

            combined_parts.extend(
                [
                    f"## PDF page {page_number}",
                    "",
                    text,
                    "",
                ]
            )
            print(f"OCR page {page_number}/{end}: {len(text)} chars")

    combined_path = out_dir / "combined.md"
    combined_path.write_text("\n".join(combined_parts), encoding="utf-8")
    print(f"written: {combined_path}")


if __name__ == "__main__":
    main()

