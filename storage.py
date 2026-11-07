"""本地 JSON 持久化；原子替换避免写入中断损坏原文件。"""
import json, os, tempfile
from pathlib import Path
PATH = Path(__file__).parent / 'data' / 'records.json'
def read():
    return json.loads(PATH.read_text('utf-8')) if PATH.exists() else []
def write(records):
    PATH.parent.mkdir(exist_ok=True)
    fd, name = tempfile.mkstemp(dir=PATH.parent)
    try:
        with os.fdopen(fd, 'w', encoding='utf-8') as f:
            json.dump(records, f, ensure_ascii=False, indent=2)
        os.replace(name, PATH)
    finally:
        if os.path.exists(name): os.unlink(name)
