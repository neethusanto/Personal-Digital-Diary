"""
Storage module for the Personal Digital Diary application.
Demonstrates File Handling (reading, writing, deleting, directory management)
and Exception Handling.
"""

import json
import os
from pathlib import Path
from typing import List, Optional

from entry import DiaryEntry
from exceptions import StorageError, EntryNotFoundError


class FileStorage:
    """
    Handles persistence of DiaryEntry objects to local files.
    
    Each entry is stored as a formatted JSON document inside the storage directory.
    Provides methods to save, load, delete, and list entries.
    """

    def __init__(self, storage_dir: str = "data/entries"):
        self.storage_path = Path(storage_dir)
        self._ensure_storage_directory()

    def _ensure_storage_directory(self) -> None:
        """
        Ensures the storage directory exists.
        Demonstrates Exception Handling with File and OS operations.
        """
        try:
            self.storage_path.mkdir(parents=True, exist_ok=True)
        except OSError as e:
            raise StorageError(f"Failed to create storage directory '{self.storage_path}': {e}") from e

    def _get_entry_filepath(self, entry_id: str) -> Path:
        """Helper to get file path for a specific entry ID."""
        return self.storage_path / f"entry_{entry_id}.json"

    def save(self, entry: DiaryEntry) -> Path:
        """
        Saves or updates a DiaryEntry to a local JSON file.
        Demonstrates file writing with context manager and exception handling.
        """
        filepath = self._get_entry_filepath(entry.entry_id)
        try:
            with open(filepath, "w", encoding="utf-8") as f:
                json.dump(entry.to_dict(), f, indent=4, ensure_ascii=False)
            return filepath
        except (OSError, PermissionError) as e:
            raise StorageError(f"Error saving entry '{entry.entry_id}' to '{filepath}': {e}") from e

    def load(self, entry_id: str) -> DiaryEntry:
        """
        Loads a single DiaryEntry from its local file by entry ID.
        Demonstrates file reading with context manager and error handling.
        """
        filepath = self._get_entry_filepath(entry_id)
        if not filepath.exists():
            raise EntryNotFoundError(f"Entry with ID '{entry_id}' does not exist.")

        try:
            with open(filepath, "r", encoding="utf-8") as f:
                data = json.load(f)
            return DiaryEntry.from_dict(data)
        except json.JSONDecodeError as e:
            raise StorageError(f"Corrupted entry file '{filepath}': {e}") from e
        except (OSError, PermissionError) as e:
            raise StorageError(f"Error reading entry file '{filepath}': {e}") from e

    def load_all(self) -> List[DiaryEntry]:
        """
        Reads and loads all entry files from the storage directory.
        """
        entries: List[DiaryEntry] = []
        try:
            for filepath in self.storage_path.glob("entry_*.json"):
                try:
                    with open(filepath, "r", encoding="utf-8") as f:
                        data = json.load(f)
                    entries.append(DiaryEntry.from_dict(data))
                except (json.JSONDecodeError, KeyError) as e:
                    # Log warning or skip corrupted files gracefully
                    print(f"[Warning] Skipping corrupted file {filepath.name}: {e}")
            
            # Sort chronologically by entry date and then creation time
            entries.sort(key=lambda e: (e.entry_date, e.created_at), reverse=True)
            return entries
        except (OSError, PermissionError) as e:
            raise StorageError(f"Error reading directory '{self.storage_path}': {e}") from e

    def delete(self, entry_id: str) -> bool:
        """
        Deletes the file corresponding to the given entry ID.
        Demonstrates file deletion and exception handling.
        """
        filepath = self._get_entry_filepath(entry_id)
        if not filepath.exists():
            raise EntryNotFoundError(f"Entry with ID '{entry_id}' does not exist.")

        try:
            filepath.unlink()
            return True
        except (OSError, PermissionError) as e:
            raise StorageError(f"Error deleting entry file '{filepath}': {e}") from e

    def export_as_text(self, entry: DiaryEntry, export_dir: str = "data/exports") -> Path:
        """
        Exports a diary entry to a clean plain-text/markdown format file.
        Demonstrates another dimension of file handling.
        """
        export_path = Path(export_dir)
        try:
            export_path.mkdir(parents=True, exist_ok=True)
            filename = f"{entry.entry_date.strftime('%Y-%m-%d')}_{entry.entry_id}.txt"
            filepath = export_path / filename

            with open(filepath, "w", encoding="utf-8") as f:
                f.write(entry.display())
            return filepath
        except (OSError, PermissionError) as e:
            raise StorageError(f"Failed to export entry '{entry.entry_id}' to text file: {e}") from e

