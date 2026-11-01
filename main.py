"""
Main CLI Application for the Personal Digital Diary.
Provides an interactive command-line interface to interact with journal entries.
"""

import sys
from datetime import date
from diary import PersonalDiary
from exceptions import (
    DiaryException,
    EntryNotFoundError,
    InvalidDateFormatError,
    StorageError,
)


def print_header(title: str) -> None:
    print(f"\n{'=' * 60}")
    print(f" {title.center(58)} ")
    print(f"{'=' * 60}")


def get_multiline_input(prompt: str) -> str:
    """Reads multiple lines of input from the user until they type 'END' or press Ctrl+D/Ctrl+Z."""
    print(prompt)
    print("(Type your entry body below. On an empty new line, type 'END' to finish):")
    lines = []
    while True:
        try:
            line = input()
            if line.strip() == "END":
                break
            lines.append(line)
        except EOFError:
            break
    return "\n".join(lines).strip()


def handle_create_entry(diary: PersonalDiary) -> None:
    print_header("CREATE DAILY JOURNAL ENTRY")
    today_str = date.today().strftime("%Y-%m-%d")
    date_input = input(f"Enter date (YYYY-MM-DD) [Default: Today ({today_str})]: ").strip()
    entry_date_str = date_input if date_input else today_str

    title = input("Enter entry title: ").strip()
    if not title:
        print("[Error] Title cannot be empty!")
        return

    content = get_multiline_input("Enter your journal content:")
    if not content:
        print("[Error] Content cannot be empty!")
        return

    try:
        entry = diary.create_entry(title=title, content=content, entry_date_str=entry_date_str)
        print(f"\n[Success] Journal entry created successfully with ID: {entry.entry_id}")
        print(f"Saved to local file in: {diary.storage.storage_path / f'entry_{entry.entry_id}.json'}")
    except (InvalidDateFormatError, ValueError, StorageError) as e:
        print(f"\n[Error] {e}")


def handle_view_all_entries(diary: PersonalDiary) -> None:
    print_header("ALL JOURNAL ENTRIES")
    try:
        entries = diary.list_all_entries()
        if not entries:
            print("No journal entries found. Start by writing your first entry!")
            return

        print(f"Found {len(entries)} entry/entries:\n")
        print(f"{'ID':<10} | {'Date':<12} | {'Title'}")
        print(f"{'-' * 10}-+-{'-' * 12}-+-{'-' * 35}")
        for e in entries:
            print(f"{e.entry_id:<10} | {e.entry_date.strftime('%Y-%m-%d'):<12} | {e.title}")
    except StorageError as e:
        print(f"\n[Error] {e}")


def handle_search_by_date(diary: PersonalDiary) -> None:
    print_header("SEARCH ENTRIES BY DATE")
    date_str = input("Enter search date (YYYY-MM-DD): ").strip()

    try:
        matches = diary.search_by_date(date_str)
        if not matches:
            print(f"\nNo entries found for date: {date_str}")
            return

        print(f"\nFound {len(matches)} entry/entries for {date_str}:")
        for entry in matches:
            print(entry.display())
    except (InvalidDateFormatError, StorageError) as e:
        print(f"\n[Error] {e}")


def handle_view_single_entry(diary: PersonalDiary) -> None:
    print_header("VIEW ENTRY DETAILS")
    entry_id = input("Enter Entry ID to view: ").strip()
    if not entry_id:
        return

    try:
        entry = diary.get_entry(entry_id)
        print(entry.display())
    except (EntryNotFoundError, StorageError) as e:
        print(f"\n[Error] {e}")


def handle_edit_entry(diary: PersonalDiary) -> None:
    print_header("EDIT JOURNAL ENTRY")
    entry_id = input("Enter Entry ID to edit: ").strip()
    if not entry_id:
        return

    try:
        entry = diary.get_entry(entry_id)
        print("\n--- Current Entry ---")
        print(f"Title: {entry.title}")
        print(f"Content: {entry.content}\n")

        print("Press Enter to keep current values, or input new ones.")
        new_title = input(f"New title [{entry.title}]: ").strip()

        change_content = input("Do you want to edit the content? (y/n) [Default: n]: ").strip().lower()
        new_content = None
        if change_content in ("y", "yes"):
            new_content = get_multiline_input("Enter new content:")

        updated_entry = diary.edit_entry(
            entry_id=entry_id,
            new_title=new_title if new_title else None,
            new_content=new_content if new_content else None,
        )
        print(f"\n[Success] Entry '{updated_entry.entry_id}' updated successfully!")
    except (EntryNotFoundError, StorageError) as e:
        print(f"\n[Error] {e}")


def handle_delete_entry(diary: PersonalDiary) -> None:
    print_header("DELETE JOURNAL ENTRY")
    entry_id = input("Enter Entry ID to delete: ").strip()
    if not entry_id:
        return

    try:
        # Check if entry exists before confirming
        entry = diary.get_entry(entry_id)
        print(f"\nTarget Entry: [{entry.entry_date}] {entry.title}")
        confirm = input("Are you sure you want to delete this entry? (yes/no): ").strip().lower()
        if confirm == "yes":
            diary.delete_entry(entry_id)
            print(f"[Success] Entry '{entry_id}' and its local file were deleted successfully.")
        else:
            print("[Cancelled] Deletion cancelled.")
    except (EntryNotFoundError, StorageError) as e:
        print(f"\n[Error] {e}")


def handle_export_entry(diary: PersonalDiary) -> None:
    print_header("EXPORT ENTRY TO TEXT FILE")
    entry_id = input("Enter Entry ID to export: ").strip()
    if not entry_id:
        return

    try:
        export_file = diary.export_entry(entry_id)
        print(f"[Success] Entry exported to plain-text file:\n{export_file}")
    except (EntryNotFoundError, StorageError) as e:
        print(f"\n[Error] {e}")


def main() -> None:
    diary = PersonalDiary()

    while True:
        print("\n" + "=" * 60)
        print("          PERSONAL DIGITAL DIARY          ")
        print("=" * 60)
        print(" 1. Create Daily Journal Entry")
        print(" 2. View All Entries")
        print(" 3. Search Entries by Date")
        print(" 4. View Entry Details by ID")
        print(" 5. Edit an Entry")
        print(" 6. Delete an Entry")
        print(" 7. Export Entry to Text File")
        print(" 8. Exit")
        print("=" * 60)

        choice = input("Select an option (1-8): ").strip()

        if choice == "1":
            handle_create_entry(diary)
        elif choice == "2":
            handle_view_all_entries(diary)
        elif choice == "3":
            handle_search_by_date(diary)
        elif choice == "4":
            handle_view_single_entry(diary)
        elif choice == "5":
            handle_edit_entry(diary)
        elif choice == "6":
            handle_delete_entry(diary)
        elif choice == "7":
            handle_export_entry(diary)
        elif choice == "8":
            print("\nThank you for using Personal Digital Diary. Goodbye!\n")
            sys.exit(0)
        else:
            print("\n[Invalid Option] Please enter a number between 1 and 8.")


if __name__ == "__main__":
    main()

