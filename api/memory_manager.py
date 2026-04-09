import json
import logging
from pathlib import Path
from datetime import datetime, timezone
from typing import List, Dict, Any, Optional

class MemoryManager:
    """Manages Nanobot-inspired layered memory files."""

    def __init__(self, memory_dir: Path = None):
        if memory_dir is None:
            # Default to the memory directory within the api package
            self.memory_dir = Path(__file__).parent / "memory"
        else:
            self.memory_dir = memory_dir
        
        self.memory_dir.mkdir(parents=True, exist_ok=True)
        self.history_file = self.memory_dir / "HISTORY.jsonl"
        self.soul_file = self.memory_dir / "SOUL.md"
        self.user_file = self.memory_dir / "USER.md"

    def get_soul(self) -> str:
        """Returns the agent's identity and core directives."""
        if not self.soul_file.exists():
            return "You are Guidely, a helpful AI tutor."
        return self.soul_file.read_text(encoding="utf-8")

    def get_user_context(self) -> str:
        """Returns the persistent user preferences and history summaries."""
        if not self.user_file.exists():
            return "No specific user context available."
        return self.user_file.read_text(encoding="utf-8")

    async def append_history(self, user_id: str, query: str, answer: str, metadata: Dict[str, Any] = None):
        """Appends a new interaction to the history.jsonl file."""
        entry = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "user_id": user_id,
            "query": query,
            "answer": answer,
            "metadata": metadata or {}
        }
        try:
            with open(self.history_file, "a", encoding="utf-8") as f:
                f.write(json.dumps(entry) + "\n")
        except Exception as e:
            logging.error(f"Failed to append memory history: {e}")

    def get_recent_history(self, limit: int = 5) -> List[Dict[str, Any]]:
        """Retrieves the most recent interactions from history."""
        if not self.history_file.exists():
            return []
        
        try:
            with open(self.history_file, "r", encoding="utf-8") as f:
                lines = f.readlines()
            
            recent_lines = lines[-limit:]
            return [json.loads(line) for line in recent_lines]
        except Exception as e:
            logging.error(f"Failed to read memory history: {e}")
            return []

# Singleton instance
memory_manager = MemoryManager()
