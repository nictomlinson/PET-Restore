from pathlib import Path
import re

IMAGES_DIR = Path("./images")
GALLERY_DIR = Path("./gallery")
INDEX_FILE = Path("./gallery_index.md")

IMAGE_EXTS = {".jpg", ".jpeg", ".png", ".gif", ".webp"}

GALLERY_DIR.mkdir(exist_ok=True)

index_lines = [
    "# Image Galleries",
    ""
]

gallery_folders = sorted(
    [d for d in IMAGES_DIR.iterdir() if d.is_dir()],
    reverse=True
)

for folder in gallery_folders:

    gallery_name = folder.name
    gallery_md = GALLERY_DIR / f"{gallery_name}.md"

    m = re.match(r"(\d{8})_(.+)", gallery_name)

    if m:
        date = f"{m.group(1)[:4]}/{m.group(1)[4:6]}/{m.group(1)[6:]}"
        display_name = m.group(2).replace("_", " ")
    else:
        date = None
        display_name = gallery_name.replace("_", " ")

    image_files = sorted(
        [f for f in folder.iterdir()
         if f.suffix.lower() in IMAGE_EXTS]
    )

    lines = [
        f"# {date} {display_name}",
        ""
    ]

    for image in image_files:

        image_path = f"/images/{gallery_name}/{image.name}"

        lines.append(f'![{image.stem}]({image_path})')
#        if date:
#            lines.append(f"*{date}*")
        lines.append("")
        lines.append("<br>")
        lines.append("")

    gallery_md.write_text(
        "\n".join(lines),
        encoding="utf-8"
    )

    index_lines.append(
        f"- [{date + ' - ' if date else ''}{display_name}](/gallery/{gallery_name}.md)"
    )

INDEX_FILE.write_text(
    "\n".join(index_lines),
    encoding="utf-8"
)

print("Gallery pages updated.")