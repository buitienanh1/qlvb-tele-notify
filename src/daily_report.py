import os
import requests
from datetime import datetime
from .notifier import TelegramNotifier
from .qlvb_api import QLVBClient

def run_daily_report():
    print("📅 Starting daily error report generation...")
    
    # Initialize clients
    notifier = TelegramNotifier()
    qlvb = QLVBClient()
    
    # We check both main functions for errors
    monitored_functions = ['sendDoc', 'recvStatus']
    all_errors = []
    
    for func in monitored_functions:
        print(f"🔍 Scanning {func} for errors...")
        logs = qlvb.get_latest_errors(func)
        if logs:
            for log in logs:
                if log.get('status', '').lower() != 'thành công':
                    all_errors.append(log)
    
    if not all_errors:
        # Optionally send a "Everything is OK" message
        # notifier.send_alert(...) 
        print("✅ No errors found. No report needed.")
        return

    # Format the summary report
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    report_msg = (
        f"📊 <b>BÁO CÁO LỖI HÀNG NGÀY</b>\n"
        f"━━━━━━━━━━━━━━━━━━\n"
        f"⏰ <b>Thời điểm:</b> {timestamp}\n"
        f"📦 <b>Tổng số lỗi:</b> {len(all_errors)} bản ghi\n\n"
    )
    
    for i, err in enumerate(all_errors, 1):
        report_msg += (
            f"{i}. 🏢 <b>{err['unitName']}</b>\n"
            f"   📄 <code>{err['docId']}</code> - {err['function']}\n"
            f"   ❌ {err['status']}: {err['errorMessage']}\n"
            f"   ────────────────\n"
        )
    
    report_msg += "\n💡 <i>Vui lòng kiểm tra hệ thống QLVB để xử lý.</i>"
    
    # Send the summary report
    # Since send_alert expects QLVBErrorPayload, we'll use a direct call to the Telegram API
    # or a modified version of the notifier. For simplicity, we use the notifier's 
    # internal logic if we can, or a simple request.
    
    token = os.getenv('TELEGRAM_BOT_TOKEN')
    chat_id = os.getenv('TELEGRAM_CHAT_ID')
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    payload = {"chat_id": chat_id, "text": report_msg, "parse_mode": "HTML"}
    
    try:
        response = requests.post(url, json=payload, timeout=10)
        response.raise_for_status()
        print("✅ Daily report sent to Telegram successfully!")
    except Exception as e:
        print(f"❌ Failed to send daily report: {e}")

if __name__ == "__main__":
    run_daily_report()
