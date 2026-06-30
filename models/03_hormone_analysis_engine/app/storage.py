from pathlib import Path
import shutil

def save_file(src,dst):
    dst=Path(dst)
    dst.parent.mkdir(parents=True,exist_ok=True)
    shutil.copy2(src,dst)
    return dst

def delete_file(path):
    p=Path(path)
    if p.exists():
        p.unlink()

def exists(path):
    return Path(path).exists()
