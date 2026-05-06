import os
import requests
import logging
from datetime import datetime
from .models import QLVBErrorPayload

logger = logging.getLogger(__name__)

class TelegramNotifier:
    def __init__(self):
        self.token = os.getenv('TELEGRAM_BOT_TOKEN')
        self.chat_id = os.getenv('TELEGRAM_CHAT_ID')

    def send_alert(self, data: QLVBErrorPayload):
        if not self.token or not self.chat_id:
            logger.error("Telegram configuration missing in .env")
            return False

        url = f"https://api.telegram.org/bot{self.token}/sendMessage"
        
        now = datetime.now().strftime("%H:%M:%S")
        message = (
            f"⚠️ <b>CẢNH BÁO LỖI HỆ THỐNG QLVB</b>\n"
            f"━━━━━━━━━━━━━━━━━━\n"
            f"🏢 <b>Đơn vị:</b> {data.unitName} ({data.unitCode or 'N/A'})\n"
            f"📄 <b>Văn bản:</b> {data.docId} - {data.docName}\n"
            f"⚙️ <b>Chức năng:</b> <code>{data.function}</code>\n"
            f"❌ <b>Lỗi:</b> {data.status} - {data.errorMessage}\n"
            f"⏰ <b>Thời gian:</b> {data.timestamp or now}"
        )
        
        payload = {
            "chat_id": self.chat_id,
            "text": message,
            "parse_mode": "HTML"
        }
        
        try:
            response = requests.post(url, json=payload, timeout=10)
            response.raise_for_status()
            return True
        except Exception as e:
            logger.error(f"Failed to send Telegram alert: {e}")
            return False
