# CrawlDataFromUrl

## ✅ Step1: Download driver for your web browser
### Can skip this step if Edge browser version is 138.0.3351.95 or Chrome browser version is 140.0.7312.0 (r1490122)

Edge: https://developer.microsoft.com/en-us/microsoft-edge/tools/webdriver?form=MA13LH  
Chrome(download "chromedriver" version): https://googlechromelabs.github.io/chrome-for-testing/#dev  

## ✅ Step2: Create Google Cloud Project
Access: https://console.cloud.google.com/  
Create new project (Ex: CrawlDataFromUrl)  

## ✅ Step3: Enable Google Sheets API và Drive API
Project Home → Navigation menu → APIs & Services → Library:  
- Find Google Sheets API → Enable  
- Find Google Drive API → Enable  

## ✅ Step4: Create Service Account
Project Home → Navigation menu → APIs & Services → Credentials:  
- Create Credentials → Service account:  
    1️⃣ Create service account: Name the service account name (ví dụ: menu-writer) → Create and continue  
    2️⃣ Permissions (optional): Select a role → (Quick access) Basic → (Roles) Editor → continue
  
- Service Accounts:  
    ◼ Select email link (Copy this for Step5)  
    ◼ Select “Keys” tab → Add Key → Create new key → Select JSON → Create
    ◼ Download JSON file and rename it to credentials.json  

## ✅ Step5: Share Google Sheets editing permissions to service accounts
Access to a spreadsheet in Google Sheets → Share → Paste email in Step4 → Allow "Editor" permissions  

## ✅ Step6: Add url
For Edge browser:  
- Open "scrape_to_sheets_edge.py", in main function:  
    ◼ Change "menu_url" to food url  
    ◼ Change "executable_path" to the folder that include this "README.md" file  
    ◼ Change "sheet_name" to spreadsheet name  
    ◼ Change "worksheet_name" to worksheet name  

For Chrome browser: do the same with the Edge browser  

## ✅ Step7: Run file 
Run file "run_chrome.bat" for Chrome browser or "run_edge.bat" for Edge browser  
