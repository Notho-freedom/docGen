import json
import os
from collections import deque
from typing import List, Dict

class Memory:
    def __init__(self, path: str = "memory.json", max_len: int = 20):
        self.path = path
        self.max_len = max_len
        self.messages = deque(maxlen=max_len)
        self._load()

    def add(self, role: str, content: str):
        self.messages.append({"role": role, "content": content})
        self._save()

    def get(self) -> List[Dict[str, str]]:
        return list(self.messages)

    def clear(self):
        self.messages.clear()
        self._save()

    def _load(self):
        if os.path.exists(self.path):
            try:
                with open(self.path, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    self.messages = deque(data, maxlen=self.max_len)
            except Exception as e:
                print(f"[Mémoire] Erreur chargement JSON : {e}")

    def _save(self):
        try:
            with open(self.path, "w", encoding="utf-8") as f:
                json.dump(list(self.messages), f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"[Mémoire] Erreur sauvegarde JSON : {e}")
