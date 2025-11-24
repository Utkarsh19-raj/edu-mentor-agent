# tools/memory.py
import json
import os
from typing import Dict, Any

MEMORY_FILE = "user_memory.json"


def load_memory() -> Dict[str, Any]:
    """
    Load the full memory dictionary from disk.
    """
    if not os.path.exists(MEMORY_FILE):
        return {}
    try:
        with open(MEMORY_FILE, "r") as f:
            return json.load(f)
    except json.JSONDecodeError:
        # If the file is corrupted, reset it
        return {}


def save_memory(memory: Dict[str, Any]) -> None:
    """
    Save the full memory dictionary to disk.
    """
    with open(MEMORY_FILE, "w") as f:
        json.dump(memory, f, indent=2)


def get_user_profile(user_id: str) -> Dict[str, Any]:
    """
    Get a single user's profile. Creates a default one if not present.
    """
    memory = load_memory()
    if user_id not in memory:
        memory[user_id] = {
            "user_id": user_id,
            "goals": [],
            "history": [],
            "weak_topics": [],
        }
        save_memory(memory)
    return memory[user_id]


def update_user_profile(user_id: str, new_data: Dict[str, Any]) -> None:
    """
    Update a specific user's profile and persist it.
    """
    memory = load_memory()
    memory[user_id] = new_data
    save_memory(memory)
