from pathlib import Path
class StorageService:
    def save_bytes(self,path,data):
        p=Path(path);p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(data);return p
storage_service=StorageService()
