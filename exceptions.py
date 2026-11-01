"""
Custom exceptions for the Personal Digital Diary application.
Demonstrates robust Exception Handling.
"""

class DiaryException(Exception):
    """Base exception class for all diary-related errors."""
    pass


class EntryNotFoundError(DiaryException):
    """Raised when an entry with the specified identifier or date is not found."""
    pass


class InvalidDateFormatError(DiaryException):
    """Raised when an invalid date string format is provided."""
    pass


class StorageError(DiaryException):
    """Raised when an error occurs during file reading, writing, or deletion."""
    pass

