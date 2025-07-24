@echo off
echo === ĐANG CHẠY EDGE SCRAPER ===

:: Bước 1: Cài thư viện nếu thiếu
echo ✅ Installing required packages...
pip install -r requirements.txt

:: Bước 2: Xoá file URL cũ nếu có
del sheet_url.txt >nul 2>&1

:: Bước 3: Chạy script Python
echo 🚀 Running Edge crawler...
python scrape_to_sheets_edge.py

:: Bước 4: Đọc file URL và mở trình duyệt
set /p SHEET_URL=<sheet_url.txt
start "" "%SHEET_URL%"

pause
