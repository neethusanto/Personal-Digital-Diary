"""
Django web tests for Personal Digital Diary.
Tests web views, forms, search by date, local file persistence, and deletion.
"""

import shutil
import tempfile
from pathlib import Path
from django.test import TestCase, override_settings
from django.urls import reverse

from entry import DiaryEntry
from storage import FileStorage
from diary import PersonalDiary


class DiaryWebTestCase(TestCase):
    def setUp(self):
        # Use temporary directory for testing file persistence
        self.test_dir = tempfile.mkdtemp()
        self.storage_dir = Path(self.test_dir) / 'entries'
        self.export_dir = Path(self.test_dir) / 'exports'
        self.storage_dir.mkdir(parents=True, exist_ok=True)
        self.export_dir.mkdir(parents=True, exist_ok=True)

        # Override settings for the duration of this test
        self.settings_override = self.settings(
            DIARY_STORAGE_DIR=self.storage_dir,
            DIARY_EXPORT_DIR=self.export_dir
        )
        self.settings_override.enable()

    def tearDown(self):
        self.settings_override.disable()
        shutil.rmtree(self.test_dir, ignore_errors=True)

    def test_entry_list_view_empty(self):
        response = self.client.get(reverse('diary:entry_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No Memories Found")

    def test_create_entry_via_web(self):
        url = reverse('diary:entry_create')
        post_data = {
            'title': 'Web Journal Test',
            'entry_date': '2026-11-01',
            'content': 'Created through Django web form!',
        }
        response = self.client.post(url, data=post_data, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Web Journal Test")
        self.assertContains(response, "Created through Django web form!")

        # Verify local file was created in storage_dir (File Handling)
        files = list(self.storage_dir.glob("entry_*.json"))
        self.assertEqual(len(files), 1)

    def test_search_entries_by_date(self):
        # Create two entries on different dates
        storage = FileStorage(storage_dir=str(self.storage_dir))
        diary = PersonalDiary(storage=storage)
        diary.create_entry("Day 1 Entry", "Content 1", "2026-11-01")
        diary.create_entry("Day 2 Entry", "Content 2", "2026-11-02")

        # Search for 2026-11-01
        response = self.client.get(reverse('diary:entry_list') + '?date=2026-11-01')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Day 1 Entry")
        self.assertNotContains(response, "Day 2 Entry")

    def test_edit_entry_via_web(self):
        storage = FileStorage(storage_dir=str(self.storage_dir))
        diary = PersonalDiary(storage=storage)
        entry = diary.create_entry("Original Title", "Original Content", "2026-11-01")

        edit_url = reverse('diary:entry_edit', kwargs={'entry_id': entry.entry_id})
        post_data = {
            'title': 'Updated Title',
            'entry_date': '2026-11-01',
            'content': 'Updated Content via Form',
        }
        response = self.client.post(edit_url, data=post_data, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Updated Title")

        # Check local file content
        reloaded = diary.get_entry(entry.entry_id)
        self.assertEqual(reloaded.title, "Updated Title")
        self.assertEqual(reloaded.content, "Updated Content via Form")

    def test_delete_entry_via_web(self):
        storage = FileStorage(storage_dir=str(self.storage_dir))
        diary = PersonalDiary(storage=storage)
        entry = diary.create_entry("To Delete", "Delete Me", "2026-11-01")

        filepath = self.storage_dir / f"entry_{entry.entry_id}.json"
        self.assertTrue(filepath.exists())

        delete_url = reverse('diary:entry_delete', kwargs={'entry_id': entry.entry_id})
        response = self.client.post(delete_url, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertFalse(filepath.exists(), "Local file should be deleted")

    def test_export_entry_as_txt(self):
        storage = FileStorage(storage_dir=str(self.storage_dir))
        diary = PersonalDiary(storage=storage)
        entry = diary.create_entry("Export Title", "Body to export", "2026-11-01")

        export_url = reverse('diary:entry_export', kwargs={'entry_id': entry.entry_id})
        response = self.client.get(export_url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Type'], 'text/plain; charset=utf-8')
        self.assertIn("Export Title", response.content.decode('utf-8'))
