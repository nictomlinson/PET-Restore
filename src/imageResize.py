from pathlib import Path
# For future me: pip install pillow
from PIL import Image
import shutil
import os

SOURCE = Path("../PET-Restore_OriginalPhotos/images")
DEST = Path("./images")

MAX_SIZE = 2000      # longest edge
JPEG_QUALITY = 85

def process_image(src_file: Path):
    rel_path = src_file.relative_to(SOURCE)
    dst_file = DEST / rel_path

    dst_file.parent.mkdir(parents=True, exist_ok=True)

    # Skip if destination exists and is newer than source
    if dst_file.exists():
        src_mtime = src_file.stat().st_mtime
        dst_mtime = dst_file.stat().st_mtime

        if dst_mtime >= src_mtime:
            print(f"SKIP {rel_path}")
            return

    print(f"BUILD {rel_path}")

    with Image.open(src_file) as img:
        img = img.convert("RGB")

        width, height = img.size

        if max(width, height) > MAX_SIZE:
            img.thumbnail((MAX_SIZE, MAX_SIZE), Image.Resampling.LANCZOS)

        img.save(
            dst_file,
            "JPEG",
            quality=JPEG_QUALITY,
            optimize=True,
            progressive=True
        )

    # Preserve original timestamp
    src_stat = src_file.stat()
    os.utime(dst_file, (src_stat.st_atime, src_stat.st_mtime))


extensions = {".jpg", ".jpeg"}

for src_file in SOURCE.rglob("*"):
    if src_file.suffix.lower() in extensions:
        process_image(src_file)

print("Done")
