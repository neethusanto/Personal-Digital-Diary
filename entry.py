"""
DiaryEntry module representing a single journal entry.
Demonstrates Object-Oriented Programming (OOP) and DateTime management.
"""

from datetime import datetime, date
from typing import Dict, Any, Optional
import uuid


class DiaryEntry:
    """
    Represents an individual journal entry.
    
    Attributes:
        entry_id (str): Unique identifier for the entry.
        entry_date (date): The calendar date the entry belongs to.
        title (str): Title or headline of the entry.
        content (str): The body text of the diary entry.
        created_at (datetime): Timestamp when entry was created.
        updated_at (datetime): Timestamp when entry was last modified.
    """

    def __init__(
        self,
        title: str,
        content: str,
        entry_date: Optional[date] = None,
        entry_id: Optional[str] = None,
        created_at: Optional[datetime] = None,
        updated_at: Optional[datetime] = None,
    ):
        self.entry_id: str = entry_id or str(uuid.uuid4())[:8]
        self.entry_date: date = entry_date or date.today()
        self.title: str = title.strip()
        self.content: str = content.strip()
        self.created_at: datetime = created_at or datetime.now()
        self.updated_at: datetime = updated_at or self.created_at

    def update(self, new_title: Optional[str] = None, new_content: Optional[str] = None) -> None:
        """
        Updates entry title and/or content, and updates the modification timestamp.
        """
        if new_title is not None and new_title.strip():
            self.title = new_title.strip()
        if new_content is not None and new_content.strip():
            self.content = new_content.strip()
        self.updated_at = datetime.now()

    def to_dict(self) -> Dict[str, Any]:
        """
        Serializes the entry object into a dictionary for JSON/file storage.
        """
        return {
            "entry_id": self.entry_id,
            "entry_date": self.entry_date.strftime("%Y-%m-%d"),
            "title": self.title,
            "content": self.content,
            "created_at": self.created_at.strftime("%Y-%m-%d %H:%M:%S"),
            "updated_at": self.updated_at.strftime("%Y-%m-%d %H:%M:%S"),
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "DiaryEntry":
        """
        Factory method to reconstruct a DiaryEntry object from a dictionary.
        """
        entry_date = datetime.strptime(data["entry_date"], "%Y-%m-%d").date()
        created_at = datetime.strptime(data["created_at"], "%Y-%m-%d %H:%M:%S")
        updated_at = datetime.strptime(data["updated_at"], "%Y-%m-%d %H:%M:%S")

        return cls(
            title=data["title"],
            content=data["content"],
            entry_date=entry_date,
            entry_id=data["entry_id"],
            created_at=created_at,
            updated_at=updated_at,
        )

    def display(self) -> str:
        """
        Returns a beautifully formatted string representation of the entry.
        """
        divider = "=" * 60
        sub_divider = "-" * 60
        return (
            f"\n{divider}\n"
            f" Entry ID:   {self.entry_id}\n"
            f" Date:       {self.entry_date.strftime('%A, %B %d, %Y')} ({self.entry_date.strftime('%Y-%m-%d')})\n"
            f" Title:      {self.title}\n"
            f" Created At: {self.created_at.strftime('%Y-%m-%d %I:%M %p')}\n"
            f" Updated At: {self.updated_at.strftime('%Y-%m-%d %I:%M %p')}\n"
            f"{sub_divider}\n"
            f"{self.content}\n"
            f"{divider}\n"
        )

    def __str__(self) -> str:
        return f"[{self.entry_date.strftime('%Y-%m-%d')}] ({self.entry_id}) {self.title}"

    def __repr__(self) -> str:
        return f"<DiaryEntry id={self.entry_id} date={self.entry_date} title={self.title!r}>"

