/**
 * Personal Digital Diary - Modern JavaScript UX & Interactions
 */

document.addEventListener('DOMContentLoaded', function () {
    // 1. Live Navigation Clock & Dynamic Greeting
    function initClockAndGreeting() {
        const timeEl = document.getElementById('navLiveTime');
        const greetingEl = document.getElementById('heroDynamicGreeting');

        function updateTime() {
            const now = new Date();
            if (timeEl) {
                timeEl.textContent = now.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
            }

            if (greetingEl) {
                const hour = now.getHours();
                let greeting = 'Good Evening';
                if (hour >= 5 && hour < 12) {
                    greeting = 'Good Morning';
                } else if (hour >= 12 && hour < 17) {
                    greeting = 'Good Afternoon';
                }
                greetingEl.textContent = `${greeting}, Writer`;
            }
        }

        updateTime();
        setInterval(updateTime, 1000);
    }
    initClockAndGreeting();

    // 2. Real-time Word, Character & Read Time Counter
    const contentArea = document.getElementById('journalContentArea');
    const wordCountSpan = document.getElementById('wordCount');
    const charCountSpan = document.getElementById('charCount');
    const readTimeSpan = document.getElementById('readingTime');

    function updateCounts() {
        if (!contentArea) return;
        const text = contentArea.value.trim();
        const chars = text.length;
        const words = text ? text.split(/\s+/).filter(Boolean).length : 0;
        const minutes = Math.max(1, Math.ceil(words / 200));

        if (wordCountSpan) wordCountSpan.textContent = words;
        if (charCountSpan) charCountSpan.textContent = chars;
        if (readTimeSpan) readTimeSpan.textContent = `${minutes} min read`;
    }

    if (contentArea) {
        contentArea.addEventListener('input', updateCounts);
        updateCounts(); // initial invocation
    }

    // Read time calculator on Detail page
    const detailContentEl = document.getElementById('journalContentBody');
    const readingTimeCalc = document.getElementById('readingTimeCalc');
    if (detailContentEl && readingTimeCalc) {
        const text = detailContentEl.innerText.trim();
        const words = text ? text.split(/\s+/).filter(Boolean).length : 0;
        const minutes = Math.max(1, Math.ceil(words / 200));
        readingTimeCalc.textContent = `${words} words &bull; ${minutes} min read`;
        readingTimeCalc.innerHTML = `${words} words &bull; ${minutes} min read`;
    }

    // 3. Quick Date Presets (Today & Yesterday)
    const dateInput = document.getElementById('journalDateInput') || document.querySelector('input[type="date"]');
    const btnToday = document.getElementById('btnPresetToday');
    const btnYesterday = document.getElementById('btnPresetYesterday');

    function formatDate(d) {
        const year = d.getFullYear();
        const month = String(d.getMonth() + 1).padStart(2, '0');
        const day = String(d.getDate()).padStart(2, '0');
        return `${year}-${month}-${day}`;
    }

    if (dateInput) {
        if (btnToday) {
            btnToday.addEventListener('click', function () {
                dateInput.value = formatDate(new Date());
            });
        }

        if (btnYesterday) {
            btnYesterday.addEventListener('click', function () {
                const yesterday = new Date();
                yesterday.setDate(yesterday.getDate() - 1);
                dateInput.value = formatDate(yesterday);
            });
        }
    }

    // 4. Quick Date Filter Today Button
    const searchDateTodayBtn = document.getElementById('btnDateToday');
    const searchDateInput = document.getElementById('dateFilter');
    if (searchDateTodayBtn && searchDateInput) {
        searchDateTodayBtn.addEventListener('click', function () {
            const todayStr = this.getAttribute('data-today') || formatDate(new Date());
            searchDateInput.value = todayStr;
        });
    }

    // 5. Mood Selector Chips
    const moodChips = document.querySelectorAll('.mood-chip');
    const titleInput = document.getElementById('journalTitleInput');

    moodChips.forEach(function (chip) {
        chip.addEventListener('click', function () {
            const mood = this.getAttribute('data-mood');
            this.classList.toggle('active');

            if (contentArea) {
                // If not already in content, prepend mood tag
                if (!contentArea.value.includes(`[Mood: ${mood}]`)) {
                    contentArea.value = `[Mood: ${mood}]\n` + contentArea.value;
                    updateCounts();
                }
            }
        });
    });

    // 6. Delete Confirmation Modal
    const deleteModal = document.getElementById('deleteModal');
    if (deleteModal) {
        deleteModal.addEventListener('show.bs.modal', function (event) {
            const button = event.relatedTarget;
            if (!button) return;

            const entryTitle = button.getAttribute('data-title') || 'This entry';
            const deleteUrl = button.getAttribute('data-url');

            const titleEl = document.getElementById('modalEntryTitle');
            const formEl = document.getElementById('deleteForm');

            if (titleEl) {
                titleEl.textContent = entryTitle;
            }
            if (formEl && deleteUrl) {
                formEl.setAttribute('action', deleteUrl);
            }
        });
    }

    // 7. Auto-dismiss alerts after 5 seconds
    const alerts = document.querySelectorAll('.alert-dismissible');
    alerts.forEach(function (alert) {
        setTimeout(function () {
            const bsAlert = bootstrap.Alert.getOrCreateInstance(alert);
            if (bsAlert) {
                bsAlert.close();
            }
        }, 5000);
    });
});
