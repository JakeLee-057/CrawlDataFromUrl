import time
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By

# === 1. Kết nối Google Sheets ===
def connect_to_sheet(spreadsheet_name, worksheet_name):
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    creds = ServiceAccountCredentials.from_json_keyfile_name("credentials.json", scope)
    client = gspread.authorize(creds)

    try:
        spreadsheet = client.open(spreadsheet_name)
    except gspread.exceptions.SpreadsheetNotFound:
        spreadsheet = client.create(spreadsheet_name)

    try:
        sheet = spreadsheet.worksheet(worksheet_name)
        sheet.clear()
    except gspread.exceptions.WorksheetNotFound:
        sheet = spreadsheet.add_worksheet(title=worksheet_name, rows="100", cols="20")

    sheet.update("A1:B1", [["Tên Món", "Giá Tiền"]])
    return sheet

# === 2. Scroll và thu thập dữ liệu ===
def scroll_and_collect_items(driver, step_px=400, wait_time=2.5, max_scrolls=50):
    collected_items = []
    seen_items = set()
    prev_height = 0
    idle_count = 0

    for i in range(max_scrolls):
        time.sleep(1.5) # Chờ DOM ổn định

        titles = driver.find_elements(By.CLASS_NAME, "item-restaurant-name")
        prices = driver.find_elements(By.CLASS_NAME, "current-price")

        for title, price in zip(titles, prices):
            name = title.text.strip()
            cost = price.text.strip()
            key = (name, cost)
            if name and cost and key not in seen_items:
                collected_items.append([name, cost])
                seen_items.add(key)

        print(f"⬇️ Scroll {i+1}: {len(collected_items)} món, height {prev_height}")

        # Scroll xuống
        driver.execute_script(f"window.scrollBy(0, {step_px});")
        time.sleep(wait_time)

        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == prev_height:
            idle_count += 1
            if idle_count >= 4:
                print("✅ Đã cuộn tới cuối và không còn món mới.")
                break
        else:
            idle_count = 0
            prev_height = new_height

    return collected_items

# === 3. Ghi dữ liệu lên sheet ===
def write_to_sheet(sheet, data):
    sheet.clear()
    sheet.append_row(["Tên Món", "Giá Tiền"])
    for row in data:
        sheet.append_row(row)
    print("✅ Đã ghi dữ liệu lên Google Sheet.")

# === 4. Hàm chính ===
def scrape_shopeefood_menu(path, url, sheet_name, worksheet_name):
    # Cấu hình trình duyệt Chrome
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--log-level=3")  # Giảm log rác
    service = ChromeService(path) # Update path
    driver = webdriver.Chrome(service=service, options=options)

    try:
        driver.get(url)
        time.sleep(5)  # Đợi trang tải

        print("🚀 Bắt đầu scroll và thu thập món ăn...")
        menu_items = scroll_and_collect_items(driver)
        print(f"✅ Tổng số món thu thập: {len(menu_items)}")

        print("📤 Gửi dữ liệu lên Google Sheets...")
        sheet = connect_to_sheet(sheet_name, worksheet_name)
        write_to_sheet(sheet, menu_items)

        # 🔗 Ghi đường dẫn Google Sheet vào file
        spreadsheet_url = sheet.spreadsheet.url
        with open("sheet_url.txt", "w", encoding="utf-8") as f:
            f.write(spreadsheet_url)
        print(f"📎 Google Sheet URL: {spreadsheet_url}")

    finally:
        driver.quit()

# === 5. Gọi chạy ===
if __name__ == "__main__":
    menu_url = "https://shopeefood.vn/ha-noi/rau-ma-la-nuoc-dua-sua-dau-nanh-tran-quoc-hoan"
    executable_path="E:\\ShopeeFood\\msedgedriver.exe"

    scrape_shopeefood_menu(
        path=executable_path,
        url=menu_url,
        sheet_name="FoodData",
        worksheet_name="Rau má lá"
    )