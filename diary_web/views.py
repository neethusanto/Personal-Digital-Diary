"""
Views for Personal Digital Diary.
Demonstrates:
- Object-Oriented Programming (Class-Based Views)
- DateTime handling and searching
- Local File Handling (reading, writing, deleting, exporting files)
- Comprehensive Exception Handling
"""

from datetime import datetime, date
from django.conf import settings
from django.contrib import messages
from django.http import Http404, HttpResponse, HttpRequest
from django.shortcuts import render, redirect
from django.views import View

from diary import PersonalDiary
from entry import DiaryEntry
from exceptions import (
    DiaryException,
    EntryNotFoundError,
    InvalidDateFormatError,
    StorageError,
)
from storage import FileStorage
from .forms import DiaryEntryForm


class BaseDiaryView(View):
    """
    Base view providing access to the PersonalDiary instance configured
    with the local file storage directory from settings.
    Demonstrates OOP inheritance.
    """
    def get_diary(self) -> PersonalDiary:
        storage = FileStorage(storage_dir=str(settings.DIARY_STORAGE_DIR))
        return PersonalDiary(storage=storage)


class EntryListView(BaseDiaryView):
    """
    Lists all diary entries with date searching and summary statistics.
    Demonstrates DateTime filtering and File Loading.
    """
    def get(self, request: HttpRequest):
        diary = self.get_diary()
        search_date_str = request.GET.get('date', '').strip()
        search_keyword = request.GET.get('q', '').strip().lower()
        
        parsed_search_date = None
        error_msg = None

        try:
            if search_date_str:
                # DateTime parsing and validation
                parsed_search_date = diary.parse_date(search_date_str)
                entries = diary.search_by_date(parsed_search_date)
            else:
                entries = diary.list_all_entries()

            # Optional keyword filtering within loaded entries
            if search_keyword:
                entries = [
                    e for e in entries
                    if search_keyword in e.title.lower() or search_keyword in e.content.lower()
                ]

        except InvalidDateFormatError as e:
            messages.warning(request, f"Invalid date specified: {e}. Showing all entries instead.")
            entries = diary.list_all_entries()
        except StorageError as e:
            messages.error(request, f"File Storage Error: {e}")
            entries = []

        context = {
            'entries': entries,
            'search_date': search_date_str,
            'search_keyword': search_keyword,
            'today_date': date.today().strftime('%Y-%m-%d'),
            'total_count': len(entries),
        }
        return render(request, 'diary_web/entry_list.html', context)


class EntryDetailView(BaseDiaryView):
    """
    Displays full details of a single diary entry loaded from disk.
    """
    def get(self, request: HttpRequest, entry_id: str):
        diary = self.get_diary()
        try:
            entry = diary.get_entry(entry_id)
            return render(request, 'diary_web/entry_detail.html', {'entry': entry})
        except EntryNotFoundError:
            messages.error(request, f"Entry with ID '{entry_id}' was not found.")
            return redirect('diary:entry_list')
        except StorageError as e:
            messages.error(request, f"Failed to read entry file: {e}")
            return redirect('diary:entry_list')


class EntryCreateView(BaseDiaryView):
    """
    Handles creating a new daily journal entry and writing it to a local file.
    Demonstrates Form validation, File writing, and Exception Handling.
    """
    def get(self, request: HttpRequest):
        initial_date = request.GET.get('date', date.today().strftime('%Y-%m-%d'))
        form = DiaryEntryForm(initial={'entry_date': initial_date})
        return render(request, 'diary_web/entry_form.html', {'form': form, 'is_edit': False})

    def post(self, request: HttpRequest):
        form = DiaryEntryForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data['title']
            content = form.cleaned_data['content']
            entry_date: date = form.cleaned_data['entry_date']
            
            diary = self.get_diary()
            try:
                # File Handling: persists as local file
                entry = diary.create_entry(
                    title=title,
                    content=content,
                    entry_date_str=entry_date.strftime('%Y-%m-%d')
                )
                messages.success(request, f"Journal entry '{entry.title}' saved successfully to local file!")
                return redirect('diary:entry_detail', entry_id=entry.entry_id)
            except (StorageError, InvalidDateFormatError, ValueError) as e:
                messages.error(request, f"Failed to save entry: {e}")
        
        return render(request, 'diary_web/entry_form.html', {'form': form, 'is_edit': False})


