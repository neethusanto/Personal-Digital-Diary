# 📔 Personal Digital Diary

A modern, responsive full-stack **Django** web application designed for personal journaling and daily reflection. The project combines an elegant **HTML5, CSS3, JavaScript, and Bootstrap 5** frontend with a robust Python backend that stores journal entries directly in local files.

---

## 🌟 Key Features

- **Daily Journaling**: Write and publish reflections with meaningful titles, rich content, and mood selector tags (e.g., 🌟 Grateful, 🌿 Peaceful, 💡 Inspired).
- **Search Entries by Date**: Filter entries for any calendar date (`YYYY-MM-DD`) with one-click "Today" shortcuts and optional keyword searching.
- **Edit & Update**: Seamlessly modify existing entries; changes are synced immediately to disk.
- **Delete with Confirmation Safeguard**: Interactive modal prevents accidental deletion and safely removes the entry's JSON file from disk.
- **Local File Storage**: Each entry is persisted in a structured local file (`data/entries/entry_<id>.json`), satisfying local file handling requirements.
- **Plain-Text Export**: Export and download entries as formatted `.txt` files with full metadata (`data/exports/`).
- **Interactive UI/UX**:
  - Live character, word, and reading-time counter.
  - Dynamic local time clock and time-based greeting (*Good Morning / Afternoon / Evening*).
  - Clean editorial aesthetics with custom fonts (*Plus Jakarta Sans*, *Playfair Display*, *Lora*).

---

## 🧠 Core Programming Concepts

| Concept | Implementation in Project |
| :--- | :--- |
| **Object-Oriented Programming (OOP)** | Domain entity encapsulated in [`DiaryEntry`](entry.py); storage operations encapsulated in [`FileStorage`](storage.py); business logic organized in [`PersonalDiary`](diary.py); controller layer implemented using Django Class-Based Views (`BaseDiaryView`, `EntryListView`, `EntryCreateView`, `EntryDetailView`, `EntryEditView`, `EntryDeleteView`, `EntryExportView`). |
| **DateTime Handling** | Uses Python's `datetime.date` and `datetime.datetime` for date parsing (`strptime`), formatting (`strftime`), date-range queries, chronological sorting, and integration with HTML5 date widgets. |
| **File Handling** | Safe context managers (`with open(..., encoding='utf-8')`), JSON file serialization/deserialization, directory management (`Path.mkdir(parents=True, exist_ok=True)`), file deletion (`Path.unlink()`), and `.txt` file generation. |
| **Exception Handling** | Custom exception hierarchy in [`exceptions.py`](exceptions.py) (`EntryNotFoundError`, `InvalidDateFormatError`, `StorageError`); defensive programming against `OSError`, `PermissionError`, and `ValueError`, with user-friendly dismissible Bootstrap alerts. |

---

## 🛠️ Technology Stack

- **Backend**: Python 3.10+, Django 5+
- **Frontend**: HTML5, CSS3, JavaScript (ES6+), Bootstrap 5.3, Bootstrap Icons
- **Typography**: Google Fonts (*Plus Jakarta Sans*, *Playfair Display*, *Lora*)
- **Storage**: Local filesystem JSON & plain-text documents

---

## 📂 Project Structure

```
Personal Digital Diary/
├── data/
│   ├── entries/                         # Local JSON entry storage files
│   │   └── .gitkeep
│   └── exports/                         # Exported text files
│       └── .gitkeep
├── diary_core/                          # Django project configuration
│   ├── settings.py                      # Settings, static dirs & storage paths
│   ├── urls.py                          # Root URL routing
│   └── wsgi.py
├── diary_web/                           # Django diary application
│   ├── static/diary_web/
│   │   ├── css/diary.css                # Custom editorial styling & paper effects
│   │   └── js/diary.js                  # Live word counter, clock & modal scripts
│   ├── templates/diary_web/
│   │   ├── base.html                    # Base layout with navbar & centered footer
│   │   ├── entry_list.html              # Journal timeline, date search & filters
│   │   ├── entry_detail.html            # Editorial reading view
│   │   └── entry_form.html              # Journal writing studio & mood pills
│   ├── forms.py                         # Form validation & input widgets
│   ├── urls.py                          # App URL endpoints
│   ├── views.py                         # Class-Based Views
│   └── tests.py                         # Automated web test suite
├── entry.py                             # DiaryEntry model class (OOP)
├── storage.py                           # FileStorage manager class (File I/O)
├── diary.py                             # PersonalDiary business logic class
├── exceptions.py                        # Custom Exception hierarchy
├── main.py                              # Optional command-line interface
├── manage.py                            # Django management script
├── requirements.txt                     # Python package dependencies
├── .gitignore                           # Git ignore rules
└── README.md                            # Project documentation
```

---

## 🚀 Installation & Setup

### 1. Clone or Open the Repository
```bash
cd "Personal Digital Diary"
```

### 2. Create and Activate a Virtual Environment
**On Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```
**On macOS/Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Required Dependencies
```bash
pip install -r requirements.txt
```

### 4. Run Database Migrations
```bash
python manage.py migrate
```

### 5. Launch the Development Server
```bash
python manage.py runserver
```

Open your browser and navigate to:
```
http://127.0.0.1:8000/
```

---

## 🧪 Running Automated Tests

To run the complete test suite verifying views, date search, local file creation, editing, deletion, and exports:

```bash
python manage.py test
```

---

## 📄 License

This project is open-source and available under the [MIT License](LICENSE).
