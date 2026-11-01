"""
PersonalDiary class managing all diary operations.
Demonstrates OOP orchestration, DateTime processing, File Handling, and Exception Handling.
"""

from datetime import datetime, date
from typing import List, Optional, Union

from entry import DiaryEntry
from exceptions import InvalidDateFormatError, EntryNotFoundError
from storage import FileStorage


class PersonalDiary:
    """
    Main controller class for the Personal Digital Diary application.
    """

    def __init__(self, storage: Optional[FileStorage] = None):
        # OOP Composition: Diary utilizes a storage engine
        self.storage = storage or FileStorage()

    @staticmethod
    def parse_date(date_str: str) -> date:
        """
        Parses and validates a date string in YYYY-MM-DD format.
        Demonstrates DateTime handling and Exception Handling.
        """
        try:
            return datetime.strptime(date_str.strip(), "%Y-%m-%d").date()
        except ValueError as e:
            raise InvalidDateFormatError(
                f"Invalid date format '{date_str}'. Please use YYYY-MM-DD (e.g., 2026-11-01)."
            ) from e

    def create_entry(
        self,
        title: str,
        content: str,
        entry_date_str: Optional[str] = None
    ) -> DiaryEntry:
        """
        Creates a new diary entry and persists it to local storage.
        """
        if not title or not title.strip():
            raise ValueError("Entry title cannot be empty.")
        if not content or not content.strip():
            raise ValueError("Entry content cannot be empty.")

        entry_date: Optional[date] = None
        if entry_date_str:
            entry_date = self.parse_date(entry_date_str)
        else:
            entry_date = date.today()

        entry = DiaryEntry(title=title, content=content, entry_date=entry_date)
        self.storage.save(entry)
        return entry

    def get_entry(self, entry_id: str) -> DiaryEntry:
        """
        Retrieves a single entry by its unique ID.
        """
        return self.storage.load(entry_id)

    def list_all_entries(self) -> List[DiaryEntry]:
        """
        Retrieves all journal entries stored locally.
        """
        return self.storage.load_all()

    def search_by_date(self, target_date: Union[date, str]) -> List[DiaryEntry]:
        """
        Searches for entries matching a specific date (YYYY-MM-DD or date object).
        Demonstrates DateTime comparisons.
        """
        if isinstance(target_date, str):
            target_date = self.parse_date(target_date)

        all_entries = self.storage.load_all()
        matches = [e for e in all_entries if e.entry_date == target_date]
        return matches

    def edit_entry(
        self,
        entry_id: str,
        new_title: Optional[str] = None,
        new_content: Optional[str] = None
    ) -> DiaryEntry:
        """
        Modifies an existing diary entry and persists changes.
        """
        entry = self.storage.load(entry_id)
        entry.update(new_title=new_title, new_content=new_content)
        self.storage.save(entry)
        return entry

    def delete_entry(self, entry_id: str) -> bool:
        """
        Deletes a diary entry by its ID from local file storage.
        """
        return self.storage.delete(entry_id)

    def export_entry(self, entry_id: str, export_dir: str = "data/exports") -> str:
        """
        Exports an entry to a human-readable text file.
        """
        entry = self.storage.load(entry_id)
        path = self.storage.export_as_text(entry, export_dir=export_dir)
        return str(path)