class EntryEditView(BaseDiaryView):
    """
    Allows editing an existing entry, persisting updates to its local file.
    """
    def get(self, request: HttpRequest, entry_id: str):
        diary = self.get_diary()
        try:
            entry = diary.get_entry(entry_id)
            form = DiaryEntryForm(initial={
                'title': entry.title,
                'entry_date': entry.entry_date,
                'content': entry.content,
            })
            return render(request, 'diary_web/entry_form.html', {
                'form': form,
                'entry': entry,
                'is_edit': True,
            })
        except EntryNotFoundError:
            messages.error(request, f"Entry with ID '{entry_id}' was not found.")
            return redirect('diary:entry_list')
        except StorageError as e:
            messages.error(request, f"Error accessing entry file: {e}")
            return redirect('diary:entry_list')

    def post(self, request: HttpRequest, entry_id: str):
        diary = self.get_diary()
        try:
            entry = diary.get_entry(entry_id)
        except EntryNotFoundError:
            messages.error(request, f"Entry with ID '{entry_id}' not found.")
            return redirect('diary:entry_list')

        form = DiaryEntryForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data['title']
            content = form.cleaned_data['content']
            new_date: date = form.cleaned_data['entry_date']

            try:
                entry.entry_date = new_date
                diary.edit_entry(entry_id=entry_id, new_title=title, new_content=content)
                messages.success(request, f"Entry '{entry.title}' updated successfully.")
                return redirect('diary:entry_detail', entry_id=entry.entry_id)
            except StorageError as e:
                messages.error(request, f"Failed to update entry file: {e}")

        return render(request, 'diary_web/entry_form.html', {
            'form': form,
            'entry': entry,
            'is_edit': True,
        })


class EntryDeleteView(BaseDiaryView):
    """
    Deletes an entry and removes its local file from disk.
    Demonstrates File deletion and Exception Handling.
    """
    def post(self, request: HttpRequest, entry_id: str):
        diary = self.get_diary()
        try:
            diary.delete_entry(entry_id)
            messages.success(request, f"Entry '{entry_id}' and its local file were deleted successfully.")
        except EntryNotFoundError:
            messages.error(request, f"Cannot delete: Entry '{entry_id}' was not found.")
        except StorageError as e:
            messages.error(request, f"Storage error during deletion: {e}")

        return redirect('diary:entry_list')


class EntryExportView(BaseDiaryView):
    """
    Exports and downloads a journal entry as a plain-text file (.txt).
    Demonstrates file generation and HTTP file delivery.
    """
    def get(self, request: HttpRequest, entry_id: str):
        diary = self.get_diary()
        try:
            entry = diary.get_entry(entry_id)
            export_path = diary.export_entry(entry_id, export_dir=str(settings.DIARY_EXPORT_DIR))
            
            with open(export_path, 'r', encoding='utf-8') as f:
                content = f.read()

            response = HttpResponse(content, content_type='text/plain; charset=utf-8')
            filename = f"diary_{entry.entry_date.strftime('%Y-%m-%d')}_{entry.entry_id}.txt"
            response['Content-Disposition'] = f'attachment; filename="{filename}"'
            return response
        except EntryNotFoundError:
            messages.error(request, f"Cannot export: Entry '{entry_id}' does not exist.")
            return redirect('diary:entry_list')
        except StorageError as e:
            messages.error(request, f"Failed to export entry: {e}")
            return redirect('diary:entry_list')
